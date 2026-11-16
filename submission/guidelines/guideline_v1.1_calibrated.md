# Guideline gán nhãn — v1.1 (sau calibration) — Nhóm Just2Men

- Phiên bản: **v1.1** = v1.0 + 7 quy tắc bổ sung từ calibration (đánh dấu **[v1.1]**). Taxonomy **không đổi** (vẫn `v1.0`: không thêm/bớt lớp hay thuộc tính).
- Ngày: 2026-11-16
- Người viết: 2A202603230 - Trần Tuấn Anh, 2A202603227 - Doãn Tùng Lâm · Người chốt khi bất đồng: nhóm trưởng (Trần Tuấn Anh)
- Nguồn: tổng hợp từ `individual/guideline_2A202603230_TranTuanAnh.md` và `individual/guideline_2A202603227_DoanTungLam.md`; các chỗ hai bản khác nhau xem **mục 6**.
- Loại nhãn: bounding box trên ảnh đường phố · Công cụ: CVAT, xuất COCO 1.0

> Bản này dùng để sửa nhãn các ảnh bị cờ ở Pha 5 và để QC ở Pha 6. Mỗi quy tắc mới có mã R1–R7 khớp cột `quy_tac_ghi_vao_guideline` trong `submission/qc/calibration_decisions.csv`.

---

## 1. Mục tiêu

Nhãn dùng để huấn luyện mô hình **phát hiện người và phương tiện có thật đang có mặt trên đường** (camera giao thông, xe tự lái), cả cảnh thưa lẫn cảnh xe máy dày đặc kiểu đô thị châu Á.

| Loại sai | Hậu quả | Mức nguy hiểm |
|---|---|---|
| Bỏ sót người (đi bộ hoặc đang ngồi trên xe) ở gần camera | Xe không phanh | **Cao nhất** |
| Bỏ sót phương tiện thật | Xe không tránh | Cao |
| Gán box cho vật **không thật** (tượng, ma-nơ-canh, poster, đồ chơi, phản chiếu) | Báo động giả, phanh nhầm | Trung bình |
| Sai lớp giữa các loại xe | Ước lượng kích thước, tốc độ sai | Thấp–trung bình |

**Câu hỏi gốc khi phân vân:** *"Nếu vật này đứng trước đầu xe thật ngoài đường, xe có phải tránh nó như một người/xe không?"*
Có → gán (kể cả xe đang đỗ, đang trưng bày, đang được chở trên xe khác). Không → không gán.

**Phép thử lớp / thuộc tính:** *"Mô hình có phải tự đoán ra điều này không?"* Có → **lớp**. Không, chỉ để lọc / phân tích / QC → **thuộc tính**.

---

## 2. Lớp và thuộc tính

### 2.1. Lớp (8 lớp vật + `ignore_region`, mỗi vật thuộc đúng một lớp)

Phân loại xe **theo hình dáng nhìn thấy được trên ảnh**, không theo số chỗ (người gán không đếm được ghế). Số chỗ trong ngoặc chỉ để tham khảo.

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Xe chở người có **nắp capo rõ, nóc thấp** (thường ≤ 9 chỗ): sedan, hatchback, SUV, crossover, wagon, taxi, MPV, xe mui trần. | Sedan, SUV, taxi, xe 7 chỗ, xe cổ đang trưng bày, xe diễu hành chạy được trên đường. | Bán tải → `truck`. Thân một khối, nóc cao → `van`. Xe mô hình/đồ chơi → không gán. |
| `van` | Xe **thân liền khối** (một hộp, capo rất ngắn hoặc không có), **nóc cao ≥ 1,3 lần sedan**, thường có cửa lùa (thường 9–16 chỗ). | Toyota Hiace, Ford Transit, Hyundai Solati, xe thùng kín giao hàng cỡ nhỏ. | Thân dài nhiều ô cửa sổ, có cửa khách giữa thân → `bus`. Bán tải có nắp thùng cao → `truck`. |
| `truck` | Xe có **khoang hàng tách khỏi cabin**: **bán tải / pickup** (thùng hở hoặc có nắp thùng), xe tải nhẹ/nặng, tải thùng kín, xe ben, xe bồn, đầu kéo, **xe chở ô tô**. | Pickup, songthaew (pickup chở khách), xe tải mui bạt, xe tải nhỏ, xe chở ô tô nhiều tầng. | SUV 5 cửa không thùng → `car`. Xe tải bằng đá / mô hình → không gán. |
| `bus` | Xe chở khách **thân dài dạng hộp chữ nhật, nhiều ô cửa sổ chạy dọc thân, có cửa khách** (thường từ ~20 chỗ). | Xe buýt, xe khách, xe giường nằm, minibus Coaster / County. | Hiace / Transit (thân ngắn, đầu nhô) → `van`. |
| `motorcycle` | Xe hai bánh có động cơ (xe số, tay ga, mô tô, xe điện dáng tay ga), **kể cả khi gắn sidecar hoặc kéo thùng hàng**; chỉ tính phần xe. | Xe máy, Vespa, xe điện có sàn để chân, xe độ còn bánh/yên/tay lái thật, xe máy + sidecar. | Xe đạp → `bicycle`. Tuk-tuk → `three_wheeler`. |
| `bicycle` | Xe hai bánh **đạp chân**, không có sàn để chân kiểu tay ga (kể cả xe đạp chở hàng, xe đạp điện dáng xe đạp); chỉ tính phần xe. | Xe đạp, xe đạp bán hàng rong. | Xe điện có sàn để chân → `motorcycle`. Xích lô → `three_wheeler`. |
| `three_wheeler` | Xe ba bánh **thiết kế liền khối** để chở người/hàng, có hoặc không có động cơ. | Tuk-tuk, auto-rickshaw, xe lam, xích lô, xe ba gác. | Xe máy hai bánh + sidecar / thùng kéo → `motorcycle`. |
| `person` | Người thật, nhìn thấy **trực tiếp** (không qua kính xe): đứng, đi, ngồi, hoặc đang ngồi trên xe 2–3 bánh. | Người đi bộ, người bán hàng, người lái/ngồi sau xe máy, xe đạp, xích lô. | Tượng, ma-nơ-canh, người trên poster/tranh/ảnh dán kính, phản chiếu → không gán. Người sau kính xe → không gán. |
| `ignore_region` | **Vùng** (không phải vật) chứa nhiều người/xe quá nhỏ hoặc chồng lấn tới mức không vẽ được từng box; bỏ sót trong vùng không tính lỗi. | Dòng xe máy ở xa, bãi xe máy dày, đám đông chen sát ở xa. | Không dùng để "né" vật to, rõ. Không dùng cho vật không thật. |

