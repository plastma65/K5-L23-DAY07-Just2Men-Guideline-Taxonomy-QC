# Báo cáo QC — Nhóm Just2Men

> Số liệu lấy từ `submission/qc/iaa_summary.md`, `qc_report_auto_round1.md`, `qc_report_auto_round2.md` (= `qc_report_auto.md`). Mọi tỉ lệ đều kèm mẫu số.

## 1. Lô

| Mục | Giá trị |
|---|---|
| Tên lô | day07-street-40 |
| Số ảnh | 40 |
| Thành viên (MSHV) | 2A202603230 - Trần Tuấn Anh (nhóm trưởng), 2A202603227 - Doãn Tùng Lâm |
| Số lần gán mỗi ảnh (K) | 2 (mỗi người gán đủ 40 ảnh, `assignment.csv`, seed 42) |
| Phiên bản guideline lúc gán | v1.0 (`guideline_v1.0_agreed.md`, taxonomy `v1.0`) |
| Phiên bản guideline hiện tại | v1.2 (`guideline_v1.2_rework.md` = v1.1 sau calibration + R8 sau QC vòng 1); taxonomy vẫn `v1.0` |
| Nhãn cuối | `labels_calibrated.json/.csv`: 40 ảnh, 391 vật + 12 `ignore_region` (person 186, motorcycle 96, car 63, bicycle 14, truck 12, three_wheeler 9, bus 8, van 3) |

## 2. Mẫu QC

- Cỡ mẫu: **40 ảnh** (35 ảnh ca khó + 5 ảnh ngẫu nhiên, seed 42), tức **toàn bộ lô**.
- Cách chọn: `python scripts/qc_sample.py --n 20 --seed 42` lấy mọi ảnh bị cờ ở Pha 4 + 20 ảnh ngẫu nhiên. Vì 35/40 ảnh bị cờ, chỉ còn 5 ảnh không cờ nên mẫu = 40/40 ảnh. Như vậy **không nới lỏng** so với quy tắc "lô < 500 ảnh kiểm 100 %": lô 40 ảnh được kiểm 100 %, hai lần.
- Hai vòng kiểm, đổi người kiểm giữa hai vòng:

| Vòng | Người kiểm | Ngày | Nhãn được kiểm | Phiếu |
|---|---|---|---|---|
| 1 | 2A202603230 - Trần Tuấn Anh | 2026-11-16 | sau calibration (guideline v1.1), 381 vật | `qc_review_round1.csv` |
| 2 | 2A202603227 - Doãn Tùng Lâm | 2026-11-16 | sau Rework vòng 1 (guideline v1.2), 391 vật | `qc_review_round2.csv` (= `qc_review.csv`) |

- Hạn chế: nhóm 2 người nên người kiểm nào cũng đã gán cả 40 ảnh (không có người "ít tham gia nhất"). Vòng 2 đổi sang Lâm vì vòng sửa calibration và Rework do Anh làm, để người kiểm khác người sửa.

## 3. Số đo

### 3.1 IAA (trước calibration)

| Chỉ số | Giá trị | Mẫu số | Ngưỡng | Đạt? |
|---|---|---|---|---|
| IoU trung bình (cặp box ghép được) | **0.836** | 306 cặp box ghép (IoU ≥ 0.5) | ≥ 0.85 | **Không** |
| Đồng thuận lớp | **99.7 %** (305/306) | 306 cặp box ghép | ≥ 95 % | Có |
| Box không ghép được (bỏ sót/thừa) | 103 (61 chỉ Lâm vẽ, 42 chỉ Anh vẽ); 37 box khác được bỏ qua vì nằm trong `ignore_region` | 794 box của cả hai (Lâm 411, Anh 383, gồm `ignore_region`) | — | — |
| Đồng thuận `occluded_level` / `truncated` / `on_vehicle` | **59.8 %** / 97.1 % / 98.4 % | 306 cặp box ghép | — | — |

→ IAA **chưa đạt** do IoU (thiếu 0.014); lớp đạt rất cao. 126/306 cặp box có IoU dưới ngưỡng từng box (0.85 với box cao ≥ 50 px, 0.7 với box nhỏ hơn).

### 3.2 Tỉ lệ lỗi (mẫu QC, sau calibration)

| Cách đếm | Vòng 1 (Anh kiểm) | Vòng 2 (Lâm kiểm) |
|---|---|---|
| Theo **đối tượng** | 5 lỗi / 381 đối tượng = **1.3 %** | 4 lỗi / 391 đối tượng = **1.0 %** (*) |
| Theo **ảnh** (ngưỡng Release ≤ 2 %) | 4 ảnh lỗi / 40 ảnh = **10.0 %** | 4 ảnh lỗi / 40 ảnh = **10.0 %** |

(*) Ở vòng 2, dòng `img_019` gộp 2 chỗ bỏ sót (hàng đầu đám đông sau rào và đầu người nhoè ở tiền cảnh) vào một dòng, nên số lỗi theo đối tượng thực tế là **5/391 = 1.3 %**. Tỉ lệ theo ảnh không đổi. Nhóm không sửa tay phiếu kiểm sau khi nộp.

