# Guideline gán nhãn — v0.1 (cá nhân) — 2A202603230 - Trần Tuấn Anh

- Phiên bản: v0.1 (bản cá nhân, sửa từ v0 của giảng viên)
- Ngày: 2026-11-16
- Người viết: Trần Tuấn Anh (2A202603230)
- Loại nhãn: bounding box trên ảnh đường phố · Công cụ: CVAT, xuất COCO 1.0

> Ký hiệu **[CHƯA CHỐT]** = mình thấy hợp lý nhưng cần đối chiếu với guideline của các thành viên khác ở Pha 2.

---

## 1. Mục tiêu

Nhãn dùng để huấn luyện mô hình **phát hiện người và phương tiện thật** trên ảnh đường phố châu Á
(camera giao thông, xe tự lái).

- **Sai nguy hiểm nhất:** bỏ sót người đi bộ, người đang lái xe máy/xe đạp, và xe thật ở gần → mô hình không phanh.
- **Sai gây nhiễu:** gán vật **không thật** (tượng, ma-nơ-canh, poster, phản chiếu, đồ chơi) thành người/xe → mô hình báo động giả.
- Tách `rider` khỏi `person` vì người đang ngồi trên xe di chuyển nhanh và theo hướng của xe, khác người đi bộ.
- Nguyên tắc khi phân vân: *"Về mặt hình ảnh, đây có phải người/xe thật không?"* Có → gán (kể cả xe đang đỗ, đang trưng bày, đang được chở). Không → không gán.

## 2. Lớp và thuộc tính

### 2.1. Lớp (mỗi vật thuộc đúng một lớp)

**Phương tiện**

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Xe 4 bánh cỡ nhỏ chở người, **tối đa 7 chỗ**, **kể cả bán tải (pickup)**. | Sedan, hatchback, SUV, crossover, taxi, xe 7 chỗ (Innova, Fortuner, Xpander), **bán tải / pickup** (Ranger, Hilux, Triton), xe cảnh sát con. | Xe 9 chỗ trở lên dáng hộp → `van`. Xe tải nhỏ có cabin riêng và thùng hàng (kể cả xe tải nhẹ 500kg–1 tấn) → `truck`. |
| `truck` | Xe chở hàng có **khoang hàng tách khỏi cabin** (thùng hở, thùng kín, bồn, sàn), **không phải bán tải**. | Xe tải, xe tải nhẹ, xe ben, xe bồn, container, **xe chở xe**, xe cẩu, đầu kéo. | Bán tải / pickup → `car`. Xe thùng kín liền cabin → `van`. |
| `van` | Xe dáng hộp, khoang khách/hàng **liền với cabin**, **9 đến 16 chỗ**, hoặc xe thùng kín chở hàng cỡ nhỏ. | Xe 9 chỗ (Limousine, Starex), xe 16 chỗ (Ford Transit, Hiace, Solati), van giao hàng, xe cứu thương dáng van. | Xe 7 chỗ → `car`. Xe từ ~20 chỗ, thân dài hình hộp chữ nhật → `bus`. |
| `bus` | Xe chở khách **từ khoảng 20 chỗ trở lên**, thân dài dáng **hộp chữ nhật** rõ rệt, nhiều cửa sổ khách chạy dọc thân. | Xe buýt thành phố, xe khách, xe giường nằm, minibus 20–29 chỗ (Coaster, County), xe đưa đón. | Xe 16 chỗ (Transit, Hiace, Solati): đầu xe nhô ra, thân ngắn → `van`. |
| `motorcycle` | Xe 2 bánh có động cơ, **chỉ tính phần xe**. | Xe máy, xe tay ga, mô tô, xe máy điện, xe máy chở hàng cồng kềnh. | Xe đạp điện dáng xe đạp (có bàn đạp, không sàn để chân) → `bicycle`. Xe máy kéo thùng thành 3 bánh → `three_wheeler`. |
| `bicycle` | Xe 2 bánh chạy bằng sức người hoặc xe đạp điện dáng xe đạp, **chỉ tính phần xe**. | Xe đạp, xe đạp thể thao, xe đạp điện có bàn đạp. | Xích lô (3 bánh) → `three_wheeler`. |
| `three_wheeler` | Xe 3 bánh chở khách hoặc hàng, có hoặc không có động cơ. | Tuk-tuk, xe lam, xích lô, xe ba gác máy, xe máy gắn thùng 3 bánh. | Xe máy 2 bánh chở hàng → `motorcycle`. |