**[v1.1 — R6] `bus` hay `car`:** chỉ dựa vào hình dáng nhìn thấy. Thân dài dạng hộp, nhiều ô cửa sổ chạy dọc thân, có cửa khách → `bus`. Có capo rõ, nóc thấp → `car`. Không dựa vào màu sơn, logo hay bối cảnh (ca `img_040`).

**Vật không thuộc lớp nào** (động vật, cọc giao thông, thùng rác, biển báo, xe kéo tay, xe đẩy, xe lăn, tàu hoả / tàu điện, tàu thuyền trong tranh…): **không gán gì**, không dùng `ignore_region`.

### 2.2. Thuộc tính

> CVAT gắn mọi thuộc tính cho mọi lớp (script `make_cvat_labels.py` không tách theo lớp). Thuộc tính nào không áp dụng cho lớp đó thì **để nguyên giá trị mặc định**.

#### `occluded_level` — phần trăm diện tích bị **vật khác** che (không tính phần ra ngoài mép ảnh)

Cách đo: hình dung toàn bộ đường viền của vật (cả phần bị che), ước lượng phần trăm bị che. Mẹo: chia box tưởng tượng làm 4 phần.

| Mức | Phần bị che | Ví dụ chung |
|---|---|---|
| `0` | < 10 % | Xe đứng riêng, thấy trọn. |
| `1` | 10 % – < 40 % | Xe bị chân người lái hoặc cột che một phần; xe sau hàng rào song mảnh. |
| `2` | 40 % – < 70 % | Người ngồi sau bàn; ô tô nằm sau khung xe chở ô tô. |
| `3` | ≥ 70 % nhưng **vẫn nhận ra chắc chắn lớp** | Xe máy gần như bị người lái che hết, còn thấy đèn/gương/đầu xe. |

- Che ≥ 70 % **và không nhận ra lớp** → không vẽ box (cả cụm như vậy → `ignore_region`).
- Bỏ nghĩa "3 = không rõ" của v0: "không chắc" dùng `can_review`, không dùng mức 3.
- Hàng rào song mảnh (nhìn xuyên được, song chiếm < 10 % diện tích vật) → tối đa mức `1`.
- Người lái che xe máy **có tính** là che.
- **[v1.1 — R1]** Chỉ tính phần bị **vật khác** che thật sự; ước lượng trên đường viền **toàn bộ** vật (cả phần bị che).
  **Phân vân giữa hai mức → chọn mức thấp hơn.** Chỉ lên mức khi chắc chắn vượt mốc 10 / 40 / 70 %.
  Lý do: IAA trước calibration chỉ 59,8 % cùng `occluded_level`; trong 123 cặp lệch, Anh chấm cao hơn Lâm ở 101 cặp (lệch có hệ thống do ước lượng %). Nhóm lấy cách chấm của Lâm làm chuẩn.

#### `truncated` — vật bị cắt ở mép ảnh

| Giá trị | Điều kiện |
|---|---|
| `yes` | Box chạm mép ảnh (cách mép ≤ 3 px) **và** vật rõ ràng còn tiếp tục ra ngoài khung hình. |
| `no` | Còn lại (kể cả vật sát mép nhưng thấy trọn). |

