# Guideline gán nhãn — v1 (cá nhân) — 2A202603227 - Doãn Tùng Lâm | Nhóm Just2Men

- Phiên bản: v1-cá-nhân (viết lại từ `guideline_v0_starter.md` sau khi xem đủ 40 ảnh `img_001`–`img_040`)
- Ngày: 2026-11-16
- Người viết: Doãn Tùng Lâm (2A202603227) · Người duyệt: cả nhóm ở Pha 2
- Loại nhãn: bounding box trên ảnh đường phố · Công cụ: CVAT, xuất COCO 1.0

> **[CHƯA CHỐT]** = quyết định cá nhân của mình, cần đem ra họp Pha 2 để thống nhất.
> Mọi con số trong file này (%, px) là ngưỡng để hai người đọc ra **cùng một** nhãn.

---

## 1. Mục tiêu

Nhãn dùng để huấn luyện mô hình **phát hiện người và phương tiện có thật đang có mặt trên đường**
(camera giao thông, xe tự lái), chủ yếu bối cảnh đô thị châu Á: xe máy dày đặc, xe ba bánh, người bán hàng rong.

| Loại sai | Hậu quả | Mức nguy hiểm |
|---|---|---|
| Bỏ sót người (đi bộ hoặc đang ngồi trên xe máy/xe đạp) ở gần camera | Xe không phanh | **Cao nhất** |
| Bỏ sót phương tiện thật | Xe không tránh | Cao |
| Gán box cho vật **không thật** (tượng, ma-nơ-canh, poster, đồ chơi, phản chiếu) | Mô hình phanh/báo động giả | Trung bình |
| Sai lớp giữa các loại xe (car / van / truck) | Dự đoán kích thước, tốc độ sai | Thấp–trung bình |

**Câu hỏi gốc khi phân vân:** *"Nếu vật này đứng trước đầu xe thật ngoài đường, xe có phải tránh nó như một người/xe không?"*
Có → gán box (kể cả xe đang đỗ, đang trưng bày, đang được chở trên xe khác). Không → không gán.

---

## 2. Lớp và thuộc tính

### 2.1. Lớp (mỗi vật thuộc đúng một lớp)

v0 chỉ có 5 lớp vật; 40 ảnh có rất nhiều xe buýt, xe đạp, xe ba bánh (tuk-tuk, xích lô, auto-rickshaw) mà v0 không nói gán gì.
Mình đề xuất **thêm 3 lớp** `bus`, `bicycle`, `three_wheeler` **[CHƯA CHỐT]** vì đây là vật mô hình phải tự phân biệt (phép thử: *"mô hình có phải đoán ra không?"* → có → lớp).

