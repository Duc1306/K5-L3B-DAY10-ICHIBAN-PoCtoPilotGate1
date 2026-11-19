# Phân công · LAB 10 · Bàn ICHIBAN

Repo và giá trị `team`: **`K5-L3B-DAY10-ICHIBAN-PoCtoPilotGate1`** (ghi đúng y hệt trong `config/acceptance_criteria.json` và `submission/submission.json`).

| Vai | Người | MSSV | Trưởng nhóm |
|---|---|---|:-:|
| **A · Kỹ sư cổng** | | | |
| **B · Sản phẩm và kinh doanh** | | | |
| **C · Vận hành và pháp lý** | | | |

Trưởng nhóm chạy các lệnh một lần của cả bàn: ký tiêu chí, chốt vòng 1, nhận thẻ, push bài.

## 1. Mỗi vai giữ file nào

Chỉ người giữ file mới sửa file đó. Người khác muốn đổi thì nhắn người giữ.

| File | Người giữ |
|---|---|
| `lab10/guards.py` | A |
| `lab10/monitors.py` (dict `MONITORS`) | A |
| `config/acceptance_criteria.json` | B. **Ký một lần, sau đó không ai mở lại** |
| `config/operating_gates.json` mục `business` | B |
| `config/operating_gates.json` mục `operations`, `legal` | C. **Pull trước khi sửa** vì B cũng sửa file này |
| `submission/submission.json` | C |
| `templates/form-a/b/c-*.md` | Ai viết mục nào thì sửa mục đó (bảng bên dưới) |
| `TEAM.md` | Trưởng nhóm điền bảng; mỗi người tự viết mục `## HoVaTen-MSSV` của mình |

Không sửa: `lab10/guards_round1.py`, `config/operating_gates.round1.json`, `config/round1.lock`, `data/`, các file `lab10/*.py` còn lại.

## 2. Việc theo từng khối

### Phút 0–15 · Cài đặt
| Ai | Việc |
|---|---|
| Trưởng nhóm | Fork, đặt tên repo, mời 2 bạn quyền Write, `git config user.name/email` |
| Cả bàn | Clone; chạy `python -m unittest discover -s tests` → `Ran 13 tests … OK`; điền bảng `TEAM.md` |

### Phút 15–65 · Khối 1 · Phiếu A (chưa chạy eval)
| Ai | Câu | Mục phiếu |
|---|---|---|
| A | 1.3 metric offline cho một bước của agent | A2 cột Offline |
| B | 1.1 mục tiêu hệ thống; 1.6 Bản tiêu chí + ranh giới đầu ra; điền `acceptance_criteria.json` | A1 · 1.1, A4 |
| C | 1.2 mục tiêu của chị Oanh và chị Hạnh; 1.4 telemetry production | A1 · 1.2, A2 cột Telemetry |
| Cả bàn | 1.5 đọc khoảng tin cậy | A3 |

**Phút 60–65 · Ký (B soát lại, trưởng nhóm chạy):**
```bash
python -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock
git commit -m "Sign acceptance criteria"
git push -u origin main
```
B điền A5 (giờ ký, mã commit).

### Phút 65–85 · Khối 2A · Phiếu B
| Ai | Câu | Mục phiếu |
|---|---|---|
| A | 2.1 chạy base + `gate`, ghi mã lần chạy; 2.2 trace `T-002@55`, điền bảng soát lỗi | B0, B1, B2 |
| B | 2.3 bản đồ dữ liệu + một ví dụ drift | B3 |
| C | 2.4 HAZOP (≥ 3 dòng + ≥ 2 dòng ngoài kỹ thuật); checklist 9 nhóm, mỗi dòng một PIC có tên | B4, B5 |
| Cả bàn | 2.5 pre-mortem 4 lăng kính, chọn 2–3 lý do sẽ thành cổng | B6 |

### Phút 85–105 · Khối 2B · Cổng phòng ngừa
| Ai | Câu | Mục phiếu |
|---|---|---|
| A | 2.6 code 2–3 cổng; 2.7 hai bước tránh rò rỉ dữ liệu; 2.8 behavioral test + 2 ticket hiểm (làm cùng B hoặc C) | B7.1, B7.2, B7.3 |
| B | 2.9 mục `business`: `daily_refund_cap_vnd`, `cost_budget_per_ticket_vnd`, `pilot_scope`, `roi_min`, mỗi số một câu lý do | B7.4 |
| C | 2.10 mục `operations` + `legal`; runbook phần 1–3; giờ cao điểm | B7.5, B7.6 |