**[v1.1 — R7]** Hai điều kiện của `truncated=yes` phải **cùng** đúng: box cách mép ≤ 3 px **và** vật rõ ràng còn tiếp ra ngoài. Vật chạm mép nhưng thấy trọn → `no`.

`truncated` độc lập với `occluded_level`: xe bị cắt mép nhưng không bị che → `truncated=yes`, `occluded_level=0`.

#### `on_vehicle` — **chỉ dùng cho `person`** (lớp khác để mặc định `no`)

| Giá trị | Điều kiện |
|---|---|
| `yes` | Người đang ngồi / đứng **trên bất kỳ phương tiện nào** và được gán box: lái, ngồi sau, khách trên xe 2–3 bánh, người trong xe mui trần, người trên thùng xe tải; hoặc giạng chân qua xe tay cầm ghi-đông. **Kể cả khi xe đang đỗ.** |
| `no` | Đi bộ, đứng, ngồi ghế; **người dắt xe** đi bên cạnh; người đứng cạnh xe đang đỗ. |

**[v1.1 — R7]** Người ngồi trên xe máy/xe đạp **đang đỗ** vẫn `on_vehicle=yes`; người chỉ đứng cạnh, tay vịn xe, không ngồi / không giạng chân → `no`.

Lý do là thuộc tính, không phải lớp: người trên xe vẫn là người, mô hình chỉ cần phát hiện `person`; `on_vehicle` để lọc và phân tích. Tách thành lớp riêng sẽ làm hai người gán dễ lệch lớp ở ca "ngồi trên xe đang đỗ".

#### `can_review` — tick khi (và chỉ khi)

1. Phân vân giữa **hai lớp** cụ thể (ghi rõ hai lớp vào ghi chú).
2. Không chắc vật **thật hay không thật** (tượng, người hoá trang, mô hình lớn).
3. Vật **nhoè chuyển động** hoặc **quá tối** khiến biên box có thể lệch > 10 % chiều cao.
4. Tình huống guideline v1.0 chưa nói tới.

Không tick cho vật chỉ bị che hoặc cắt mép: đã có thuộc tính riêng. Không tick chỉ vì box khó vẽ.

---

## 3. Quy tắc vẽ box

### 3.1. Nguyên tắc chung
1. **Ôm sát phần nhìn thấy**: không đoán phần bị che, không vẽ vượt ra ngoài phần thấy được. Sai lệch cho phép ≤ 2 px mỗi cạnh với vật cao ≥ 50 px.
   **[v1.1 — R3]** Vật cao < 100 px: **phóng to ảnh** (con lăn chuột) trước khi vẽ, kéo từng cạnh tới điểm ngoài cùng của phần nhìn thấy (đỉnh đầu/mũ, mũi giày, mép bánh xe, gương). Không quy tắc mới; lỗi IoU thấp (126 ca, IoU 0,75–0,84, chủ yếu `person`/`motorcycle`) là do vẽ chưa sát, không ai vẽ to hơn có hệ thống.
2. Mỗi vật **một box**; không gộp hai vật vào một box (trừ `ignore_region`).
3. Box tính cả phụ kiện **đang gắn trên** vật: mũ bảo hiểm, nón lá, ba lô đang đeo, áo mưa trùm (người); gương, giá chở hàng, nắp thùng, khung chở xe (xe). **Không** tính ăng-ten, dây buộc hàng thò ra.

### 3.2. Vật nhỏ
- Vật có box cao **< 20 px** (`min_box_height_px`) → không vẽ từng vật.
- Vùng có **≥ 3 vật nhỏ** như vậy nằm sát nhau → **một** `ignore_region` bao cả cụm. Chỉ 1–2 vật lẻ → bỏ qua.

### 3.3. Vật bị che / bị cắt mép
- Bị che: vẽ phần thấy được, gán `occluded_level`. Vật bị một vật mảnh (cột điện, thân cây) chia làm hai mảnh → **một box** bao cả hai mảnh.
- Bị cắt mép: box dừng ở mép ảnh, `truncated=yes`. Phần thấy < 10 % vật và không nhận ra lớp từ phần đó (ví dụ chỉ lộ hai gương xe) → không gán.