**Người**

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `person` | Người thật **không ngồi trên** xe 2–3 bánh. | Người đi bộ, đứng, ngồi ghế đá, người bán hàng rong, người **dắt** xe (đi bộ cạnh xe), người ngồi trên thùng xe tải. | Người đang ngồi trên xe máy/xe đạp/xe 3 bánh → `rider`. Tượng, ma-nơ-canh, người trên poster/màn hình, phản chiếu → **không gán**. |
| `rider` | Người thật **đang ngồi trên** `motorcycle`, `bicycle` hoặc `three_wheeler` (người lái hoặc người ngồi sau/khách). | Người lái xe máy, người ngồi sau, trẻ em ngồi trước, người đạp xe, người lái tuk-tuk/xích lô, khách trên tuk-tuk nhìn thấy được. | Người dắt xe, đứng cạnh xe đang đỗ → `person`. Người ngồi trong ô tô → **không gán**. |

**Vùng**

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `ignore_region` | Vùng **không gán từng vật**; bỏ sót trong vùng này không tính lỗi. | Cụm từ 3 vật nhỏ (dưới 20px) trở lên, đám đông không tách được từng người, vùng quá tối/nhoè có nhiều vật. | Không dùng cho vật không thật (vật không thật thì **không gán gì**). Không dùng thay cho vật rõ ràng gán được. |

### 2.2. Vật không thuộc lớp nào

**Không gán** (không box, không `ignore_region`): xe kéo tay, xe đẩy hàng, xe bò/ngựa, động vật, xe lăn, ván trượt, tàu hoả/tàu điện. **[CHƯA CHỐT]**: tàu điện/tàu hoả có cần lớp riêng không.

### 2.3. Vật không thật → KHÔNG gán gì cả

Không gán bất kỳ lớp nào (kể cả `ignore_region`) cho: **tượng** (tượng người, tượng xe, tượng pickup), **ma-nơ-canh**,
**hình in** trên poster, biển quảng cáo, thân xe, màn hình; **phản chiếu** trong gương, kính, vũng nước;
**đồ chơi, mô hình thu nhỏ**; **xe giả tưởng/trang trí** không phải xe thật (xe làm bằng hoa, xe đạo cụ, mô hình sân khấu).

- Cách nhận biết: chất liệu (đá, đồng, nhựa bóng), đặt trên bệ, tư thế cứng bất thường, sai tỉ lệ, nằm trong khung tranh/màn hình.
- **Xe thật đang trưng bày, đỗ, đứng yên** (xe cổ trưng bày, xe trong showroom nhìn thấy từ đường) → **vẫn gán** theo lớp, vì về hình ảnh đó là xe thật.
- Không chắc thật hay giả → không gán, tick nhận xét vào mục Ca khó để đem ra họp.

### 2.4. Thuộc tính

**`occluded_level`** — ước lượng % diện tích vật **bị vật khác che** (phần nằm ngoài mép ảnh tính vào `truncated`, không tính ở đây):

| Mức | Nghĩa | Ngưỡng |
|---|---|---|
| `0` | Không bị che | dưới 5% |
| `1` | Che ít | 5% đến 35% |
| `2` | Che nhiều | 35% đến 70% |
| `3` | Che rất nặng | trên 70%, nhưng vẫn **chắc chắn** nhận ra lớp |

- Ước lượng nhanh: tưởng tượng box của toàn bộ vật rồi chia làm 4 phần. Bị che khoảng 1/4 → mức 1, khoảng 1/2 → mức 2, hơn 3/4 → mức 3.
- **Không nhận ra được lớp → không gán.** (v0 dùng mức 3 cho "không rõ"; bỏ cách hiểu đó vì nó trộn "bị che" với "không chắc".)
- `rider` bị chính xe che phần chân → vẫn tính là bị che (thường mức 1).

**`truncated`** — vật bị **mép ảnh** cắt:

| Giá trị | Ngưỡng |
|---|---|
| `no` | Dưới 10% vật nằm ngoài khung ảnh |
| `yes` | Từ 10% vật trở lên nằm ngoài khung ảnh |

**`can_review`** — tick khi: (a) không chắc lớp; (b) không chắc thật hay giả; (c) gặp tình huống guideline chưa nói tới.
Mỗi box tick `can_review` phải nêu được lý do khi họp calibration. Không tick chỉ vì box khó vẽ.

## 3. Quy tắc vẽ box

1. **Ôm sát phần nhìn thấy.** Mép box chạm điểm ngoài cùng của phần nhìn thấy (lệch tối đa ~2px), không đoán phần bị che.
   Gương chiếu hậu **có** tính. Ăng-ten, dây buộc hàng thò ra **không** tính.
2. **Vật bị che:** chỉ vẽ phần nhìn thấy. Vật bị một vật mảnh (cột điện, thân cây) **cắt đôi** → vẫn **một** box bao cả hai phần.
3. **Vật bị cắt mép ảnh:** box dừng ở mép ảnh, `truncated = yes` nếu từ 10% vật trở lên nằm ngoài khung.
4. **Người trên xe 2–3 bánh → 2 loại box riêng:**
   - Xe máy: `rider` + `motorcycle`. Xe đạp: `rider` + `bicycle`. Tuk-tuk/xích lô: `rider` (mỗi người nhìn thấy được) + `three_wheeler`.
   - Box `rider` chỉ bao người (gồm mũ bảo hiểm, áo mưa trùm). Box xe chỉ bao xe (bánh, tay lái, gương, hàng buộc trên xe).
   - Xe chở 2–3 người → mỗi người một box `rider`.