| Lớp | Định nghĩa (một câu) | Ví dụ trong 40 ảnh | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Xe chở người ≤ 9 chỗ, có nắp capo, gầm thấp: sedan, hatchback, SUV, crossover, wagon, taxi, xe mui trần. | sedan đen `img_023`, Mazda SUV `img_012`, taxi `img_040`, xe trưng bày `img_024`, xe diễu hành chạy được `img_019` | Pickup → `truck`. Xe thân liền khối nóc cao → `van`. Xe mô hình/đồ chơi → không gán (`img_038`). |
| `van` | Xe thân liền khối (một hộp hoặc capo rất ngắn), nóc cao rõ hơn ô tô con (≈ ≥ 1,3 lần chiều cao sedan), thường có cửa lùa, ≤ 16 chỗ. | Toyota Hiace `img_005`, `img_016` | Minibus dài có cửa khách giữa thân → `bus` (`img_009`). Pickup có nắp thùng cao → `truck` (`img_037`). |
| `truck` | Xe có **khoang hàng tách khỏi cabin**: pickup (thùng hở hoặc có nắp thùng), xe tải nhẹ/nặng, xe tải thùng kín, xe chở ô tô. | Suzuki tải nhỏ `img_001`, xe chở ô tô `img_002`, Isuzu + pickup có thùng `img_007`, pickup `img_012`, `img_028`, Veryca `img_036`, pickup nắp thùng `img_037` | Xe tải bằng đá ở nghĩa trang `img_027` → không gán. SUV 5 cửa không có thùng → `car`. |
| `bus` **[mới]** | Xe chở khách ≥ 10 chỗ, thân dài nhiều ô cửa sổ, có cửa khách: xe buýt, xe khách, minibus (Coaster/County). | minibus `img_009`, xe buýt `img_031`, `img_037`, `img_040` (nền) | Van Hiace → `van`. Xe songthaew (pickup chở khách) → `truck`. |
| `motorcycle` | Xe hai bánh có động cơ (xe số, tay ga, xe điện dáng tay ga), **kể cả khi gắn thùng bên (sidecar) hoặc kéo xe lôi**. | `img_006`, `img_010`, `img_021`, `img_030`, sidecar `img_022`, xe máy kéo thùng hàng `img_025`, xe điện `img_029`, xe độ `img_011` | Xe đạp → `bicycle`. Tuk-tuk (thân liền 3 bánh) → `three_wheeler`. |
| `bicycle` **[mới]** | Xe hai bánh đạp chân (kể cả xe đạp chở hàng), không có sàn để chân kiểu tay ga. | `img_003`, `img_006`, xe hàng rong `img_010`, `img_029`, `img_034`, `img_039` | Xe điện có sàn để chân → `motorcycle` (`img_029`). |
| `three_wheeler` **[mới]** | Xe ba bánh thiết kế liền khối để chở người/hàng: tuk-tuk, auto-rickshaw, xích lô. | tuk-tuk `img_004`, `img_016`, `img_040`, auto-rickshaw `img_035`, xích lô `img_023`, `img_039` | Xe máy + sidecar → `motorcycle`. |
| `person` | Người thật, nhìn thấy trực tiếp (không qua kính xe), đứng/đi/ngồi/đang ngồi trên xe. | người đi bộ `img_014`, `img_034`; người ngồi quán `img_001`; người lái/ngồi sau xe máy `img_005`, `img_026` | Tượng `img_017`, ma-nơ-canh `img_033`, người trên poster `img_018`, `img_030`, `img_036`, ảnh dán kính taxi `img_040` → không gán. |
| `ignore_region` | **Vùng** (không phải vật) chứa nhiều người/xe quá nhỏ hoặc chồng lấn tới mức không vẽ được từng box; bỏ sót trong vùng này không tính lỗi. | dòng xe máy xa `img_021`, bãi xe máy sâu `img_030`, đám đông sau rào `img_019` | Không dùng `ignore_region` để "né" vật to, rõ. |

**Vật không thuộc lớp nào** (chó `img_009`, tượng ngựa `img_028`, cọc giao thông `img_004`/`img_032`, tàu thuyền trên tranh `img_026`, thùng rác…): **không gán gì**, không dùng `ignore_region`.

**Nếu nhóm không thêm 3 lớp mới** (phương án dự phòng **[CHƯA CHỐT]**): `bus` → `van` nếu ≤ 16 chỗ, còn lại không gán; `bicycle`, `three_wheeler` → không gán và tick `can_review`. Mình **không khuyến khích** phương án này vì sẽ dạy mô hình rằng tuk-tuk/xe đạp là "nền".

### 2.2. Thuộc tính

#### `occluded_level` — mức bị **vật khác** che (không tính phần ra ngoài mép ảnh)

Cách đo: hình dung toàn bộ đường viền của vật (kể cả phần bị che), ước lượng **phần trăm diện tích bị vật khác che**.