### 3.4. Người và xe (một vật có nhiều phần)
- Người lái/ngồi trên xe máy, xe đạp, xích lô, tuk-tuk: **hai box riêng**: `person` (`on_vehicle=yes`) và box xe. Xe chở 2–3 người → mỗi người một box `person`. Các box được phép chồng nhau.
- Box `person` gồm toàn bộ người nhìn thấy (cả chân đặt trên xe). Box xe gồm toàn bộ xe nhìn thấy; phần xe bị người che nằm trong đường viền xe vẫn thuộc box xe.
- **Người trong xe kín** (ô tô, van, bus, cabin xe tải) **và người sau kính chắn gió** tuk-tuk / auto-rickshaw → **không gán**. Người thấy **trực tiếp** (xe mui trần, sườn hở của tuk-tuk) → gán `person`.
- **Hàng hoá:** box xe **chỉ gồm thân xe** (khung, cabin, thùng, nắp thùng, khung chở xe). Hàng chất cao vượt thân xe và vật trang trí đặt trên xe (tượng, mô hình) **không** tính vào box xe.
- **[v1.1 — R4]** Nhắc lại cho `bicycle`: box **chỉ gồm thân xe** (bánh, khung, ghi-đông, yên, giỏ gắn liền). Hàng chở, khay, bao tải buộc trên xe **không** tính, kể cả khi vượt ít.
- **Đồ cầm / gánh / vác** (đòn gánh, quang gánh, ống dài, túi xách): **không** tính vào box người.
- **Xe chở ô tô / xe kéo rơ-moóc:** **một** box `truck` bao đầu kéo + rơ-moóc / khung chở khi đang nối. **Mỗi ô tô đang được chở** là một box `car` riêng (`occluded_level` theo phần bị khung che).
- **Xe máy gắn sidecar hoặc kéo thùng hàng:** **một** box `motorcycle` bao cả phần gắn kèm.
- Người ngồi / đứng trên thùng xe tải → `person` (`on_vehicle=yes`), box riêng.

### 3.5. Vật không thật → **không gán gì** (kể cả `ignore_region`)
- Tượng, đài tưởng niệm, ma-nơ-canh (kể cả tượng người cưỡi ngựa, tượng động vật, xe tạc bằng đá).
- Hình in: poster, biển quảng cáo, tranh tường, ảnh dán kính xe, màn hình.
- Đồ chơi, mô hình thu nhỏ, thú bông, xe mô hình đặt trên xe khác.
- **Phản chiếu**: trong gương chiếu hậu, trên kính cửa hàng, trên mặt đường ướt.
- **Ngoại lệ, vẫn là vật thật → gán:** xe có hình dáng lạ / như đồ chơi nhưng **chạy được trên đường** (có biển số, có người lái, bánh chạm đất); xe độ trang trí còn bánh, yên, tay lái thật; xe thật đang trưng bày / đỗ.
- Người hoá trang / cosplay: chỉ gán `person` khi thấy rõ là người thật (da, mặt, tay chân); không chắc → không gán và tick `can_review` vào vật gần nhất hoặc ghi chú ảnh.

### 3.6. Xe chủ (ego vehicle)
- Phần xe mà camera đang ngồi trong / trên (nắp capo, thân xe, gương, tay lái thấy từ góc người lái) → **không gán**.
- Xe đỗ sát camera nhưng camera **không ở trong xe** (chụp từ ngoài, từ phía sau thùng) → **gán** bình thường, thường kèm `truncated=yes`.

### 3.7. Đám đông và vật dày đặc
- **[v1.1 — R2] Quy tắc quyết định cho từng vật trong cảnh đông** (áp trước các dòng dưới):
  1. Vật cao **≥ 20 px** và thấy **≥ 1/2 thân** → **vẽ box riêng**, kể cả nằm giữa cụm.
  2. Vật không đạt (1) → không vẽ riêng; nếu nằm trong cụm **≥ 3** vật như vậy → bao chung bằng **một** `ignore_region`; vật lẻ → bỏ qua.
  3. Không vẽ box riêng **bên trong** `ignore_region`, không để `ignore_region` phủ lên vật đạt (1).
  Lý do: 103 ca bỏ sót / thừa tập trung ở `img_008`, `021`, `032`, `034`; hai người cùng lệch về chỗ dừng vẽ từng vật (Anh dùng 25 `ignore_region`, Lâm 17).
- Vẽ `ignore_region` khi có **≥ 5 vật cùng lớp chồng lấn** mà **không vẽ được** từng box chắc chắn (đa số che ≥ 40 % hoặc cao < 20 px).
- Vật **ở rìa trước** cụm, cao ≥ 20 px và `occluded_level ≤ 2` → **vẫn vẽ box riêng**, kể cả khi nằm kề `ignore_region`.
- Đám đông còn **tách được từng người** (cao ≳ 50 px, che ≤ mức 2) → vẽ từng người, **không** dùng `ignore_region`.
- `ignore_region` vẽ sát cụm, không phủ cả ảnh, không phủ lên vật lớn đã có box.

### 3.8. Nhoè, tối, mưa
- Nhận ra chắc chắn lớp → vẽ box quanh **phần thân đậm nhất**, không kéo theo vệt mờ đuôi; tick `can_review` nếu biên có thể lệch > 10 %.
- Không nhận ra lớp (quá tối, quá nhoè) → không vẽ; rõ là có cụm người/xe (≥ 3) → `ignore_region`.
- **[v1.1 — R5]** Sau calibration, ca đã có quy tắc thì **bỏ tick** `can_review`; chỉ giữ tick cho ca vẫn chưa quyết được. Ảnh nhoè/tối: tiêu chí "nhận ra lớp" = nói được lớp mà không cần đoán từ bối cảnh. (80 ca `can_review`, nhiều nhất ở `img_034`, `014`, `031`.)

