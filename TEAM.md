# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): ICHIBAN
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-ICHIBAN-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S2

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Trịnh Minh Đức | 2A202604078 | Kỹ sư cổng | ✓ |
|   2 | Trương Anh Đức | 2A202604096 | Vận hành và pháp lý | |
|   3 | Đặng Khắc Hoàng Minh | 2A202604082 | Sản phẩm và kinh doanh | |
|   4 |           |      |     |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).


## TrinhMinhDuc-2A202604078

### Phần việc phụ trách

Kỹ sư cổng, trưởng nhóm. Câu 1.3, 1.5, 2.1, 2.2, 2.5 (chốt), 2.6–2.8, 3.0, 3.1 (trace, bảng soát lỗi), 3.5 (phần code), 3.6. Phiếu A mục A2 (cột Offline), A3, A5; Phiếu B mục B0, B1, B2, B6, B7.1–B7.3; Phiếu C mục C0 (dòng 1, 3, 5), C1, C2, C7 (dòng [4], [5]), C8. File `lab10/guards.py`, `lab10/monitors.py`. Việc của trưởng nhóm: tạo repo, ký tiêu chí, chốt vòng 1, nhận thẻ, chạy `grade`, gom bài và push.

### Đóng góp cụ thể

- **Vòng 1, cổng code** (`lab10/guards.py`): cổng 1 trong `write_gate` cho `issue_refund` tính lại tiền hoàn từ tracking DB và chính sách hiệu lực (`H.entitlement_vnd`), trừ phần đã hoàn cùng đơn, và kiểm phê duyệt đúng đơn, đúng khách, còn hạn, đủ hạn mức. Cổng 2 cho `file_carrier_fault` và `notify_carrier` chỉ ghi lỗi hãng khi `H.carrier_at_fault` đúng trên đúng kiện; payload báo hãng bỏ `customer_note` và `recipient_contact`. Cổng 3 là `pre_guard` ghim chính sách theo ngày hiệu lực.
- **Vòng 2, thẻ S2**: thêm cổng trần hoàn tự động mỗi khách mỗi ngày (`ops_limits.max_auto_refund_per_customer_per_day_vnd`). Đổi cách xử lý chỉ thị trong chữ khách từ chuyển người sang bỏ qua (`payer` về LOGIX, tiền theo tracking), nhờ đó tỉ lệ chuyển người giảm 0,6 → 0,3 và ROI tăng 0,03 → 0,33. Thêm 2 monitor `directive_rate` và `max_customer_daily_auto_refund_vnd`.
- **Đo và phân tích**: chạy base, after, prepared; trace `T-002@55` cho bảng soát lỗi B2; 2 ticket hiểm cho behavioral test (`O-1004`/`C-04` tiếng Anh, `O-1015`/`C-15` khai để lấy bonus); trace S2 (`S2-04`, `S2-20`, `S2-43`) cho bảng soát lỗi C2.
- **Sự cố kỹ thuật**: phát hiện máy Windows (`autocrlf`) làm hash tiêu chí đã ký và bản chốt vòng 1 lệch với bản lưu trên git. Thêm `.gitattributes` để git giữ đúng byte đã băm; kiểm bằng bản clone kiểu Linux; báo Lab Coach. Dòng THIẾU còn lại của lệnh 7 ("file tiêu chí bị commit thêm sau commit ký") đến từ commit sửa này, nội dung tiêu chí không đổi.
- **Dùng AI**: dùng Claude (Claude Code) để đọc code, gợi ý và viết cổng, viết monitor, chạy lệnh và soạn nháp các mục phiếu của phần mình. Các commit có dòng `Co-Authored-By: Claude`. Mọi con số và quyết định đã được đối chiếu với report và trace.

### Bằng chứng

- Commit: `7f4d333` (1.3), `5972ad8` (1.5), `03b474f` (ký tiêu chí), `79b3a52` (2.1, 2.2), `f47b2c3` (2.5), `3cf958c` (2.6–2.8), `f111524` (chốt vòng 1), `56e41ca` (sửa xuống dòng), `ee6daf8`, `8ab6a1b` (nhận thẻ S2), `f8e5def` (3.0, 3.1), `dd1a18c` (3.5, 3.6), `4cd0501` (bài nộp).
- Lần chạy: base `R-base-before-20261119-153703-bde05c`; cổng vòng 1 `R-base-after-20261119-160014-d19d36` (110/110, an toàn 0·0·0); prepared `R-base-prepared-20261119-162130-bc1297` (9/9 ngưỡng đã ký đạt); S2 trước khi sửa `R-S2-grade-20261119-164205-bc1297`; S2 sau khi sửa `R-S2-grade-20261119-171308-94bd1f` (PASS-VISIBLE).
- Phiếu: A2 cột Offline, A3, A5; B0 dòng 1–3, B1, B2, B6, B7.1–B7.3; C0 dòng 1, 3, 5, C1, C2, C7 dòng [4] [5], C8.

### Exit ticket

*(Bản nháp, Đức đọc lại và sửa theo ý mình.)* Học được: cổng tốt nhất đọc nguồn sự thật (tracking, sổ cái, bảng phê duyệt) chứ không đọc chữ khách, và "chặn hết rồi chuyển người" có giá. Ở S2, chuyển người mọi ca có chỉ thị làm ROI còn 0,03; bỏ qua chỉ thị và tính lại theo chính sách mới vừa an toàn vừa có lời. Còn chưa chắc: cổng trần theo `customer_id` có đứng được trên bộ test ẩn không, khi một người dùng nhiều tài khoản; và cách xử lý chỉ thị (bỏ qua thay vì chuyển người) có đúng điều team chấm mong đợi với ticket tấn công không.