| Mức | Phần bị che | Ví dụ |
|---|---|---|
| `0` | < 10 % | sedan `img_023`, pickup `img_028` |
| `1` | 10 % – < 40 % | xe máy bị chân người lái che một phần `img_010`; xe sau hàng rào song mảnh `img_018` |
| `2` | 40 % – < 70 % | người ngồi sau bàn quán `img_001`; xe con trên xe chở ô tô bị khung che `img_002` |
| `3` | ≥ 70 % nhưng **vẫn nhận ra chắc chắn lớp** | xe máy gần như bị người lái che hết `img_005` |

- Che ≥ 70 % **và không nhận ra lớp** → không vẽ box (nếu là cả cụm → `ignore_region`).
- v0 ghi "3 là không rõ": bỏ nghĩa này. "Không chắc" dùng `can_review`, không dùng mức 3.
- Hàng rào song mảnh (song chiếm < 10 % diện tích vật, nhìn xuyên qua được) tối đa mức `1`.
- Người lái che xe máy **có tính** là che.

#### `truncated` — vật bị cắt ở mép ảnh

| Giá trị | Điều kiện |
|---|---|
| `yes` | Box chạm mép ảnh (cách mép ≤ 3 px) **và** vật rõ ràng còn tiếp tục ra ngoài khung hình. |
| `no` | Còn lại (kể cả vật nằm sát mép nhưng thấy trọn). |

`truncated` độc lập với `occluded_level`: xe đỏ `img_015` bị cắt mép trái → `truncated=yes`, `occluded_level=0`.

#### `on_vehicle` — chỉ cho `person` **[CHƯA CHỐT, thuộc tính mới]**

| Giá trị | Điều kiện |
|---|---|
| `yes` | Người đang ngồi trên xe (lái hoặc ngồi sau), hoặc đứng giạng chân qua xe tay cầm ghi-đông — kể cả khi xe đang đỗ (`img_010`, `img_029`). |
| `no` | Đi bộ, đứng, ngồi ghế; người dắt xe đi bên cạnh (`img_003`). |

Lý do: người trên xe di chuyển nhanh và theo hướng xe, khác người đi bộ; nhưng mô hình không cần lớp riêng → làm thuộc tính để lọc/phân tích.

#### `can_review` — tick khi (và chỉ khi) gặp một trong các trường hợp

1. Phân vân giữa **hai lớp** cụ thể (ghi rõ hai lớp vào ghi chú).
2. Không chắc vật **thật hay không thật** (tượng/người hóa trang/mô hình).
3. Vật bị **nhoè chuyển động** hoặc **tối** khiến biên box có thể lệch > 10 % chiều cao.
4. Ca nằm trong danh sách **[CHƯA CHỐT]** của mục 4.

Không tick `can_review` cho vật chỉ đơn thuần bị che hoặc cắt mép — đã có thuộc tính riêng.

---

## 3. Quy tắc vẽ box

### 3.1. Nguyên tắc chung
1. **Ôm sát phần nhìn thấy** (modal box): không đoán phần bị che, không vẽ box vượt ra ngoài phần thấy được. Sai lệch cho phép ≤ 2 px mỗi cạnh với vật cao ≥ 50 px.
2. Mỗi vật **một box**; không gộp hai vật vào một box (trừ `ignore_region`).
3. Vật có box cao **< 20 px** → không vẽ từng vật. Nếu vùng đó có ≥ 3 vật nhỏ như vậy → vẽ một `ignore_region` bao quanh; nếu chỉ 1–2 vật lẻ → bỏ qua.
4. Box tính cả phụ kiện **đang gắn trên** vật: mũ bảo hiểm, nón lá, ba lô đang đeo (người); gương, giá chở hàng, nắp thùng, khung chở xe (xe).

### 3.2. Vật bị che / cắt mép
- Bị che: vẽ phần thấy được, gán `occluded_level` theo mục 2.2. Nếu vật bị chia thành hai mảnh (ví dụ cột điện chắn giữa), **một box** bao cả hai mảnh.
- Bị cắt mép: box dừng ở mép ảnh, `truncated=yes`. Vật thấy < 10 % và không nhận ra lớp chỉ từ phần đó (ví dụ chỉ thấy 2 gương xe máy ở đáy `img_040`) → không gán.