---

## 4. Ca khó

> Các ca dưới đây được ghi khi **xem** 40 ảnh ở Pha 1 (chưa gán box), áp theo quy tắc v1.0. Nếu khi gán thấy thực tế khác mô tả, **làm theo quy tắc chung ở mục 2–3**, tick `can_review`, đem ra calibration. Quy tắc luôn ưu tiên hơn ví dụ.

| Ảnh | Tình huống | Quyết định (v1.0) | Lý do / quy tắc |
|---|---|---|---|
| img_001 | Xe tải nhỏ bị cắt mép phải; nhiều người ngồi sau bàn; banner có hình | `truck` (`truncated=yes`); mỗi người ngồi là `person` (`occluded_level` 1–2 theo phần bị bàn/người che); banner không gán | Thùng tách cabin → truck. Banner là hình in (3.5). |
| img_002 | Xe chở ô tô mang nhiều xe con; người nhỏ bên phải | Một box `truck` bao đầu kéo + khung; mỗi xe con một box `car` (thường `occluded_level` 1–2 do khung); người cao ≥ 20 px → `person` | 3.4: xe được chở vẫn là xe thật. |
| img_003 | Người gánh đòn gánh; người đứng cạnh xe đạp; bãi xe máy dày phía xa | `person` không gồm quang gánh; người đứng cạnh xe (không giạng chân) → `on_vehicle=no`; `bicycle` riêng; bãi xe xa → `ignore_region` | 3.4 đồ cầm/gánh; 3.7. |
| img_004 | 2 tuk-tuk; tài xế trái sau kính chắn gió, tài xế phải thấy trực tiếp từ sườn hở | 2 box `three_wheeler`; chỉ tài xế phải là `person` (`on_vehicle=yes`) | 3.4: sau kính → không gán. |
| img_005 | Cận cảnh người đi xe máy, xe gần như bị người che; van phía sau | Mỗi người `person` `on_vehicle=yes` (`truncated` nếu chạm mép); xe máy còn nhận ra (đầu, gương, đèn) → `motorcycle` `occluded_level=3`; van → `van` | Không bỏ xe chỉ vì bị che nhiều nếu còn nhận ra. |
| img_007 | Kho tối; pickup có thùng hộp; xe tải cắt mép phải | Pickup → `truck`; xe tải → `truck` (`truncated=yes`) | Bán tải là truck (2.1). |
| img_009 | Minibus, khách nhìn qua cửa kính; chó; người trên ban công | Minibus → `bus`; khách qua kính → không gán; chó → không gán; người ban công cao ≥ 20 px → `person` | Thân dài, cửa khách → bus. |
| img_010 | Người ngồi trên xe máy đỗ; xe đạp chở chuối | `person` `on_vehicle=yes`; xe đạp → `bicycle`, box không gồm khay chuối vượt thân xe | `on_vehicle` không phụ thuộc xe chạy hay đỗ; 3.4 hàng hoá. |
| img_011 | Nhân vật hoá trang (Predator); xe máy độ bằng sắt vụn | Nhân vật: không gán, `can_review` nếu thấy da/tay người thật; xe độ có bánh, yên, ghi-đông chạm đất → `motorcycle` | 3.5 ngoại lệ và quy tắc cosplay. |
| img_012 | Pickup chiếm góc dưới phải, camera ở sau thùng; SUV; xe tải phía trước | Pickup → `truck` `truncated=yes`; SUV → `car`; xe tải → `truck` | Không có dấu hiệu camera trong xe → không phải ego (3.6). |
| img_013 | Đêm mưa; tượng rồng; xe con nhỏ ở xa | Người đi bộ → `person`; tượng không gán; xe xa < 20 px → `ignore_region` nếu ≥ 3, không thì bỏ qua | 3.2, 3.5. |
| img_014 | Hai người đi bộ rõ, xe máy nhoè chuyển động xung quanh | 2 `person`; xe/người nhoè nhận ra được → box phần đậm, `can_review` | 3.8. |
| img_015 | Hai xe con cắt mép; xe phía sau có vệt mờ; phản chiếu trên đường ướt | 2 `car` `truncated=yes`; xe nền box phần đậm, `can_review`; phản chiếu không gán | 3.5, 3.8. |
| img_016 | Tuk-tuk, van, pickup, Vespa chở hàng, người cắt mép; đầu người mờ góc trái dưới | `three_wheeler`; van → `van`; pickup → `truck`; Vespa → `motorcycle` + `person` `on_vehicle=yes`; người cắt mép `truncated=yes`; đầu người không nhận ra → không gán | 3.3. |
| img_017 | Tượng người cưỡi ngựa | Không gán gì | Tượng. |
| img_018 | Biển quảng cáo có ảnh người; xe sau hàng rào song; chụp qua kính xe | Ảnh người không gán; xe → `car`/`truck` theo dáng, `occluded_level=1` do song rào | Rào mảnh tối đa mức 1. |
| img_019 | Xe diễu hành có biển số, có người lái; thú bông; đám đông sau rào; đầu người nhoè tiền cảnh | Xe → `car`; người lái thấy trực tiếp → `person` `on_vehicle=yes`; thú bông không gán; đám đông → `ignore_region`, người hàng đầu rõ vẽ riêng; đầu người tiền cảnh → `person` `truncated=yes`, `can_review` | Xe chạy được trên đường = xe thật (3.5). Người lái → `on_vehicle=yes`. |
| img_020 | Gương chiếu hậu phản chiếu xe phía sau + thân xe chủ | Không gán gì | Phản chiếu và ego. |
| img_021 | Dòng xe máy cực dày lúc chiều tối | Phần gần: từng `person` + `motorcycle`; phần xa (< 20 px, chồng lấn) → một `ignore_region`; ô tô/xe buýt rõ → `car`/`bus` | 3.7. |
| img_022 | Ảnh đen trắng, xe máy gắn sidecar, người ngồi | Một box `motorcycle` bao cả sidecar; người → `person` `on_vehicle=yes` | 3.4 sidecar. |
| img_023 | Xích lô có người đạp; người ngồi vỉa hè | Xích lô → `three_wheeler`; người đạp → `person` `on_vehicle=yes`; người ngồi vỉa hè → `person` `on_vehicle=no` | Xích lô là xe 3 bánh liền khối. |
| img_024 | Bảo tàng xe; xe mô hình trên nóc xe khác | Các xe thật → `car`; mô hình trên nóc không gán; xe cắt mép `truncated=yes` | Xe trưng bày là xe thật; mô hình không chạy được. |
| img_025 | Xe máy kéo thùng hàng; người ngồi ghế bãi biển; người ở xa | Xe máy + thùng → một `motorcycle`; người lái `on_vehicle=yes`; người ngồi ghế `on_vehicle=no`; người xa < 20 px → `ignore_region` nếu ≥ 3 | 3.2, 3.4. |
| img_026 | Đôi nam nữ trên xe máy nhoè; tranh tường | 2 `person` `on_vehicle=yes` + 1 `motorcycle`, `can_review` nếu biên nhoè; tranh không gán | 3.5, 3.8. |
| img_027 | Xe pickup tạc bằng đá ở nghĩa trang | Không gán | Đài tưởng niệm. |
| img_028 | Pickup thật chở tượng ngựa; SUV phía sau bị che | Pickup → `truck`, box chỉ thân xe (không gồm tượng); SUV → `car` `occluded_level=2` | 3.4 hàng hoá; tượng không gán. |
| img_029 | Người đi xe điện chở ống thép dài; người giạng chân trên xe đạp | Xe điện dáng tay ga → `motorcycle`; xe đạp → `bicycle`; 2 người `on_vehicle=yes`; ống thép không tính vào box nào | 3.4 đồ cầm/chở. |
| img_030 | Bãi xe máy dày; poster người; bảo vệ | Xe hàng đầu vẽ từng chiếc; phần sâu → `ignore_region`; bảo vệ → `person`; poster không gán | 3.7. |
| img_031 | Đêm mưa; xe, xe buýt, xe máy, người đi bộ; phản chiếu; tranh trên nhà | `car`, `bus`, `motorcycle`, `person` cho vật ≥ 20 px; phản chiếu và tranh không gán | 3.2, 3.5. |
| img_032 | Khoảng 35 người đợi xe buýt, chồng lấn; xe cắt mép; xe đỗ phía sau | Vẽ **từng người** (đủ lớn, tách được) với `occluded_level` riêng; xe cắt mép `truncated=yes`; xe phía sau → `car` theo mức che | 3.7: không lạm dụng `ignore_region`. |
| img_033 | Ma-nơ-canh, ảnh người mẫu, phản chiếu xe trên kính | Không gán gì | Vật không thật / phản chiếu. |
| img_035 | Auto-rickshaw chở bao tải cao gấp đôi thân xe; tài xế sau kính chắn gió | `three_wheeler`, box chỉ thân xe; tài xế → không gán | 3.4 hàng hoá, người sau kính. |
| img_036 | Xe tải nhỏ mui bạt; xe máy đỗ; poster người trên kính | `truck`; xe máy đỗ → `motorcycle`; poster không gán | Thùng tách cabin. |
| img_037 | Pickup có nắp thùng cao trông giống van; xe buýt; người đi bộ | Pickup → `truck`; xe buýt → `bus` (`truncated`/`occluded` theo mức); người → `person` | Cabin và thùng tách rời → không phải van. |
| img_038 | Tủ kính đồ chơi: xe mô hình, thú bông | Không gán gì | Đồ chơi. |
| img_039 | Phố có xe máy đỗ, người đi bộ, xe đạp, xích lô nhỏ ở xa | Vật ≥ 20 px vẽ từng cái theo lớp; vật < 20 px bỏ qua hoặc `ignore_region` nếu ≥ 3 | 3.2. |
| img_040 | Người đội mũ bảo hiểm cận cảnh (chỉ thấy 2 gương xe máy ở đáy); taxi; tuk-tuk; SUV; xe buýt; ảnh dán kính taxi | Người → `person` `truncated=yes`, `on_vehicle=yes`; 2 gương không gán; taxi → `car`; tuk-tuk → `three_wheeler`; SUV → `car`; xe buýt → `bus`; ảnh dán không gán | 3.3: phần xe thấy < 10 %, không nhận ra lớp. |