5. **Người ngồi trong ô tô, xe buýt, van, cabin xe tải** (thấy qua kính) → **không gán**. Box xe đã đại diện.
6. **Hàng hoá trên xe:** hàng dính liền xe (buộc trên xe máy, chất trên thùng xe tải) **tính vào box xe**. Người ngồi trên thùng xe tải → `person` riêng.
7. **Xe chở xe (car carrier, xe cứu hộ):** box `truck` bao cả xe tải và các xe đang chở (hình dạng tổng thể trên đường).
   Mỗi ô tô đang được chở **vẫn gán** `car` riêng, với `occluded_level` theo phần bị che.
8. **Xe chủ (ego):** nắp capo, tay lái, kính của xe đang chụp ảnh → **không gán**.
9. **Vật nhỏ:** box cao dưới **20px** (`min_box_height_px`) → không gán riêng.
   - Một hoặc hai vật nhỏ lẻ → bỏ qua.
   - Cụm **từ 3 vật nhỏ trở lên** nằm sát nhau → một `ignore_region` bao cả cụm.
10. **Đám đông / xe dày đặc:**
    - **Không tách được** từng cá thể (không thấy ranh giới đâu là người/xe nào) → `ignore_region` cho phần đó; các cá thể rõ ở mép vẫn gán riêng.
    - **Đếm và tách được** từng cá thể (mỗi cá thể cao ≥ 20px) → gán **từng box riêng**.
11. **Nhoè / tối / ngược sáng:** gán nếu nhận ra lớp **chắc chắn** và vẽ được mép box lệch dưới ~10% kích thước vật.
    Nếu không: có từ 3 vật trở lên → `ignore_region`; chỉ một hai vật → bỏ qua.
12. `ignore_region` vẽ ôm sát vùng cần bỏ qua, không phủ lên vật rõ ràng đã gán.

## 4. Ca khó

> Sẽ bổ sung sau khi tự xem và gán 40 ảnh `data/images/`. Mỗi dòng: ảnh, tình huống, quyết định theo guideline này, lý do.

| Ảnh | Tình huống | Quyết định | Lý do |
|---|---|---|---|
| img_0xx | | | |

### Câu hỏi chưa chốt, đem ra họp Pha 2

1. Ngưỡng `occluded_level` (5 / 35 / 70%) và `truncated` (10%): mình thấy hợp lý, cần đối chiếu với bản của các thành viên khác.
2. Ranh giới `van` / `bus`: 9–16 chỗ là `van`, từ ~20 chỗ (thân dài hình chữ nhật) là `bus`; bán tải xếp vào `car`. Cả nhóm có thống nhất không?
3. Người lái/khách trên `three_wheeler` có mui che kín 2 bên → vẫn là `rider` hay không gán như người trong ô tô?
4. Có cần lớp cho tàu điện/tàu hoả không?

## 5. QC và phiên bản

- Ngưỡng QC (theo `taxonomy.json`, không đổi): IoU trung bình giữa người gán ≥ **0.85**, đồng thuận lớp ≥ **95%**;
  box khớp khi IoU so với đồng thuận ≥ 0.85 (vật ≥ 50px) hoặc ≥ 0.7 (vật nhỏ); tỉ lệ ảnh lỗi ≤ **2%** mới Release.
- Ca mơ hồ khi gán: tick `can_review`, **không tự đoán**, không đổi guideline giữa Pha 3. Nhóm quyết ở họp calibration và ghi vào `calibration_decisions.csv`.
- Mọi thay đổi làm đổi nhãn → tăng phiên bản guideline và `taxonomy.json`.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản khởi đầu của giảng viên | — |
| v0.1 | Thêm lớp `bus`, `bicycle`, `three_wheeler`, `rider`; định nghĩa, ví dụ, phản ví dụ cho mỗi lớp; mốc số chỗ car (≤7, kể cả bán tải) / van (9–16) / bus (từ ~20, dáng hộp chữ nhật); ngưỡng % cho `occluded_level` và `truncated`; quy tắc vật không thật, người trên xe, người trong ô tô, xe chở xe, xe trưng bày, ego, vật nhỏ, đám đông (ignore_region hoặc từng box), nhoè/tối | v0 không trả lời được: tuk-tuk, xe đạp, xe buýt, xe chở xe, tượng, ma-nơ-canh, xe giả tưởng (xem mục 4) |