A chạy lại `eval --stage after` và `unittest` sau mỗi lần sửa cổng; báo cả bàn nếu có ca mới hỏng.

### Phút 105–115 · Chốt vòng 1 · quyết định v1
| Ai | Việc |
|---|---|
| Trưởng nhóm | `python -m lab10.checkpoint` → `eval --suite base --stage prepared` → `gate` |
| B | Viết cột v1 ở B8 (quyết định, 3 bằng chứng có mã lần chạy, dòng `decision_rule`, kho/hãng xấu nhất, ngày quyết định lại) |
| Cả bàn | Chốt quyết định v1; commit + push |

### Phút 125–185 · Khối 3 · Phiếu C
| Ai | Câu | Mục phiếu |
|---|---|---|
| Trưởng nhóm | Nhận thẻ (3 lệnh ở README mục 3), chạy `grade --incident Sx` **trước khi sửa**, push | — |
| Cả bàn | 3.0 cổng vòng 1 đỡ được gì; ghi `Thẻ đã bốc:` | C0, C1 |
| A | 3.1 trace ≥ 2 ticket hỏng khác kiểu, bảng soát lỗi; 3.5 sửa cổng code; 3.6 thêm chỉ số theo dõi | C2, C7 (phần code), C8 |
| B | 3.2 specification; 3.5 sửa `business` (phạm vi, trần, ngân sách) | C5 · 3.2, C7 (phần business) |
| C | 3.1 phần riêng theo thẻ + HAZOP của thẻ; 3.3 giả định môi trường; 3.5 sửa `operations`/`legal`; 3.7 fault tree sau, risk register, checklist, runbook 4–5 | C3, C4, C5 · 3.3, C7 (phần ops/legal), C9, C10, C11 |
| Cả bàn | 3.4 fault tree trước khi sửa (≥ 2 nhánh ở 2 tầng, lá có bằng chứng) | C6 |

Sau khi sửa, A chạy:
```bash
python -m lab10.eval --suite Sx --stage after --note "đổi MỘT thứ: ..."
python -m lab10.eval --suite base --stage after --note "kiểm lại bộ nền sau khi sửa"
python -m lab10.grade --incident Sx
```
Cần thấy `monitor ✅` và `regression ✅`.

### Phút 185–200 · Quyết định v2 và gom bài
| Ai | Việc |
|---|---|
| B | C12: cột v2, đổi hay giữ so với v1 và vì con số nào, mã lần chạy 3 mốc, 3 dòng bắt buộc |
| C | Điền `submission.json` (`members` dạng `"HoVaTen-MSSV"`, `decision_v1`, `decision_v2`, `three_lines` chép từ C12); chạy `python -m lab10.check_submission --collect` tới khi `ĐỦ THÀNH PHẦN` |
| Cả bàn | Chốt quyết định v2. **Còn dòng vượt trần thì không chọn Tiếp tục.** |

### Phút 200–240 · Demo và nộp
| Ai | Việc |
|---|---|
| A | Chiếu report 3 mốc `base · prepared · after`; chạy ticket hiểm bàn kia đưa |
| B | Trình bày quyết định v2 và con số đỡ cho nó |
| C | Trình bày phần sửa ở người và quy trình; sau demo trả các số đã đổi thử về bản v2, chạy lại lệnh 6 và lệnh 7 |
| Trưởng nhóm | Push bài lần cuối |
| **Từng người** | Viết mục cá nhân + exit ticket trong `TEAM.md`; **tự nộp link repo trên LMS** |

## 3. Luật nhóm
- Pull trước khi sửa, commit nhỏ, push ngay sau khi xong một mục.
- Không chạy `eval` trước khi tiêu chí đã ký và push.
- Không viết cổng xử lý riêng theo mã ticket hay câu chữ cụ thể (bộ test ẩn sẽ bắt).
- Không chặn hết, không thu hẹp phạm vi về 0, không xếp thật nhiều người trực.
- Mọi con số phải có người giải thích được lúc demo. Ai đặt số thì người đó giải thích.
- Dùng AI cho phần nào thì ghi vào mục cá nhân trong `TEAM.md`.