Ca gặp khi gán mà không có trong bảng và quy tắc chưa trả lời: tick `can_review`, ghi chú ngắn, báo nhóm trưởng. **Không tự đoán.**

---

## 5. QC và phiên bản

### 5.1. Ngưỡng áp dụng (theo `taxonomy.json` → `rules`, không đổi)

| Đại lượng | Ngưỡng |
|---|---|
| Box nhỏ nhất được vẽ từng vật | cao ≥ 20 px |
| IoU giữa hai người gán (box cao ≥ 50 px) | ≥ 0,85 |
| IoU giữa hai người gán (box cao < 50 px) | ≥ 0,70 |
| IAA cả tập | IoU trung bình ≥ 0,85 **và** cùng lớp ≥ 95 % |
| Ghép cặp box khi so sánh | IoU ≥ 0,5 |
| Tỉ lệ lỗi theo ảnh để Release | ≤ 2 % (luôn ghi mẫu số, ví dụ "1/40 ảnh") |

### 5.2. Ai quyết
- Ca mơ hồ trong lúc gán: tick `can_review` + ghi chú, **không sửa guideline giữa Pha 3**.
- Ca bất đồng sau khi đo IAA: hai thành viên cùng xem ảnh ở buổi calibration; không thống nhất được thì **nhóm trưởng** chốt, ghi một dòng vào `calibration_decisions.csv`.
- Quyết định là **quy tắc mới** → ghi vào `guideline_v1.1_calibrated.md`; cần đổi lớp/thuộc tính thì sửa `taxonomy.json` và tăng `version`.

