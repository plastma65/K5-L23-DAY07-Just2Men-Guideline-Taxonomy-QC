# Ghi chú cá nhân — 2A202603230 - Trần Tuấn Anh

## 1. Pha 1: ba ca khó tôi tìm ra trong 40 ảnh

Bản guideline cá nhân Pha 1 của tôi viết quy tắc chung nhưng **chưa ghi ca theo `img_0xx`** (tôi định điền sau khi gán, đó là thiếu sót vì bản cá nhân không được sửa sau họp). Dưới đây là các ca khó tôi gặp khi gán (Pha 3), sửa calibration (Pha 5) và Rework sau QC vòng 1 (Pha 6); các mã R2, R6, R8 là quy tắc nhóm thêm sau calibration và QC:

| Ảnh | v0 không trả lời được gì | Quyết định của tôi | Lý do |
|---|---|---|---|
| img_013 | Nền xa có cụm xe nhỏ (van, xe trắng, xe tối) cao khoảng 20–25 px, bị cone che một phần | 1 `ignore_region` phủ cụm; không vẽ box riêng | Cụm ≥3 xe sát nhau, mỗi xe sát ngưỡng 20 px nên không đạt để vẽ riêng (R8). Vùng không đè lên box xe, người hay xe máy gần camera (R2). |
| img_019 | Đám đông sau rào chắn, người chen sát và che nhau nặng | 2 `ignore_region` phủ đám đông; giữ box riêng cho người đứng tách ở phía trước | Người trong đám đông không tách được ranh giới nên không vẽ từng box, nhưng cũng không để cụm nhận ra được mà không có box lẫn `ignore_region` (R8). Vùng không đè lên người và xe đã có box (R2). |
| img_036 | Hai dãy xe máy đỗ sát nhau ở mép trái và mép phải ảnh, bị xe tải xanh chắn một phần | 7 box `motorcycle` riêng (3 trái, 4 phải); box chạm mép đặt `truncated=yes`; occluded_level 0–1 | Từng xe đủ cao và thấy ≥½ thân nên vẽ riêng (R8); xe đỗ vẫn là xe thật. Không dùng `ignore_region` vì sẽ bỏ phí xe tách được. |
| img_039 | Ba xe máy đỗ cạnh cột điện, che nhẹ nhau | 3 box `motorcycle`, occluded_level 1, `truncated=no`, `on_vehicle=no` | Mỗi xe cao khoảng 45–55 px và thấy rõ nên đạt ngưỡng vẽ riêng (R8). Mức che phân vân thì chọn mức thấp (mốc 10/40/70 %). |
| img_040 | Phương tiện ở sát mép trái ảnh, bị cắt một phần | Gán `bus` | Theo R6, dựa vào phần hình dạng còn thấy; chưa có xe nào khác dễ nhầm trong khung. |
| img_005 | Người ngồi sau trên xe máy, không có box xe máy riêng cho người đó | Tôi gán `person`, `on_vehicle=yes` | Lúc gán tôi chưa chắc người ngồi sau chỉ cần `on_vehicle=yes` hay phải có box xe riêng. Theo guideline v1.0 (mục 3.4), mỗi xe một box và mỗi người một box `person`, nên người ngồi sau không cần box xe riêng. |
| img_025 | Xe màu vàng nhãn ISUZU, có thể là bán tải hoặc tải nhẹ | Tôi gán `car` | Tôi thấy dáng xe giống bán tải nhưng chưa chắc. Guideline v1.0 xếp cả bán tải lẫn tải nhẹ vào `truck`, nên gán `car` là tôi chưa áp đúng quy tắc (bản cá nhân Pha 1 của tôi từng xếp bán tải vào `car`). |
| img_004 | Tài xế xe ba bánh bên trái, hai chân lộ ra ngoài thân xe | Tôi không ghi lại quyết định lúc gán | Ca này cho thấy guideline cần nói rõ hơn cách vẽ box người so với box xe ba bánh khi một phần người lộ ra ngoài thân xe. |

## 2. Pha 2: chỗ tôi bất đồng với nhóm

Bản của tôi và của Lâm khác nhau ở 13 điểm (bảng mục 6 trong `guideline_v1.0_agreed.md`). Ba điểm lớn nhất:
- **Người trên xe:** tôi đề xuất lớp riêng `rider`; nhóm chốt `person` + thuộc tính `on_vehicle`. Tôi đồng ý: phép thử "mô hình có phải đoán ra không" cho thấy đây là thuộc tính, và lớp riêng dễ làm lệch lớp ở ca người ngồi trên xe đang đỗ (thực tế IAA lớp đạt 99.7 %).
- **Bán tải:** tôi xếp vào `car`; nhóm chốt `truck` vì đúng định nghĩa "khoang hàng tách cabin". Tôi đồng ý.
- **Ngưỡng `occluded_level`:** tôi đề xuất 5/35/70 %, nhóm chốt 10/40/70 % của Lâm vì mắt người khó phân biệt 0 % và 5 %.

## 3. Pha 3: ảnh tôi đã gán

- Số ảnh được giao: 40. Số box đã vẽ: 383 (person 167, motorcycle 84, car 63, ignore_region 25, truck 12, bicycle 11, three_wheeler 9, bus 8, van 4). Số lần tick `can_review`: 31 (nhiều nhất img_034: 9, img_014: 5, img_040: 3).
- Ca tôi lưỡng lự nhất: **img_005**, người ngồi sau xe máy không có box xe riêng. Tôi không chắc mỗi người ngồi sau phải đi kèm một box xe, hay chỉ cần `person` + `on_vehicle=yes` theo xe của người lái. Tôi đặt ca này lên đầu vì cảnh chở 2–3 người rất phổ biến trong 40 ảnh, hiểu sai sẽ lặp lỗi ở nhiều ảnh, còn img_025 chỉ ảnh hưởng một vật. Xem lại thì guideline mục 3.4 đã trả lời: mỗi người một box `person`, xe chỉ một box.

## 4. Pha 4–5: tôi lệch ở đâu

- **`occluded_level`:** trong 123 cặp lệch mức, tôi chấm **cao hơn** Lâm ở 101 cặp → lệch có hệ thống. Nguyên nhân chủ yếu là **guideline mơ hồ** (ước lượng % che bằng mắt, chưa nói phân vân thì chọn mức nào), một phần do cách tôi ước lượng → R1.
- **Box `bicycle`:** box của tôi to hơn Lâm ở 5/7 ca IoU thấp, có thể do tôi tính cả hàng chở → **tôi chưa nắm quy tắc** "chỉ thân xe" của v1.0 (R4).
- **Bỏ sót / thừa:** tôi dùng 25 `ignore_region` (Lâm 17), nhiều chỗ Lâm vẽ từng người còn tôi bao vùng → guideline chưa rõ ranh giới (R2).
- Quyết định calibration tôi thấy quan trọng nhất: **R1** (cải thiện được thuộc tính có đồng thuận thấp nhất, 59.8 %), và **R8** sau QC (lỗi duy nhất còn lại là bỏ sót vật ở mép và nền).

## 5. Bài học

- Lần sau tôi sẽ ghi ca khó theo `img_0xx` ngay ở Pha 1, và đưa một bước bắt buộc "quét bốn mép ảnh và nền" vào guideline ngay từ v1.0: sau calibration, lỗi duy nhất còn lại ở cả hai vòng QC là bỏ sót đúng kiểu này.