### 3.3. Người và xe (một vật có nhiều phần)
- Người lái/ngồi sau xe máy, xe đạp, xích lô, tuk-tuk: **hai box riêng** — một `person` (`on_vehicle=yes`), một box xe. Hai box được phép chồng nhau.
- Box `person` gồm toàn bộ người nhìn thấy (cả chân đặt trên xe); box xe gồm toàn bộ xe nhìn thấy (phần bị người che nằm bên trong đường viền xe vẫn thuộc box xe).
- **Người bên trong xe kín** (ô tô, van, bus, cabin xe tải) nhìn **qua kính** → **không gán** `person`. Người nhìn thấy **trực tiếp** (xe mui trần `img_019`, sườn hở tuk-tuk bên phải `img_004`) → gán.
- Hàng hóa: box xe **chỉ gồm thân xe** (khung, cabin, thùng, nắp thùng, khung chở ô tô). **Không** gồm hàng chất cao vượt thân xe (bao tải trên auto-rickshaw `img_035`, tượng ngựa trên pickup `img_028`) **[CHƯA CHỐT — hàng quá khổ có thể ảnh hưởng va chạm]**.
- Đồ người cầm/gánh (đòn gánh `img_003`, ống thép dài `img_029`, túi xách `img_014`): **không** tính vào box người.
- Xe kéo rơ-moóc / xe chở ô tô (`img_002`): **một box `truck`** bao cả đầu kéo + rơ-moóc khi đang nối với nhau. Mỗi ô tô đang được chở là một box `car` riêng.
- Xe máy gắn sidecar (`img_022`) hoặc kéo thùng lôi (`img_025`): **một box `motorcycle`** bao cả phần gắn kèm.

### 3.4. Vật không thật → **không gán**
- Tượng, đài tưởng niệm, ma-nơ-canh: `img_017`, `img_027`, `img_033`, tượng rồng `img_013`, tượng ngựa `img_028`.
- Hình in: poster, biển quảng cáo, tranh tường, ảnh dán kính: `img_018`, `img_026`, `img_030`, `img_036`, `img_040`.
- Đồ chơi, mô hình thu nhỏ, thú bông: `img_038`, xe mô hình trên nóc `img_024`, thú bông Dangermouse `img_019`.
- **Phản chiếu**: trong gương chiếu hậu (`img_020`), trên kính cửa hàng (`img_033`, `img_038`), trên mặt đường ướt (`img_015`, `img_031`).
- Ngoại lệ: xe "trông như đồ chơi" nhưng **chạy được trên đường** (có biển số, có người lái) → gán (`img_019` → `car`). Xe độ trang trí nhưng vẫn có bánh, yên, tay lái chạm đất (`img_011`) → gán `motorcycle`.

### 3.5. Xe chủ (ego vehicle)
- Phần xe mà camera đang ngồi trong/trên (nắp capo, thân xe, gương, tay lái thấy từ góc người lái) → **không gán**: thân xe và gương `img_020`.
- Xe đỗ sát camera nhưng camera **không ở trong xe** (pickup `img_012` chụp từ phía sau thùng) → **gán** bình thường (`truncated=yes`).

### 3.6. Đám đông và vật dày đặc
- Vẽ `ignore_region` khi có **≥ 5 vật cùng lớp** chồng lấn mà **không vẽ được** từng box chắc chắn (đa số che ≥ 40 % hoặc cao < 20 px).
- Vật **ở rìa trước** cụm, cao ≥ 20 px và `occluded_level ≤ 2` → vẫn vẽ box riêng, kể cả khi nằm trong/kề `ignore_region`.
- `ignore_region` vẽ sát cụm, không phủ cả ảnh, không phủ lên vật lớn đã có box.
- Ví dụ: `img_021` (vẽ từng xe/người ở 1/3 dưới, phần xa là `ignore_region`), `img_030` (hàng xe máy đầu vẽ từng chiếc, phía sau `ignore_region`), `img_019` (đám đông sau rào), `img_008` (dãy xe đỗ sâu bên trái).
- Ngược lại `img_032` (≈ 35 người ở trạm xe buýt, cao ≈ 80–110 px): **vẽ từng người**, vì vẫn tách được.