### 5.3. Lịch sử thay đổi

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản khởi đầu của giảng viên: 5 lớp vật + `ignore_region`, 3 thuộc tính, chưa có ca khó | — |
| v1.0 | Thêm lớp `bus`, `bicycle`, `three_wheeler` | Xe buýt, xe đạp, tuk-tuk/xích lô không có lớp (`img_004`, `009`, `023`, `029`, `035`) |
| v1.0 | Định nghĩa car / van / truck / bus theo hình dáng; bán tải → `truck` | Pickup, van, minibus dễ nhầm (`img_007`, `009`, `012`, `037`) |
| v1.0 | Thêm thuộc tính `on_vehicle` cho `person`; người + xe hai box; người sau kính không gán | Nhiều người ngồi trên xe, v0 không nói gán mấy box (`img_004`, `005`, `010`, `035`) |
| v1.0 | `occluded_level` có ngưỡng 10 / 40 / 70 %; bỏ nghĩa "3 = không rõ" | v0 không có ngưỡng đo được (`img_001`, `002`, `005`, `018`) |
| v1.0 | `truncated` có điều kiện đo (≤ 3 px tới mép + vật còn tiếp) | v0 không nói thế nào là "bị cắt" (`img_015`, `016`, `040`) |
| v1.0 | Quy tắc vật không thật, phản chiếu, hình in, ego; ngoại lệ xe chạy được | Tượng, ma-nơ-canh, poster, đồ chơi, gương (`img_017`, `019`, `020`, `027`, `033`, `038`) |
| v1.0 | Vật nhỏ < 20 px; cụm ≥ 3 vật nhỏ hoặc ≥ 5 vật chồng lấn → `ignore_region` | Cảnh xe máy dày, đám đông (`img_019`, `021`, `030`, `032`) |
| v1.0 | Hàng hoá không tính vào box xe; sidecar/thùng kéo gộp vào `motorcycle`; xe chở ô tô | `img_002`, `022`, `025`, `028`, `035` |
| v1.0 | Nhoè / tối / mưa và tiêu chí tick `can_review` | `img_013`, `014`, `015`, `026` |
| v1.1 | R1: `occluded_level` chỉ tính vật khác che, phân vân → mức thấp; chuẩn theo cách chấm của Lâm | 123 cặp lệch mức (Anh cao hơn ở 101); IAA `occluded_level` 59,8 % |
| v1.1 | R2: quy tắc vẽ riêng / `ignore_region` trong cảnh đông (≥ 20 px và thấy ≥ 1/2 thân) | 103 ca bỏ sót/thừa; `img_008`, `021`, `032`, `034` |
| v1.1 | R3: hướng dẫn vẽ sát (phóng to khi vật < 100 px), không đổi quy tắc | 126 ca IoU thấp; IoU TB 0,836 < 0,85 |
| v1.1 | R4: nhắc lại box `bicycle` chỉ thân xe | 7 ca IoU thấp của `bicycle` |
| v1.1 | R5: tiêu chí nhận ra lớp khi nhoè/tối; bỏ tick `can_review` sau khi chốt | 80 ca `can_review`; `img_014`, `031`, `034` |
| v1.1 | R6: `bus`/`car` chỉ theo hình dáng | 1 ca sai lớp `img_040` |
| v1.1 | R7: làm rõ điều kiện `truncated` và `on_vehicle` | 8 ca lệch thuộc tính khác |

