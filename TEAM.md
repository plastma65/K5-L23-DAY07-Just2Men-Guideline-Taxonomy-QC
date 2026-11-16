# Thông tin nhóm

- Tên nhóm: Just2Men
- Repo bài nộp (URL): https://github.com/plastma65/K5-L23-DAY07-Just2Men-Guideline-Taxonomy-QC
- Commit chốt bài (hash):
- Số thành viên: 2 → số người gán mỗi ảnh (K): 2

| STT | MSHV        | Họ và tên     | Lớp (L2 / L3 / khác) | Tài khoản GitHub |
| --- | ----------- | ------------- | -------------------- | ---------------- |
| 1   | 2A202603230 | Trần Tuấn Anh |          L2          | plastma65        |
| 2   | 2A202603227 | Doãn Tùng Lâm |          L2          | doantunglam      |

Danh sách trên phải khớp dòng tiêu đề của `README.md` (đã đổi theo [SUBMISSION.md](SUBMISSION.md)) và `--members` đã dùng ở `scripts/split_assign.py`.

## Phân công (mỗi người làm gì ngoài phần gán nhãn)

| MSHV | Phụ trách thêm |
| ---- | -------------- |
| 2A202603230 | Nhóm trưởng: fork repo, `TEAM.md`/README; tổng hợp `guideline_v1.0_agreed.md` + `taxonomy.json` + nhãn CVAT; chạy `split_assign`, `qc_compare`, `build_final`, `qc_sample`, `qc_report`; chốt `calibration_decisions.csv`, viết v1.1 và v1.2; sửa nhãn calibration và Rework vòng 1 trên CVAT; người kiểm QC vòng 1; viết `QC_REPORT.md`; sửa 3 lỗi script (ghi trong `QC_REPORT.md` mục 6) |
| 2A202603227 | Viết phần ca khó (35 ca `img_0xx`) và phần lớn quy tắc được chọn cho v1.0 (thuộc tính `on_vehicle`, ngưỡng 10/40/70 %, `truncated` ≤ 3 px, đám đông); họp chốt v1.0 và calibration; người kiểm QC chính vòng 2 (`qc_review.csv`) |

## Kết quả tóm tắt (điền cuối bài)

- Số thành viên / số lần gán mỗi ảnh (K): 2 / 2
- IAA trước calibration: IoU trung bình 0.836 (< 0.85, chưa đạt), đồng thuận lớp 99.7 % (mẫu số: 306 cặp box ghép)
- Số ảnh phải calibration: 35 / 40
- Tỉ lệ lỗi sau calibration: vòng 1 10.0 % theo ảnh (4/40), 1.3 % theo đối tượng (5/381); vòng 2 (sau Rework) 10.0 % theo ảnh (4/40), 1.0 % theo đối tượng (4/391; thực tế 5/391 vì một dòng gộp 2 chỗ bỏ sót)
- **Quyết định:** Rework — lý do một dòng: 4/40 ảnh lỗi > 2 % ở cả hai vòng, 100 % lỗi là bỏ sót xe đỗ / vật nền / đám đông (lỗi hệ thống), IAA IoU dưới ngưỡng.