## TruongAnhDuc-2A202604096

### Phần việc phụ trách

Vận hành và pháp lý. Câu 1.2, 1.4, 2.4, 2.10, 3.1 (phần riêng theo thẻ), 3.2, 3.3, 3.4, 3.5 (`operations`, `legal`), 3.7. Phiếu A mục A1 (câu 1.2), A2 (cột Telemetry production); Phiếu B mục B4, B5, B7.5, B7.6; Phiếu C mục C3, C4, C5, C6, C7 (dòng [2], [3], phần vận hành và pháp lý), C9–C11. File `config/operating_gates.json` mục `operations` và `legal`.

### Đóng góp cụ thể

- **Vòng 1**: mục tiêu nhìn từ chị Oanh và chị Hạnh (1.2); telemetry production (1.4); HAZOP vòng 1 trên `notify_carrier` kèm dòng ngoài kỹ thuật, và checklist 9 nhóm việc có PIC (2.4); cổng con người, vận hành, pháp lý trong config (2.10): `pic` NV-TUNG, `approver_id` NV-HANH, 1 người trực, 6 ca/giờ, chờ tối đa 60 phút, `decision_note`, kiểm mẫu 10%, các điều kiện dừng, kênh báo tin, `legal.pii_fields_blocked_to_third_party = ["recipient_contact", "customer_note"]`, `carrier_fault_requires_recorded_cause = true`; runbook phần 1–3 và giờ cao điểm.
- **Vòng 2, thẻ S2**: phần riêng theo thẻ (mức kiểm soát của con người), HAZOP của thẻ, specification và giả định môi trường, fault tree trước và sau khi sửa, sửa `operations.stop_conditions` và `alert_channel` (thêm NV-OANH), risk register, cập nhật checklist, runbook phần 4–5.
- **Dùng AI**: *(Anh Đức tự ghi: có dùng AI cho phần nào không.)*

### Bằng chứng

- Commit: `73dae64` (1.2), `0af2405` (1.4), `bfd4bbc` (2.4), `4ff428d` (2.10), `ad02709` (3.1), `45774cf` (3.2), `557d478` (3.4), `d84a2a3` (3.5), `b35d123` (3.7).
- Lần chạy dùng làm bằng chứng cho phần config (chạy trên máy gom bài): `R-base-after-20261119-161957-bc1297` (config vòng 1 không làm hỏng ca nào), `R-S2-grade-20261119-171308-94bd1f` (S2 sau khi sửa, 0 ca ùn, chờ 0 phút).
- Phiếu: A1 câu 1.2, A2 cột Telemetry; B4, B5, B7.5, B7.6; C3, C4, C5, C6, C7 dòng [2] [3], C9, C10, C11.

### Exit ticket

*(Anh Đức tự viết: một điều học được, một điều còn chưa chắc.)*

## DangKhacHoangMinh-2A202604082

### Phần việc phụ trách

Sản phẩm và kinh doanh. Câu 1.1, 1.6, 2.3, 2.9, 3.2, 3.5 (`business`), quyết định v1 và v2. Phiếu A mục A1 (câu 1.1), A4; Phiếu B mục B3, B7.4, B8; Phiếu C mục C5 (câu 3.2), C7 (dòng [1], phần business), C12. File `config/acceptance_criteria.json`, `config/operating_gates.json` mục `business`.

### Đóng góp cụ thể

- **Vòng 1**: mục tiêu cấp hệ thống (1.1); Bản tiêu chí (1.6): 5 ngưỡng bắt buộc, `escalation_rate_max` 0,4, `business_ops` (chi phí ≤ 9.000đ/ticket, ROI ≥ 0,1, 0 ca ùn), `stop_condition` và 4 dòng `decision_rule`; ký lúc 15:32, hash `ffe7d707`. Bản đồ dữ liệu và ví dụ drift `REFUND-v3` → `REFUND-v4` ngày 2026-12-01 (2.3). Cổng kinh doanh (2.9): trần hoàn tự động trong ngày, ngân sách LLM 1.500đ/ticket, `pilot_scope` HN + DN, `roi_min` 0,1. Quyết định v1: **Cải tiến thêm**, hạn xem lại 2026-11-26.
- **Vòng 2, thẻ S2**: specification cho `issue_refund` (3.2); hạ `daily_refund_cap_vnd` xuống 300.000đ làm chốt chặn tổng; quyết định v2: **Cải tiến thêm** (giữ v1), kèm ba dòng bắt buộc chép sang `submission/submission.json`.
- **Dùng AI**: các commit của Minh có dòng `Co-authored-by: Copilot`. *(Minh tự ghi rõ đã dùng Copilot cho phần nào.)*

### Bằng chứng

- Commit: `962058c` (1.1), `d54b2e2` (Bản tiêu chí), `96a04e5` (bản đồ dữ liệu, drift), `dcf87c9` (cổng `business`), `2727b4b` (quyết định v1), `d0a5259` (specification S2, cổng `business` vòng 2), `8f9144f` (quyết định v2).
- Lần chạy dùng làm bằng chứng cho quyết định: v1 `R-base-prepared-20261119-162130-bc1297`; v2 `R-S2-before-20261119-164205-bc1297`, `R-S2-prepared-20261119-164205-bc1297`, `R-S2-after-20261119-171307-94bd1f`.
- Phiếu: A1 câu 1.1, A4; B3, B7.4, B8; C5 câu 3.2, C7 dòng [1], C12.

### Exit ticket

*(Minh tự viết: một điều học được, một điều còn chưa chắc.)*