---

## 6. Bất đồng giữa hai bản cá nhân và quyết định

| # | Vấn đề | Anh | Lâm | Quyết định v1.0 | Lý do |
|---|---|---|---|---|---|
| 1 | Người trên xe | Lớp riêng `rider` | `person` + thuộc tính `on_vehicle` | `person` + `on_vehicle` | Phép thử lớp/thuộc tính; ca "ngồi trên xe đang đỗ" làm `rider`/`person` dễ lệch lớp, kéo đồng thuận lớp dưới 95 %. |
| 2 | Bán tải | `car` | `truck` | `truck` | Đúng định nghĩa "khoang hàng tách cabin" của cả hai bản; tránh ngoại lệ. |
| 3 | Ranh giới car / van / bus | Theo số chỗ (≤ 7 / 9–16 / ~20+) | car ≤ 9; van nóc cao ≥ 1,3 sedan; bus ≥ 10 chỗ, thân dài | Theo **hình dáng**; số chỗ chỉ tham khảo | Người gán không đếm được ghế trên ảnh. |
| 4 | Xe máy gắn sidecar / kéo thùng | `three_wheeler` | `motorcycle` (một box) | `motorcycle` | `three_wheeler` chỉ cho xe ba bánh thiết kế liền khối. |
| 5 | Ngưỡng `occluded_level` | 5 / 35 / 70 % | 10 / 40 / 70 % | 10 / 40 / 70 % | Mắt người khó phân biệt 0 % với 5 %; thêm quy tắc rào song mảnh tối đa mức 1. |
| 6 | `truncated` | ≥ 10 % vật ra ngoài khung | Box ≤ 3 px tới mép và vật còn tiếp | Theo Lâm | Đo được trực tiếp trên CVAT. |
| 7 | Hàng chất trên xe | Hàng dính liền tính vào box xe | Chỉ thân xe | Chỉ thân xe | Dáng box ổn định hơn nên IoU giữa hai người cao hơn. |
| 8 | Box xe chở ô tô | `truck` bao cả xe đang chở | `truck` bao đầu kéo + khung | Đầu kéo + khung | Nhất quán với #7; xe được chở đã có box `car` riêng. |
| 9 | Đám đông | Không tách được → `ignore_region` | ≥ 5 vật chồng lấn không vẽ được; vật rìa trước vẫn vẽ | Theo Lâm, giữ thêm quy tắc cụm ≥ 3 vật nhỏ < 20 px | Có ngưỡng cụ thể. |
| 10 | Xe giả tưởng / trang trí | Không gán | Gán nếu chạy được trên đường | Gán nếu chạy được (biển số, người lái, bánh chạm đất) | Kiểm chứng được trên ảnh. |
| 11 | Người trên tuk-tuk | Mọi người thấy được đều gán | Sau kính chắn gió → không gán | Theo Lâm | Khớp quy tắc "qua kính → không gán". |
| 12 | Group id cho cụm đếm được | Đã bỏ trong bản cá nhân | Không có | Không dùng | Script QC không đọc group id. |
| 13 | Tàu hoả / tàu điện | Hỏi có cần lớp không | Không nhắc | Không gán | Ngoài mục tiêu người và phương tiện đường bộ. |

---

## 7. Tóm tắt calibration (v1.0 → v1.1)

- IAA trước calibration (`submission/qc/iaa_summary.md`, mẫu số **306 cặp box ghép**, 40 ảnh, 2 người): IoU TB **0,836** (ngưỡng 0,85) → **chưa đạt**; cùng lớp **99,7 %** (305/306, ngưỡng 95 %) → đạt.
- 441 ca bất thường trên **35/40 ảnh** bị cờ: `sai_thuoc_tinh` 131, `iou_thap` 126, `bo_sot_thua` 103, `co_can_review` 80, `sai_lop` 1.
- Mỗi ca có một dòng trong `submission/qc/calibration_decisions.csv`, cột `quy_tac_ghi_vao_guideline` trỏ tới mã R1–R7 ở trên. Người chốt: nhóm trưởng Trần Tuấn Anh.
- Phân loại nguyên nhân: **guideline mơ hồ** (cả hai cùng lệch / lệch có hệ thống) → R1, R2, R5, R7 là quy tắc mới. **Người gán chưa nắm / vẽ chưa sát** → R3, R4 (không đổi quy tắc, chỉ nhắc). **Một ca sai lớp** → R6.
- Taxonomy không đổi (không thêm/bớt lớp hay thuộc tính), nên `taxonomy.json` giữ `v1.0`.