### 3.7. Nhoè, tối, mưa
- Nhận ra chắc chắn lớp → vẽ box quanh **phần thân đậm nhất** của vật, không kéo theo vệt mờ đuôi; tick `can_review` nếu biên có thể lệch > 10 % (`img_014`, `img_015`, `img_026`).
- Không nhận ra lớp (quá tối, quá nhoè) → không vẽ; nếu rõ là có một cụm người/xe → `ignore_region`.

---

## 4. Ca khó (từ 40 ảnh)

| Ảnh | Tình huống | Quyết định | Lý do |
|---|---|---|---|
| img_001 | Xe tải nhỏ Suzuki bị cắt mép phải; nhiều người ngồi sau bàn; banner xúc xích bên trái | `truck` (`truncated=yes`); mỗi người ngồi là `person` (`occluded_level` 1–2 theo phần bị bàn/người khác che); banner không gán | Thùng hàng tách cabin → truck. Banner là hình in. |
| img_002 | Xe chở ô tô mang ~9 xe con; người nhỏ bên phải | 1 box `truck` bao đầu kéo + khung; mỗi xe con 1 box `car` (thường `occluded_level` 1–2 do khung); người cao ≥ 20 px → `person` | Xe được chở vẫn là xe thật, mô hình cần biết vị trí. |
| img_003 | Người bán gánh đòn gánh; người đứng cạnh xe đạp; bãi xe máy đỗ dày phía xa | `person` không gồm quang gánh; người đứng cạnh xe đạp không giạng chân → `on_vehicle=no`; `bicycle` riêng; bãi xe xa → `ignore_region` | Đồ cầm/gánh không phải thân người. |
| img_004 | 2 tuk-tuk, tài xế bên trái ngồi sau kính chắn gió, tài xế phải thấy trực tiếp từ sườn hở | 2 box `three_wheeler`; chỉ tài xế bên phải là `person` (`on_vehicle=yes`) | Quy tắc "qua kính → không gán" để hai người làm giống nhau. **[CHƯA CHỐT]** |
| img_005 | Cận cảnh người đi xe máy, xe gần như bị người che; van Hiace phía sau | Mỗi người `person` (`truncated=yes` nếu chạm mép); xe máy nào còn nhận ra (đầu xe, gương, đèn) → `motorcycle`, `occluded_level=3`; Hiace → `van` | Không bỏ xe chỉ vì bị che nhiều nếu còn nhận ra. |
| img_007 | Kho tối; pickup có thùng hộp phía sau; xe tải Isuzu cắt mép phải | Pickup có thùng hộp → `truck`; Isuzu → `truck` (`truncated=yes`) | Khoang hàng tách cabin. Ảnh tối nhưng vẫn rõ. |
| img_009 | Minibus (County), khách nhìn qua cửa kính; chó; người trên ban công | Minibus → `bus`; khách qua kính → không gán; chó → không gán; người ban công cao ≥ 20 px → `person` | Không phải van vì thân dài, cửa khách. |
| img_010 | Người ngồi trên xe máy đỗ nghịch điện thoại; xe đạp chở chuối | `person` `on_vehicle=yes`; xe đạp → `bicycle` (box không gồm khay chuối vượt thân xe) | `on_vehicle` không phụ thuộc xe chạy hay đỗ. |
| img_011 | Tượng/người hóa trang Predator; xe máy độ bằng sắt vụn | Predator không gán (không thấy bộ phận người thật), tick `can_review` nếu thấy da/tay người; xe độ → `motorcycle` | Có bánh, yên, ghi-đông chạm đất → coi là xe thật. **[CHƯA CHỐT]** |
| img_012 | Pickup chiếm góc dưới phải, camera ở sau thùng | `truck`, `truncated=yes`; Mazda → `car`; xe tải phía trước → `truck` | Không có dấu hiệu camera ngồi trong xe → không phải ego. |
| img_013 | Đêm, mưa; tượng rồng vàng; xe con nhỏ phía xa | 2 người đi bộ → `person`; tượng rồng không gán; xe xa < 20 px → `ignore_region` nếu ≥ 3 xe, không thì bỏ qua | Ngưỡng 20 px. |
| img_014 | Hai người đi bộ rõ, xung quanh xe máy nhoè chuyển động | 2 `person`; xe/người nhoè nhận ra được → vẽ box phần đậm, tick `can_review` | Biên nhoè không ổn định giữa hai người gán. |
| img_015 | Xe đỏ và SUV bạc cắt mép; xe phía sau có vệt mờ; phản chiếu trên đường ướt | 2 box `car` `truncated=yes`; xe nền vẽ phần đậm, `can_review`; phản chiếu không gán | Phản chiếu không phải vật. |
| img_016 | Tuk-tuk, van, pickup Nissan, xe Vespa chở hàng, người cắt mép phải-dưới | `three_wheeler` ×2; Hiace → `van`; pickup → `truck`; Vespa → `motorcycle` + `person`; người dưới phải `truncated=yes`; đầu người mờ góc trái dưới (không nhận ra) → không gán | Áp quy tắc cắt mép. |
| img_017 | Tượng người cưỡi ngựa đội nón giao thông | Không gán gì | Tượng. |
| img_018 | Biển quảng cáo có ảnh người; xe con sau hàng rào song; chụp qua kính xe | Ảnh người không gán; mỗi xe → `car`/`truck` (`occluded_level=1` do song rào) | Hàng rào mảnh tối đa mức 1. |
| img_019 | Xe diễu hành Dangermouse có biển số, người lái; thú bông; đám đông sau rào; đầu người nhoè tiền cảnh | Xe → `car`; người lái → `person` `on_vehicle=yes`; thú bông không gán; đám đông → `ignore_region`, người hàng đầu rõ ràng vẽ riêng; đầu người tiền cảnh → `person` `truncated=yes`, `can_review` | Xe chạy được trên đường = xe thật. |
| img_020 | Gương chiếu hậu phản chiếu xe phía sau + thân xe chủ | Không gán gì | Phản chiếu và ego. |
| img_021 | Dòng xe máy cực dày lúc chiều tối | ~1/3 dưới: từng `person` + `motorcycle`; phần xa (cao < 20 px, chồng lấn) → một `ignore_region`; xe con/xe buýt rõ → `car`/`bus` | Quy tắc đám đông 3.6. |
| img_022 | Ảnh đen trắng cũ, xe máy gắn sidecar, người ngồi | Một box `motorcycle` bao cả sidecar; người → `person` `on_vehicle=yes` | Sidecar gắn cứng vào xe máy. |
| img_023 | Xích lô có người đạp; người ngồi vỉa hè bên phải | Xích lô → `three_wheeler`; người đạp → `person` `on_vehicle=yes`; người ngồi → `person` `on_vehicle=no` | Xích lô là xe 3 bánh liền khối. |
| img_024 | Bảo tàng xe; xe mô hình vàng trên nóc xe đen | Các xe thật → `car`; mô hình trên nóc không gán; xe cam góc trái dưới `truncated=yes` | Mô hình không chạy được trên đường. **[CHƯA CHỐT — mô hình khá to]** |
| img_025 | Đường dạo ven biển; xe máy kéo thùng hàng; người ngồi ghế bãi biển | Xe máy + thùng → một `motorcycle`; người lái `person` `on_vehicle=yes`; người ngồi ghế → `person` `on_vehicle=no`; người xa < 20 px → `ignore_region` nếu thành cụm | Quy tắc 3.3 và 3.6. |
| img_026 | Đôi nam nữ trên xe máy nhoè, tranh tường cảng biển | 2 `person` + 1 `motorcycle`, tick `can_review` nếu biên nhoè; tranh tường không gán | Hình in. |
| img_027 | Xe pickup bằng đá đen ở nghĩa trang | Không gán | Đài tưởng niệm, không phải xe. |
| img_028 | Pickup thật chở tượng ngựa; SUV đỏ phía sau bị che | Pickup → `truck`, box chỉ thân xe (không gồm tượng ngựa); SUV → `car` `occluded_level=2` | Tượng không phải lớp; hàng chất cao không tính. **[CHƯA CHỐT]** |
| img_029 | Người đi xe điện chở ống thép dài; người giạng chân trên xe đạp | Xe điện dáng tay ga → `motorcycle`; xe đạp → `bicycle`; 2 người `on_vehicle=yes`; ống thép không tính vào box nào | Đồ cầm/chở không phải thân xe/người. |
| img_030 | Bãi xe máy dày đặc; poster người phía trên; bảo vệ | Xe hàng đầu (thấy ≥ 30 %) vẽ từng chiếc; phần sâu → `ignore_region`; bảo vệ → `person`; poster không gán | Quy tắc đám đông. |
| img_031 | Đêm mưa; xe, xe buýt, xe máy, người đi bộ; phản chiếu trên đường; tranh hoạt hình trên nhà | `car`, `bus`, `motorcycle` + `person` cho vật ≥ 20 px; phản chiếu và tranh không gán | Phản chiếu/hình in. |
| img_032 | ≈ 35 người đứng đợi xe buýt, chồng lấn | Vẽ từng người (đủ lớn, tách được); `occluded_level` từng người; xe con cắt mép trái `truncated=yes`; các xe đỗ phía sau bị người che → `car` theo mức che | Không lạm dụng `ignore_region`. |
| img_033 | Ma-nơ-canh, ảnh người mẫu, phản chiếu xe trên kính | Không gán gì | Toàn bộ là vật không thật/phản chiếu. |
| img_035 | Auto-rickshaw chở bao tải cao gấp đôi thân xe | `three_wheeler`, box chỉ thân xe; tài xế qua kính chắn gió → không gán | **[CHƯA CHỐT]** có nên tính hàng quá khổ. |
| img_036 | Xe tải nhỏ Veryca mui bạt; xe máy đỗ; poster người trên kính ngân hàng | `truck`; xe máy đỗ → `motorcycle`; poster không gán | Thùng hàng tách cabin. |
| img_037 | Pickup có nắp thùng cao (truck cap) trông giống van; xe buýt; người đi bộ | Pickup → `truck`; xe buýt → `bus` (xe phải `truncated`/`occluded` theo mức); người → `person` | Cabin và thùng vẫn tách rời → không phải van. |
| img_038 | Tủ kính đồ chơi: xe mô hình, thú bông | Không gán gì | Đồ chơi. |
| img_039 | Phố có xe máy đỗ, người đi bộ, xe đạp, xích lô nhỏ phía xa | Vật ≥ 20 px vẽ từng cái theo lớp; vật xa < 20 px bỏ qua hoặc `ignore_region` nếu ≥ 3 | Ngưỡng 20 px. |
| img_040 | Người đội mũ bảo hiểm cận cảnh (chỉ thấy 2 gương xe máy dưới đáy); taxi; tuk-tuk; SUV; xe buýt; ảnh dán trên kính taxi | Người → `person` `truncated=yes`, `on_vehicle=yes`; 2 gương xe máy không gán; taxi → `car` `occluded_level` 1–2; tuk-tuk → `three_wheeler`; SUV → `car`; xe buýt → `bus`; ảnh dán không gán | Phần xe máy thấy < 10 % và không nhận ra lớp. |

