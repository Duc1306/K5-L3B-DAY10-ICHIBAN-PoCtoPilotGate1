# Bản chung từ Lab 9

Cả bàn dùng PRD v1.1 và eval card Lab 9 của **Trịnh Minh Đức** làm bản tham chiếu chung cho Day 10.

| File | Nguồn |
|---|---|
| [PRD_v1.1.md](PRD_v1.1.md) | `docs/PRD_v1.1.md`, commit `aa78486` (2026-11-18) |
| [eval_card.md](eval_card.md) | `docs/eval_card.md`, commit `aa78486` (2026-11-18) |

Repo gốc: https://github.com/Duc1306/K5-L3B-DAY09-TrinhMinhDuc-2A202604078-EvaluationandFailureAnalysis

Các link tương đối bên trong hai file (`evidence/…`, `m5_…md`, `../src/reports/…`) trỏ về repo Lab 9 nên không mở được ở đây. Muốn xem thì mở repo gốc.

## Dùng ở đâu trong Day 10

| Câu | Mục cần đọc |
|---|---|
| 1.1 · mục tiêu cấp hệ thống (Phiếu A, A1) | PRD §3 "Định nghĩa chạy đúng" |
| 1.2 · mục tiêu của chị Oanh và chị Hạnh (Phiếu A, A1) | PRD §2 "Phạm vi pilot", §6 "Bằng chứng còn thiếu / rủi ro mở", cùng `data/world.json` → `staff` |
| 1.3–1.4 · thước đo (Phiếu A, A2) | Eval card: cách đo, seed, grader |
| 1.6 · Bản tiêu chí (Phiếu A, A4) | PRD §5 "Cổng release", §7 "Khi nào lên v1.2" |

**Không chép ngưỡng hay con số từ Lab 9.** Lab 9 đo 14 item × 5 seed; Day 10 dùng bộ nền 22 ticket × 5 seed và có thêm chi phí, ROI, hàng chờ. Ngưỡng của bàn lấy căn cứ từ `data/world.json` (`ops_facts`, `ops_limits`).
