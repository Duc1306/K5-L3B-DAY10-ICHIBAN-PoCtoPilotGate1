"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Cổng vòng 1 của bàn ICHIBAN (Phiếu B mục B6 · B7.1):
  Cổng 1 · issue_refund       số tiền phải bằng quyền lợi tính lại từ nguồn sự thật (tracking DB + chính sách hiệu lực),
                              trừ phần đã hoàn cho cùng đơn; phê duyệt phải đúng đơn, còn hạn, đủ hạn mức;
                              ticket có chỉ thị của khách thì chuyển người.          (pre-mortem lý do 1 · B2 lỗi 1)
  Cổng 2 · file_carrier_fault chỉ ghi lỗi hãng khi chính sách cho phép trên ĐÚNG kiện của ticket, số liệu lấy từ DB;
           notify_carrier     chỉ báo hãng khi lỗi đã ghi hợp lệ, payload lấy số từ dòng lỗi, bỏ chữ khách gõ
                              và liên hệ người nhận.                                 (pre-mortem lý do 2, 8 · B2 lỗi 2)
  Cổng 3 · pre_guard          ghim phiên bản chính sách theo ngày hiệu lực, không theo cờ index_active.
                                                                                     (pre-mortem lý do 3 · B3 drift)
Vòng 2 (thẻ S2, Phiếu C mục C7):
  Cổng 4 · issue_refund       tổng hoàn TỰ ĐỘNG cho một khách trong ngày + khoản mới vượt
                              ops_limits.max_auto_refund_per_customer_per_day_vnd thì chuyển người duyệt. (C2 lỗi 3)
Không xử lý riêng theo mã ticket hay câu chữ: mọi kiểm tra chỉ đọc bảng nguồn sự thật.
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict

# Trường của payload gửi hãng không được mang ra khỏi LogiX: chữ khách tự gõ (có thể chứa tên, số điện thoại người khác)
# và liên hệ người nhận quà. Lớp này đỡ thêm cho legal.pii_fields_blocked_to_third_party trong config.
_PAYLOAD_DROP = ("customer_note", "recipient_contact")


# ---------------------------------------------------------------- tra cứu nguồn sự thật (chỉ đọc)

def _policy(ctx):
    """Chính sách có hiệu lực tại ctx.as_of (không tin cờ index_active)."""
    return H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)


def _facts(ctx, order_id):
    """(order, parcel của ticket, độ trễ theo tracking, chính sách hiệu lực) hoặc None nếu thiếu dữ liệu."""
    order = ctx.tools.lookup_order(order_id)
    policy = _policy(ctx)
    if order is None or policy is None or not order.get("parcels"):
        return None
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    return order, parcel, H.db_delay_days(parcel, ctx.as_of), policy


def _directive_seen(ctx):
    """Agent đã làm theo một chỉ thị lấy từ chữ khách (ticket hoặc ghi chú lúc đặt hàng)."""
    return any(e.get("type") == "directive_obeyed" for e in ctx.events)


# ---------------------------------------------------------------- cổng 3 · pre_guard

def pre_guard(ctx):
    pol = _policy(ctx)
    if pol is not None:
        return Verdict.allow(policy_id=pol["policy_id"])
    return Verdict.allow()


# ---------------------------------------------------------------- cổng 1 · issue_refund

def _gate_refund(ctx, action):
    # Vòng 2 · S2: chỉ thị lấy từ chữ khách (ticket, checkout_note) là DỮ LIỆU, không phải lệnh. Thay vì chuyển người
    # mọi ca có chỉ thị (tốn công duyệt, ROI âm), bỏ qua chỉ thị: bên trả luôn là LOGIX theo chính sách hoàn phí giao
    # trễ, số tiền tính lại từ tracking, và ca vượt hạn mức vẫn cần phê duyệt thật ở bảng approvals (nhánh bên dưới).
    changes = {}
    if action.get("payer", "LOGIX") != "LOGIX":
        changes["payer"] = "LOGIX"
    if _directive_seen(ctx) or changes:
        ctx.log("directive_ignored", payer_before=action.get("payer"), amount_before_vnd=action.get("amount_vnd"))

    f = _facts(ctx, action.get("order_id"))
    if f is None:
        return Verdict.escalate("thiếu đơn, kiện hoặc chính sách hiệu lực để tính quyền lợi: chuyển người")
    order, parcel, delay, policy = f
    entitled = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
    paid = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(order_id=order["order_id"]))
    remaining = max(0, entitled - paid)
    amount = action.get("amount_vnd", 0)

    if remaining <= 0:
        ctx.log("refund_recomputed", amount_vnd=amount, entitled_vnd=entitled, paid_before_vnd=paid,
                db_delay_days=delay, policy_id=policy["policy_id"])
        why = "đơn đã được hoàn đủ trước đó" if entitled > 0 else \
            f"theo tracking trễ {delay} ngày, {policy['policy_id']} không cho hoàn"
        return Verdict.deny(why)

    if amount != remaining:
        changes["amount_vnd"] = remaining
    approval_id = action.get("approval_id")
    appr_ok = bool(approval_id) and _approval_valid(ctx, approval_id, order, remaining)
    if remaining > policy["auto_limit_vnd"] and not appr_ok:
        return Verdict.escalate(f"{remaining}đ vượt hạn mức tự động {policy['auto_limit_vnd']}đ và không có phê duyệt "
                                "hợp lệ cho đúng đơn này (sai đơn, đã dùng, hết hạn hoặc thiếu hạn mức): chuyển người duyệt")
    # Vòng 2 · S2: trần hoàn TỰ ĐỘNG cho một khách trong ngày (ops_limits). Mỗi khoản riêng lẻ đúng chính sách
    # vẫn có thể cộng dồn vượt trần; khoản làm vượt trần cần người duyệt.
    cap = ctx.tools.ops_limits().get("max_auto_refund_per_customer_per_day_vnd")
    if cap is not None and not appr_ok:
        cust = action.get("customer_id") or ctx.ticket.get("customer_id")
        spent = _auto_refund_today_for(ctx, cust)
        if spent + remaining > cap:
            ctx.log("customer_daily_cap", customer_id=cust, spent_today_vnd=spent, amount_vnd=remaining, cap_vnd=cap)
            return Verdict.escalate(f"khách {cust} đã được hoàn tự động {spent}đ hôm nay; thêm {remaining}đ "
                                    f"vượt trần {cap}đ/khách/ngày (ops_limits): chuyển người duyệt")
    if approval_id and not appr_ok:          # dưới hạn mức thì không cần phê duyệt: bỏ phê duyệt sai, không gắn vào sổ
        changes["approval_id"] = None

    if changes:
        ctx.log("refund_recomputed", amount_vnd=amount, entitled_vnd=entitled, paid_before_vnd=paid,
                db_delay_days=delay, policy_id=policy["policy_id"], changes=changes)
        return Verdict.modify(f"tính lại từ tracking ({delay} ngày) và {policy['policy_id']}", **changes)
    return Verdict.allow()