**Câu hỏi chưa chốt (đem ra họp Pha 2):**
1. Có thêm 3 lớp `bus`, `bicycle`, `three_wheeler` và thuộc tính `on_vehicle` không?
2. Hàng chất quá khổ (`img_028`, `img_035`) có tính vào box xe không?
3. Người sau kính chắn gió tuk-tuk/auto-rickshaw (`img_004`, `img_035`) có gán không?
4. Xe mô hình cỡ lớn (`img_024`) và nhân vật hóa trang (`img_011`): có cần quy tắc "thật/không thật" chi tiết hơn?

Ca nào gặp trong lúc gán mà không có trong bảng: tick `can_review`, ghi chú ngắn, báo nhóm trưởng. **Không tự đoán.**

---

## 5. QC và phiên bản

### 5.1. Ngưỡng áp dụng (theo `taxonomy.json` → `rules`, không đổi)

| Đại lượng | Ngưỡng |
|---|---|
| Box nhỏ nhất được vẽ từng vật | cao ≥ 20 px |
| IoU giữa hai người gán (box cao ≥ 50 px) | ≥ 0,85 |
| IoU giữa hai người gán (box cao 20–50 px) | ≥ 0,70 |
| IAA cả tập | IoU trung bình ≥ 0,85 **và** cùng lớp ≥ 95 % |
| Ghép cặp box khi so sánh | IoU ≥ 0,5 |
| Tỉ lệ lỗi theo ảnh để Release | ≤ 2 % (luôn ghi mẫu số, ví dụ "1/40 ảnh") |

