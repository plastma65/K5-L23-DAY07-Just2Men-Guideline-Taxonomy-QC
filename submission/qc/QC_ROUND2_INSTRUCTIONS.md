# Hướng dẫn QC vòng 2 — Nhóm Just2Men

- Người kiểm vòng 2: **2A202603227 - Doãn Tùng Lâm**
- Guideline áp dụng: [`submission/guidelines/guideline_v1.2_rework.md`](../guidelines/guideline_v1.2_rework.md) (v1.1 + quy tắc **R8**)
- Vì sao Lâm kiểm: vòng 1 người kiểm là Anh, cũng là người sửa nhãn calibration. Vòng 2 đổi người để kiểm khách quan hơn.

## 1. Bối cảnh vòng 1

| Chỉ số | Vòng 1 | Mẫu số |
|---|---|---|
| Lỗi theo đối tượng | 1,3 % | 5/381 đối tượng |
| Ảnh có lỗi | **10,0 %** (ngưỡng ≤ 2 %) | 4/40 ảnh |
| Quyết định | **Rework** | |

5 lỗi vòng 1, **tất cả là `bo_sot`** (chi tiết: `submission/qc/qc_review_round1.csv`):

| Ảnh | Vị trí (x, y) | Mô tả |
|---|---|---|
| img_013 | x215–285, y412–440 | Xe tải nhỏ trắng + ô tô ở nền sau xe #140, cao ~20–25 px |
| img_019 | x130–440, y50–300 | Đám đông sau hàng rào bên trái, nhiều người cao > 50 px |
| img_036 | x0–95, y190–330 | Dãy xe máy đỗ bên trái |
| img_036 | x760–960, y185–330 | Dãy xe máy đỗ bên phải |
| img_039 | x465–545, y425–482 | Xe máy đỗ cạnh cột điện, cao ~50 px |

Các lỗi này đã được Anh sửa trên CVAT theo R8 trước khi Lâm kiểm (xem mục 2).

## 2. Thứ tự làm

1. **Anh** sửa 4 ảnh trên theo R8 trong Task calibration CVAT → export COCO 1.0 → thay `submission/qc/labels_calibrated_flagged.json` → chạy `build_final.py` → chạy `qc_sample.py --n 20 --seed 42 --force` (tạo lại ảnh duyệt và phiếu kiểm trống) → push.
2. **Lâm** `git pull`, rồi tạo ảnh duyệt trên máy mình (thư mục `work/` không có trên git):
   ```powershell
   $env:PYTHONUTF8 = "1"
   python scripts/qc_sample.py --n 20 --seed 42
   ```
   Lệnh này **không ghi đè** `qc_review.csv` đã có trên git (script báo "Giữ nguyên…"); nó chỉ vẽ lại ảnh nhãn cuối kèm id vào `work/review/`. **Không** thêm `--force`.
3. **Lâm** kiểm **cả 40 ảnh** và điền `submission/qc/qc_review.csv` (mục 3), commit + push bằng tài khoản của Lâm.
4. **Anh** chạy `qc_report.py`, viết `QC_REPORT.md` với số liệu cả hai vòng.

## 3. Cách kiểm và điền phiếu

Mở từng ảnh trong `work/review/` (mỗi vật có id in sẵn, ví dụ `#12 car`). Với mỗi ảnh, kiểm theo thứ tự:

1. **Bỏ sót (R8 — trọng tâm vòng này):** quét **bốn mép ảnh** và **phần nền** (vỉa hè, dãy xe đỗ, sau hàng rào, sau xe gần camera). Vật cao ≥ 20 px và thấy ≥ 1/2 mà không có box → `bo_sot`. Cụm ≥ 3 vật nhỏ không có box cũng không có `ignore_region` → `bo_sot`.
2. **Thừa:** box trên tượng, ma-nơ-canh, poster, phản chiếu, đồ chơi, xe chủ; box trùng hai lần một vật; box vật < 20 px đứng lẻ → `thua`.
3. **Sai lớp:** đối chiếu bảng lớp mục 2.1 (bán tải = `truck`; van/bus theo hình dáng; sidecar = `motorcycle`; xích lô = `three_wheeler`) → `sai_lop`.
4. **Sai vị trí / kích thước:** box hở rõ (> ~10 % kích thước vật) hoặc cắt mất một phần vật nhìn thấy; box `bicycle` / xe có tính cả hàng chở → `sai_vi_tri_kich_thuoc`.
5. **Sai thuộc tính:** `occluded_level` lệch ≥ 1 mức so với mốc 10/40/70 %, `truncated`, `on_vehicle` sai định nghĩa → `sai_thuoc_tinh`.

Điền `submission/qc/qc_review.csv` (cột `image, object_id, error_type, reviewer, note`):

- Ảnh không lỗi: `error_type = khong`.
- Ảnh có lỗi: **mỗi lỗi một dòng** (thêm dòng cùng tên ảnh); `object_id` = id trên ảnh; bỏ sót thì để trống id, mô tả vị trí (x, y) trong `note`.
- `error_type` chỉ nhận: `khong`, `bo_sot`, `thua`, `sai_lop`, `sai_vi_tri_kich_thuoc`, `sai_thuoc_tinh`.
- `reviewer = 2A202603227`.

Ví dụ:
```
img_001.jpg,,khong,2A202603227,
img_036.jpg,,bo_sot,2A202603227,xe máy đỗ bên phải x800 y200 vẫn chưa có box
img_008.jpg,57,sai_vi_tri_kich_thuoc,2A202603227,box hở phần bánh trước
```

## 4. Nguyên tắc

- Kiểm **độc lập**: không hỏi Anh "ảnh này đã sửa chưa", không xem phiếu vòng 1 khi đang kiểm (trừ mục 1 ở trên để biết bối cảnh).
- Chỉ ghi `khong` khi đã thực sự xem kỹ ảnh. Tìm ra lỗi rồi kết luận Rework vẫn được điểm; báo Release khi số liệu không đạt bị trừ điểm.
- Ngưỡng Release: ảnh có lỗi ≤ 2 % → với 40 ảnh, chỉ Release khi **0/40** ảnh lỗi.
- Ca nào guideline v1.2 chưa trả lời được: ghi vào `note` và báo nhóm trưởng (sẽ tính là `guideline-gap` → Hold).