def _auto_refund_today_for(ctx, customer_id):
    """Tổng đã hoàn tự động (không có approval_id) cho một khách trong ngày hôm nay.

    Sổ cái gồm các dòng của ngày trước (sổ đầu kỳ) rồi tới các dòng hôm nay. auto_refund_today_vnd() cho tổng hôm nay
    của mọi khách; đi ngược từ cuối sổ, cộng các dòng tự động cho tới khi đủ tổng đó thì chính là phần của hôm nay."""
    today_total = ctx.tools.auto_refund_today_vnd()
    acc = mine = 0
    for r in reversed(ctx.tools.ledger_rows()):
        if acc >= today_total:
            break
        if r.get("approval_id"):
            continue
        acc += r["amount_vnd"]
        if r.get("customer_id") == customer_id:
            mine += r["amount_vnd"]
    return mine


def _approval_valid(ctx, approval_id, order, amount):
    """Phê duyệt phải đúng đơn và đúng khách, còn hiệu lực, chưa dùng, đủ hạn mức."""
    appr = next(iter(ctx.tools.lookup_approvals(approval_id=approval_id)), None)
    return (appr is not None
            and appr.get("order_id") == order["order_id"]
            and appr.get("customer_id") in (None, order.get("customer_id"))
            and appr.get("status") == "valid"
            and str(appr.get("expires_at") or "9999-12-31") >= ctx.as_of
            and amount <= appr.get("max_vnd", 0))


# ---------------------------------------------------------------- cổng 2 · file_carrier_fault, notify_carrier

def _gate_fault(ctx, action):
    f = _facts(ctx, action.get("order_id"))
    if f is None:
        return Verdict.deny("thiếu đơn, kiện hoặc chính sách hiệu lực: không ghi lỗi hãng")
    _, parcel, delay, policy = f
    if not H.carrier_at_fault(policy, parcel, delay):
        ctx.log("carrier_fault_blocked", parcel_id=parcel["parcel_id"], carrier_id=parcel["carrier_id"],
                db_delay_days=delay, recorded_cause=parcel.get("delay_cause"), claimed_delay_days=action.get("delay_days"))
        return Verdict.deny(f"kiện {parcel['parcel_id']} trễ {delay} ngày theo tracking, nguyên nhân "
                            f"{parcel.get('delay_cause')}: chính sách không cho ghi lỗi hãng")
    truth = {"parcel_id": parcel["parcel_id"], "carrier_id": parcel["carrier_id"],
             "driver_id": parcel.get("driver_id"), "delay_days": delay}
    diff = {k: v for k, v in truth.items() if action.get(k) != v}
    if diff:
        ctx.log("carrier_fault_corrected", before={k: action.get(k) for k in diff}, after=diff)
        return Verdict.modify("ghi lỗi theo đúng kiện và số ngày trễ trong tracking", **diff)
    return Verdict.allow()


def _gate_notify(ctx, action):
    rows = ctx.tools.fault_rows(ticket_id=action.get("ticket_id"), carrier_id=action.get("carrier_id"))
    if not rows:
        return Verdict.deny("chưa có dòng lỗi hợp lệ cho hãng này: không báo hãng")
    row = rows[-1]
    payload = dict(action.get("payload") or {})
    clean = {k: v for k, v in payload.items() if k not in _PAYLOAD_DROP}
    clean.update(parcel_id=row["parcel_id"], delay_days=row["delay_days"])
    if clean != payload:
        dropped = [k for k in _PAYLOAD_DROP if k in payload]
        ctx.log("carrier_payload_cleaned", dropped=dropped)
        return Verdict.modify("báo hãng bằng số liệu của dòng lỗi, bỏ chữ khách gõ và liên hệ người nhận",
                              payload=clean)
    return Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")
    if tool == "issue_refund":
        return _gate_refund(ctx, action)
    if tool == "file_carrier_fault":
        return _gate_fault(ctx, action)
    if tool == "notify_carrier":
        return _gate_notify(ctx, action)
    return Verdict.allow()