Với 40 ảnh, ngưỡng 2 % nghĩa là chỉ Release khi **0/40** ảnh lỗi (1/40 = 2.5 %).

## 4. Lỗi

Cả hai vòng chỉ tìm thấy **một loại lỗi**: bỏ sót. Không có lỗi thừa, sai lớp, sai vị trí/kích thước hay sai thuộc tính nào được ghi.

| Hạng | Loại lỗi | Số lỗi | Ảnh ví dụ | Nguyên nhân gốc |
|---|---|---|---|---|
| 1 | `bo_sot` | vòng 1: 5 (img_013, 019, 036 ×2, 039); vòng 2: 4 dòng / 5 chỗ (img_006, 011, 019, 032) | img_036 (hai dãy xe máy đỗ hai bên, không có box cũng không có `ignore_region`); img_032 (nhóm người cao ~70 px ở mép trái) | **Người gán / người sửa sót** khi quét mép ảnh và nền; guideline v1.1 có quy tắc (R2: vật ≥ 20 px, thấy ≥ 1/2 → box) nhưng không bắt buộc bước quét mép/nền → thêm R8 ở v1.2. Riêng img_019 vòng 2 là **người sửa áp sai R2** (bao người cao > 50 px bằng `ignore_region`). |
| 2 | (không có loại thứ hai) | 0 | — | — |
| 3 | (không có loại thứ ba) | 0 | — | — |

**Có lỗi lặp lại cùng một kiểu:** có. 100 % lỗi của cả hai vòng là bỏ sót **xe đỗ, người/xe ở nền hoặc ở rìa ảnh, đám đông**. Đây là lỗi hệ thống, không phải lỗi lẻ.

Thêm một quan sát quan trọng: **3/4 ảnh lỗi ở vòng 2 (img_006, 011, 032) đã được người kiểm vòng 1 đánh `khong`**. Hai người kiểm bắt được những chỗ bỏ sót khác nhau, nghĩa là bản thân bước kiểm cũng bỏ sót. Tỉ lệ lỗi thật nhiều khả năng **cao hơn** con số của từng vòng.

## 5. Calibration

- Số ảnh bị cờ: **35 / 40** (5 ảnh sạch: img_017, 020, 027, 033, 038, toàn là tượng / gương / ma-nơ-canh / đồ chơi → quy tắc "vật không thật không gán" hoạt động tốt).
- Số quyết định đã ghi: **446 dòng** trong `calibration_decisions.csv` (441 ca từ `calibration_candidates.csv` + 5 dòng `QC1-01…05` từ QC vòng 1), mỗi dòng trỏ tới một quy tắc R1–R8.
- Ba quyết định quan trọng nhất:
  1. 123 cặp lệch `occluded_level` (Anh chấm cao hơn Lâm ở 101 cặp) → **R1**: chỉ tính phần vật khác che, phân vân → mức thấp hơn, lấy cách chấm của Lâm làm chuẩn → v1.1.
  2. 103 box bỏ sót/thừa, tập trung img_008, 021, 032, 034 → **R2**: vật cao ≥ 20 px và thấy ≥ 1/2 thân → box riêng; phần còn lại của cụm ≥ 3 vật → `ignore_region` → v1.1.
  3. QC vòng 1: 5/5 lỗi là bỏ sót xe đỗ / vật nền → **R8**: bắt buộc quét bốn mép ảnh và nền trước khi chuyển ảnh → v1.2.
- Quy tắc mới đã vào guideline: v1.1 thêm R1, R2, R5, R7 (quy tắc mới), R3, R4 (nhắc lại cách vẽ, không đổi quy tắc), R6 (`bus`/`car` theo hình dáng; ca img_040 chốt `bus`); v1.2 thêm R8. Taxonomy không đổi.
- Nguyên nhân bất đồng chính:
  - **Guideline mơ hồ** (cả hai cùng lệch, lệch có hệ thống): `occluded_level` (ước lượng % che bằng mắt), ranh giới vẽ từng vật / `ignore_region` trong cảnh đông.
  - **Vẽ chưa sát** (ngẫu nhiên, không ai vẽ to hơn có hệ thống: Lâm vẽ to hơn ở 34/77 cặp `person` IoU thấp): IoU thấp ở `person`, `motorcycle`.
  - **Một người sai lớp**: 1 ca (img_040).
- Cách sửa nhãn: nạp `consensus_flagged.json` (box trung bình của hai người) vào CVAT, **áp R1 bằng script** `scripts/calib_apply_r1.py` (lấy `occluded_level` từ nhãn Lâm đã tự gán cho 367 box ghép được, đổi 22 giá trị; không phán đoán tự động nào), phần còn lại (R2–R7) sửa bằng tay trên CVAT: 418 → 390 box, 153 box thêm mới hoặc chỉnh, `can_review` 58 → 0. Rework vòng 1 thêm 13 box/vùng trên 4 ảnh → 391 vật.

## 6. Script kiểm được gì, không kiểm được gì

