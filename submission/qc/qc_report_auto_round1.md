# Báo cáo QC tự động (nháp)

> Đây là **gợi ý** do script tính - người kiểm phải xác nhận. Script chỉ đếm theo phiếu kiểm bằng mắt người; không tự biết box có ôm sát vật hay không.

## Mẫu
- Cỡ mẫu: 40 ảnh (35 ca khó + 5 ngẫu nhiên), 381 đối tượng; tổng lô: 40 ảnh.
- Phiên bản taxonomy: v1.0

## Số đo
| Chỉ số | Giá trị | Mẫu số |
|---|---|---|
| Tỉ lệ lỗi **theo đối tượng** | 5/381 = 1.3% | 381 đối tượng trong mẫu (lỗi bỏ sót tính như 1 đối tượng lỗi) |
| Tỉ lệ **ảnh có lỗi** (dùng cho ngưỡng) | 4/40 = 10.0% | 40 ảnh trong mẫu |
| IoU trung bình (IAA, trước calibration) | 0.836 (ngưỡng 0.85) | 306 cặp box ghép |
| Đồng thuận lớp (IAA) | 99.7% (ngưỡng 95%) | 306 cặp box ghép |

Ngưỡng Release: ảnh có lỗi <= 2% (đếm theo ảnh).

## Top 3 loại lỗi
| Loại lỗi | Số lỗi | Ảnh ví dụ |
|---|---|---|
| bo_sot | 5 | img_013.jpg, img_019.jpg, img_036.jpg |

**Lỗi hệ thống**: 'bo_sot' lặp lại (5/5 lỗi) -> cần sửa quy tắc/guideline, không chỉ sửa từng ảnh.

## Gợi ý quyết định (người kiểm xác nhận)
**REWORK**

- tỉ lệ ảnh có lỗi 10.0% > 2%
- lỗi hệ thống: 'bo_sot' chiếm 5/5 lỗi
- IAA (đo trước calibration) dưới ngưỡng

Cây quyết định: Hold (guideline chưa rõ/dữ liệu hỏng) -> Rework (>ngưỡng, lỗi lặp, IAA thấp) -> Release.
