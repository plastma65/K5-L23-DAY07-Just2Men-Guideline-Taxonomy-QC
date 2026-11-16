# Ghi chú cá nhân — 2A202603227 - Doãn Tùng Lâm


## 1. Pha 1: ca khó tôi tìm ra trong 40 ảnh

Ở bản guideline cá nhân (`individual/guideline_2A202603227_DoanTungLam.md`), mục 4 "Ca khó" **chưa điền**. Bản cá nhân không được sửa sau họp, nên mục này vẫn trống.

Phần ca khó theo `img_0xx` tôi viết sau, cho `guideline_v1.0_agreed.md` (mục 4, 35 ca). Ba ca tôi thấy v0 không trả lời được:

| Ảnh | v0 không trả lời được gì | Quyết định trong v1.0 |
|---|---|---|
| img_007 / img_037 | Pickup có nắp thùng cao trông giống van | `truck` vì cabin và thùng tách rời (img_037); bán tải luôn là `truck` |
| img_004 / img_035 | Người ngồi sau kính chắn gió tuk-tuk có gán không | Không gán; chỉ gán người thấy trực tiếp từ sườn hở |
| img_028 | Pickup chở tượng ngựa: box có gồm tượng không | Box `truck` chỉ gồm thân xe; tượng không gán |


## 2. Pha 2: chỗ tôi bất đồng với nhóm

Hai bản cá nhân khác nhau ở 13 điểm (bảng mục 6 trong `guideline_v1.0_agreed.md`). Điểm khác giữa tôi và Anh, và kết quả:
- **Người trên xe:** tôi dùng `person` + thuộc tính `on_vehicle`, Anh đề xuất lớp `rider`. Nhóm chốt theo tôi.
- **Bán tải:** tôi xếp `truck`, Anh xếp `car`. Nhóm chốt `truck`.
- **Ngưỡng `occluded_level`:** tôi dùng 10/40/70 %, Anh dùng 5/35/70 %. Nhóm chốt theo tôi.


## 3. Pha 3: ảnh tôi đã gán

- Số ảnh được giao: 40. Số box trong file nộp `2A202603227_DoanTungLam.json`: **411** (person 196, motorcycle 92, car 62, ignore_region 17, bicycle 14, truck 12, three_wheeler 9, bus 7, van 2). Số lần tick `can_review`: **49** (nhiều nhất `img_034`: 14, `img_031`: 8, `img_014`: 5).
- Ca lưỡng lự nhất: `img_040`, xe sát mép trái chỉ thấy phần đầu, được gán `bus` + `can_review` vì không chắc `bus` hay `van`; nhóm chốt `bus` ở Pha 5.

## 4. Pha 4–5: tôi lệch ở đâu

Số liệu từ `QC_REPORT.md`:
- **`occluded_level`:** trong 123 cặp lệch mức, Anh chấm cao hơn nhãn của tôi ở 101 cặp. Nguyên nhân chính là guideline mơ hồ (ước lượng % che bằng mắt) → R1.
- **Box `person`:** nhãn của tôi to hơn Anh ở 34/77 cặp IoU thấp, không có chiều lệch hệ thống → vẽ chưa sát.
- **Bỏ sót / thừa:** 103 box không ghép được (61 chỉ tôi vẽ, 42 chỉ Anh vẽ); tôi vẽ từng người ở nhiều chỗ Anh dùng `ignore_region` → R2.
- **QC vòng 2 (tôi kiểm):** 4/40 ảnh có lỗi `bo_sot` (`img_006`, `011`, `019`, `032`), cả 4 là bỏ sót vật ở nền/mép/đám đông. Ba ảnh trong đó vòng 1 đã ghi `khong`, nên bản thân bước kiểm cũng sót.
- Quyết định calibration tôi thấy quan trọng nhất: **R8** (quét bốn mép ảnh và nền), vì đó là lỗi duy nhất còn lại sau calibration.


## 5. Bài học

- Một điều tôi sẽ làm khác khi viết guideline lần sau: điền ca khó theo `img_0xx` ngay ở Pha 1