### 5.2. Ai quyết
- Ca mơ hồ trong lúc gán: tick `can_review` + ghi chú, **không sửa guideline giữa Pha 3**.
- Ca bất đồng sau khi đo IAA: hai thành viên cùng xem ảnh ở buổi calibration; không thống nhất được thì **nhóm trưởng** chốt, ghi một dòng vào `calibration_decisions.csv` và tăng phiên bản guideline.
- Mọi thay đổi làm **đổi nhãn** (thêm/bớt lớp, đổi ngưỡng) → tăng phiên bản và ghi vào bảng dưới.

### 5.3. Lịch sử thay đổi

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản khởi đầu của giảng viên: 5 lớp vật + `ignore_region`, 3 thuộc tính, chưa có ca khó | — |
| v1-cá-nhân | Viết định nghĩa, ví dụ, phản ví dụ cho từng lớp; phân biệt car / van / truck (pickup → truck) | `img_001`, `img_007`, `img_012`, `img_037` |
| v1-cá-nhân | Đề xuất thêm lớp `bus`, `bicycle`, `three_wheeler` | `img_004`, `img_009`, `img_023`, `img_029`, `img_035` |
| v1-cá-nhân | `occluded_level` có ngưỡng % (10 / 40 / 70); bỏ nghĩa "3 = không rõ" | `img_001`, `img_002`, `img_005` |
| v1-cá-nhân | `truncated` có điều kiện đo (≤ 3 px tới mép) | `img_015`, `img_016`, `img_040` |
| v1-cá-nhân | Thêm thuộc tính `on_vehicle` cho `person`; quy tắc người + xe hai box | `img_005`, `img_010`, `img_026` |
| v1-cá-nhân | Quy tắc vật không thật / phản chiếu / ego / hình in | `img_017`, `img_020`, `img_027`, `img_033`, `img_038` |
| v1-cá-nhân | Quy tắc vật nhỏ (< 20 px), đám đông (≥ 5 vật) → `ignore_region` | `img_019`, `img_021`, `img_030`, `img_032` |
| v1-cá-nhân | Quy tắc hàng hóa, đồ cầm, sidecar, rơ-moóc | `img_002`, `img_003`, `img_022`, `img_028`, `img_029`, `img_035` |
| v1-cá-nhân | Quy tắc nhoè / tối / mưa và tiêu chí tick `can_review` | `img_013`, `img_014`, `img_015`, `img_026` |
