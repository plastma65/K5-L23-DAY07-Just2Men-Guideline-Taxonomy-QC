# Tóm tắt IAA (taxonomy v1.0)

- Ảnh được so sánh (có >=2 người gán): **40**; số người gán: 2
- IoU trung bình và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU >= 0.5, ghép 1-1 không phân biệt lớp). Box chưa ghép được thống kê riêng ở cột bỏ sót/thừa.
- Mẫu số: 306 cặp box ghép (tổng mọi cặp người gán, ảnh chung).

| Cặp | Ảnh | Cặp box ghép | IoU TB | Cùng lớp | Cùng occluded_level | Cùng truncated | Cùng on_vehicle | Chưa ghép (A/B) | Bỏ qua do ignore | Đạt IAA |
|---|---|---|---|---|---|---|---|---|---|---|
| **TỔNG** | 40 | 306 | 0.836 | 99.7% | 59.8% | 97.1% | 98.4% | 61/42 | 37 | CHƯA ĐẠT |
| 2A202603227|2A202603230 | 40 | 306 | 0.836 | 99.7% | 59.8% | 97.1% | 98.4% | 61/42 | 37 | CHƯA ĐẠT |

Ngưỡng IAA: IoU TB >= 0.85, đồng thuận lớp >= 95%.

Số ca bất thường: 441 ({'iou_thap': 126, 'sai_thuoc_tinh': 131, 'bo_sot_thua': 103, 'co_can_review': 80, 'sai_lop': 1}), trên 35 ảnh cần calibration.