**Script đã kiểm:**
- `validate_labels.py`: tên file, lớp thuộc taxonomy, giá trị thuộc tính hợp lệ, box nằm trong ảnh, đủ ảnh được giao. Hai file nhãn cá nhân: 0 lỗi, 0 cảnh báo.
- `qc_compare.py`: IoU, đồng thuận lớp và thuộc tính, box không ghép được giữa hai người; liệt kê 441 ca bất thường.
- `build_final.py`: mỗi ảnh bị cờ có ≥ 1 dòng quyết định, file calibrated đủ ảnh và đúng taxonomy.
- `qc_report.py`: tính tỉ lệ lỗi hai cách và gợi ý quyết định **từ phiếu kiểm do người điền**.

**Script không kiểm được, và nhóm đã dùng mắt người ra sao:**
- **Box có ôm sát vật không:** script chỉ so hai người với nhau. Nhóm sửa bằng mắt toàn bộ 126 ca IoU thấp ở calibration (R3), phóng to khi vật < 100 px.
- **Cả nhóm cùng bỏ sót:** `qc_compare.py` không thấy vật mà cả hai đều không vẽ. Chính QC bằng mắt hai vòng mới tìm ra (img_006, 011, 013, 019, 032, 036, 039), và hai người kiểm còn bắt được lỗi khác nhau.
- **Cùng hiểu sai quy tắc:** script không biết. Nhóm phát hiện qua QC (ví dụ img_019 dùng `ignore_region` cho người > 50 px, trái R2).
- **Lớp có đúng thực tế không:** script chỉ kiểm tên lớp có trong taxonomy; lớp đúng hay sai do người kiểm đối chiếu ảnh.

**Sửa script và công cụ thêm** (RULES cho phép sửa bug nếu ghi lại):
1. `scripts/make_cvat_labels.py`: thuộc tính checkbox `can_review` sinh `values: []`, CVAT bản đang chạy từ chối ("attribute values must be a non-empty array") → sinh `values: ["false"]`.
2. `scripts/make_cvat_labels.py`: nhãn thiếu trường `type`, CVAT báo `unknown label type "undefined"` → thêm `"type": "rectangle"`. Đã đối chiếu toàn bộ file nhãn với hàm kiểm Raw của chính container CVAT: không còn lỗi. Tên lớp/thuộc tính không đổi.
3. `scripts/validate_labels.py`: chỉ chấp nhận MSHV toàn chữ số (`^\d+_`), trong khi MSHV của nhóm có chữ cái (`2A202603230`) → cho phép MSHV bắt đầu bằng chữ số, có thể kèm chữ cái. Các kiểm tra khác không đổi.
4. Thêm `scripts/calib_apply_r1.py` (công cụ của nhóm, không phải script gốc): áp quyết định R1 bằng cách chép `occluded_level` từ nhãn **người** (Lâm) sang box nháp ghép được (IoU ≥ 0.5, cùng lớp). Không dùng mô hình hay AI để gán nhãn.

Không sửa tay `iaa_summary.*`, `calibration_candidates.csv`, `consensus_draft.json`, `qc_report_auto*.md`; không đổi mục `rules` của `taxonomy.json`.

## 7. Quyết định

**Rework** — người kiểm: 2A202603227 - Doãn Tùng Lâm (vòng 2), xác nhận: 2A202603230 - Trần Tuấn Anh (nhóm trưởng), ngày 2026-11-16.

Lý do (đi theo cây Hold → Rework → Release):
1. **Guideline chưa rõ / dữ liệu hỏng?** Không. Không có ảnh hỏng; mọi lỗi tìm được đều có quy tắc trả lời (R2, R8), không có `guideline-gap` → không Hold.
2. **> 2 % ảnh lỗi, lỗi lặp lại, hoặc IAA dưới ngưỡng?** Có cả ba: ảnh lỗi 4/40 = 10.0 % ở cả hai vòng (> 2 %); 100 % lỗi là `bo_sot` cùng kiểu (lỗi hệ thống); IAA IoU 0.836 < 0.85.
3. **Kết luận:** **Rework**. Không Release vì cần 0/40 ảnh lỗi; sau hai vòng, mỗi vòng vẫn tìm ra lỗi mới.

Việc cần làm tiếp và ai làm:
- Sửa 4 ảnh lỗi vòng 2 theo R2/R8 (img_006, 011, 019 — bỏ `ignore_region` trên người > 50 px và vẽ box riêng, 032) — Trần Tuấn Anh.
- Vì hai người kiểm bắt lỗi khác nhau: vòng 3 **cả hai** cùng quét lại **toàn bộ 40 ảnh**, chỉ tập trung R8 (bốn mép ảnh, nền, sau rào, xe đỗ), mỗi người một nửa rồi đổi chéo — Trần Tuấn Anh + Doãn Tùng Lâm.
- Chạy lại `build_final.py` → `qc_sample.py --force` → `qc_report.py`; Release chỉ khi 0/40 ảnh lỗi.
- Bài học cho lô sau: đưa bước "quét mép và nền" (R8) vào ngay guideline v1.0 và vào checklist khi gán, vì đây là lỗi duy nhất còn lại sau calibration.
