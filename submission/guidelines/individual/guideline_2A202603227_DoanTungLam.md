# Guideline gán nhãn — v1 (cá nhân) — 2A202603227 - Doãn Tùng Lâm | Nhóm Just2Men

- Phiên bản: v1-cá-nhân (viết lại từ `guideline_v0_starter.md`)
- Ngày: 2026-11-16
- Người viết: Doãn Tùng Lâm (2A202603227) · Người duyệt: cả nhóm ở Pha 2
- Phạm vi: **quy định chung** để gán bounding box người và phương tiện trên **mọi ảnh đường phố**, không riêng 40 ảnh của lab. 40 ảnh `img_001`–`img_040` chỉ là nguồn để tìm ra các tình huống khó; mục 4 (Ca khó) sẽ được điền sau khi gán nhãn.
- Công cụ: CVAT, xuất COCO 1.0

> **[CHƯA CHỐT]** = quyết định cá nhân của mình, cần đối chiếu với các thành viên khác ở Pha 2.
> Mọi con số (%, px) là ngưỡng để hai người gán độc lập ra **cùng một** nhãn.

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
Có → gán box (kể cả xe đang đỗ, đang trưng bày, đang được chở trên xe khác). Không → không gán.

---

## 2. Lớp và thuộc tính

### 2.1. Lớp (mỗi vật thuộc đúng một lớp)

v0 chỉ có 5 lớp vật, trong khi cảnh đường phố thực tế luôn có xe buýt, xe đạp, xe ba bánh (tuk-tuk, xích lô, auto-rickshaw) mà v0 không nói gán gì. Mình đề xuất **thêm 3 lớp** `bus`, `bicycle`, `three_wheeler` **[CHƯA CHỐT]**, vì mô hình phải tự phân biệt chúng (phép thử: *"mô hình có phải đoán ra không?"* → có → là lớp).

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Xe chở người ≤ 9 chỗ, có nắp capo, gầm thấp: sedan, hatchback, SUV, crossover, wagon, taxi, xe mui trần. | Sedan, SUV, taxi, xe cổ đang trưng bày, xe diễu hành chạy được trên đường. | Pickup → `truck`. Thân liền khối nóc cao → `van`. Xe mô hình/đồ chơi → không gán. |
| `van` | Xe thân liền khối (một hộp, capo rất ngắn), nóc cao rõ hơn ô tô con (≈ ≥ 1,3 lần chiều cao sedan), thường có cửa lùa, ≤ 16 chỗ. | Toyota Hiace, xe thùng kín cỡ nhỏ. | Minibus thân dài nhiều cửa sổ → `bus`. Pickup có nắp thùng cao → `truck`. |
| `truck` | Xe có **khoang hàng tách khỏi cabin**: pickup (thùng hở hoặc có nắp thùng), xe tải nhẹ/nặng, xe tải thùng kín, xe chở ô tô. | Pickup, xe tải mui bạt, xe tải thùng kín, xe chở ô tô nhiều tầng. | SUV 5 cửa không thùng → `car`. Xe tải làm bằng đá/mô hình → không gán. |
| `bus` **[mới]** | Xe chở khách ≥ 10 chỗ, thân dài nhiều ô cửa sổ, có cửa khách. | Xe buýt, xe khách, minibus. | Hiace → `van`. Songthaew (pickup chở khách) → `truck`. |
| `motorcycle` | Xe hai bánh có động cơ (xe số, tay ga, xe điện dáng tay ga), **kể cả khi gắn sidecar hoặc kéo thùng hàng**. | Xe máy, mô tô, Vespa, xe điện dáng tay ga, xe độ có bánh và yên thật. | Xe đạp → `bicycle`. Tuk-tuk → `three_wheeler`. |
| `bicycle` **[mới]** | Xe hai bánh đạp chân, không có sàn để chân kiểu tay ga (kể cả xe đạp chở hàng). | Xe đạp thường, xe đạp bán hàng rong. | Xe điện có sàn để chân → `motorcycle`. |
| `three_wheeler` **[mới]** | Xe ba bánh thiết kế liền khối để chở người/hàng. | Tuk-tuk, auto-rickshaw, xích lô. | Xe máy + sidecar → `motorcycle`. |
| `person` | Người thật, nhìn thấy **trực tiếp** (không qua kính xe), đang đứng, đi, ngồi hoặc ngồi trên xe. | Người đi bộ, người bán hàng, người lái/ngồi sau xe máy, xe đạp. | Tượng, ma-nơ-canh, người trên poster/tranh, ảnh dán kính → không gán. |
| `ignore_region` | **Vùng** (không phải vật) chứa nhiều người/xe quá nhỏ hoặc chồng lấn tới mức không vẽ được từng box; bỏ sót trong vùng này không tính lỗi. | Dòng xe máy xa, bãi xe máy dày, đám đông đứng sát nhau ở xa. | Không dùng để "né" vật to, rõ. |

**Vật không thuộc lớp nào** (động vật, cọc giao thông, thùng rác, tàu thuyền trong tranh, biển báo…): **không gán gì**, không dùng `ignore_region`.

**Nếu nhóm không thêm 3 lớp mới** (phương án dự phòng **[CHƯA CHỐT]**): `bus` ≤ 16 chỗ → `van`, còn lại không gán; `bicycle`, `three_wheeler` → không gán và tick `can_review`. Mình không khuyến khích vì mô hình sẽ học rằng xe đạp/tuk-tuk là "nền".

### 2.2. Thuộc tính

#### `occluded_level` — mức bị **vật khác** che (không tính phần ra ngoài mép ảnh)

Cách đo: hình dung toàn bộ đường viền của vật (kể cả phần bị che), ước lượng **phần trăm diện tích bị vật khác che**.

| Mức | Phần bị che | Ví dụ chung |
|---|---|---|
| `0` | < 10 % | Xe đứng riêng, thấy trọn. |
| `1` | 10 % – < 40 % | Xe bị chân người lái hoặc cột che một phần; xe sau hàng rào song mảnh. |
| `2` | 40 % – < 70 % | Người ngồi sau bàn; xe nằm sau khung xe chở ô tô. |
| `3` | ≥ 70 % nhưng **vẫn nhận ra chắc chắn lớp** | Xe máy gần như bị người lái che hết, còn thấy đèn/gương/đầu xe. |

- Che ≥ 70 % **và không nhận ra lớp** → không vẽ box (nếu là cả cụm → `ignore_region`).
- v0 ghi "3 là không rõ": bỏ nghĩa này. "Không chắc" dùng `can_review`, không dùng mức 3.
- Hàng rào song mảnh (song chiếm < 10 % diện tích vật, nhìn xuyên được) tối đa mức `1`.
- Người lái che xe máy **có tính** là che.

#### `truncated` — vật bị cắt ở mép ảnh

| Giá trị | Điều kiện |
|---|---|
| `yes` | Box chạm mép ảnh (cách mép ≤ 3 px) **và** vật rõ ràng còn tiếp tục ra ngoài khung hình. |
| `no` | Còn lại (kể cả vật sát mép nhưng thấy trọn). |

`truncated` độc lập với `occluded_level`: xe bị cắt mép nhưng không bị che → `truncated=yes`, `occluded_level=0`.

#### `on_vehicle` — chỉ cho `person` **[CHƯA CHỐT, thuộc tính mới]**

| Giá trị | Điều kiện |
|---|---|
| `yes` | Người đang ngồi trên xe (lái hoặc ngồi sau), hoặc giạng chân qua xe, kể cả khi xe đang đỗ. |
| `no` | Đi bộ, đứng, ngồi ghế; người dắt xe đi bên cạnh. |

Lý do: người trên xe di chuyển nhanh và theo hướng của xe, khác người đi bộ; mô hình không cần lớp riêng nên dùng thuộc tính để lọc và phân tích.

#### `can_review` — tick khi (và chỉ khi)

1. Phân vân giữa **hai lớp** cụ thể (ghi rõ hai lớp vào ghi chú).
2. Không chắc vật **thật hay không thật** (tượng, người hoá trang, mô hình lớn).
3. Vật **nhoè chuyển động** hoặc **quá tối** khiến biên box có thể lệch > 10 % chiều cao.
4. Tình huống thuộc các điểm **[CHƯA CHỐT]** (danh sách ở cuối mục 2).

Không tick `can_review` cho vật chỉ bị che hoặc bị cắt mép: đã có thuộc tính riêng.

### 2.3. Điểm chưa chốt (đem ra họp Pha 2)

1. Có thêm 3 lớp `bus`, `bicycle`, `three_wheeler` và thuộc tính `on_vehicle` không?
2. Hàng chất quá khổ có tính vào box xe không (mục 3.3)?
3. Người sau kính chắn gió tuk-tuk/auto-rickshaw có gán không (mục 3.3)?
4. Mô hình cỡ lớn và nhân vật hoá trang: có cần quy tắc "thật/không thật" chi tiết hơn (mục 3.4)?

---

## 3. Quy tắc vẽ box

### 3.1. Nguyên tắc chung
1. **Ôm sát phần nhìn thấy**: không đoán phần bị che, không vẽ vượt ra ngoài phần thấy được. Sai lệch cho phép ≤ 2 px mỗi cạnh với vật cao ≥ 50 px.
2. Mỗi vật **một box**; không gộp hai vật vào một box (trừ `ignore_region`).
3. Vật có box cao **< 20 px** → không vẽ từng vật. Vùng có ≥ 3 vật nhỏ như vậy → một `ignore_region` bao quanh; chỉ 1–2 vật lẻ → bỏ qua.
4. Box tính cả phụ kiện **đang gắn trên** vật: mũ bảo hiểm, nón lá, ba lô đang đeo (người); gương, giá chở hàng, nắp thùng, khung chở xe (xe).

### 3.2. Vật bị che / bị cắt mép
- Bị che: vẽ phần thấy được, gán `occluded_level` theo 2.2. Nếu vật bị chia làm hai mảnh (cột điện chắn giữa), **một box** bao cả hai.
- Bị cắt mép: box dừng ở mép ảnh, `truncated=yes`. Phần thấy < 10 % và không nhận ra lớp chỉ từ phần đó (ví dụ chỉ lộ hai gương xe) → không gán.

### 3.3. Người và xe (một vật có nhiều phần)
- Người lái/ngồi trên xe máy, xe đạp, xích lô, tuk-tuk: **hai box riêng** — `person` (`on_vehicle=yes`) và box xe. Hai box được phép chồng nhau.
- Box `person` gồm toàn bộ người nhìn thấy (cả chân đặt trên xe). Box xe gồm toàn bộ xe nhìn thấy; phần bị người che nằm trong đường viền xe vẫn thuộc box xe.
- **Người trong xe kín** (ô tô, van, bus, cabin tải) nhìn **qua kính** → **không gán** `person`. Người thấy **trực tiếp** (xe mui trần, tuk-tuk sườn hở) → gán.
- **Hàng hoá:** box xe **chỉ gồm thân xe** (khung, cabin, thùng, nắp thùng, khung chở xe). Hàng chất cao vượt thân xe và vật trang trí đặt trên xe (tượng, mô hình) **không** tính **[CHƯA CHỐT — hàng quá khổ có thể ảnh hưởng va chạm]**.
- **Đồ cầm/gánh/vác** (đòn gánh, ống dài, túi xách): không tính vào box người.
- **Xe kéo rơ-moóc / xe chở ô tô**: một box `truck` bao cả đầu kéo và rơ-moóc khi đang nối. Mỗi ô tô được chở là một box `car` riêng.
- **Xe máy gắn sidecar hoặc kéo thùng hàng**: một box `motorcycle` bao cả phần gắn kèm.

### 3.4. Vật không thật → **không gán**
- Tượng, đài tưởng niệm, ma-nơ-canh (kể cả tượng người cưỡi ngựa, tượng động vật, xe được tạc bằng đá).
- Hình in: poster, biển quảng cáo, tranh tường, ảnh dán kính xe.
- Đồ chơi, mô hình thu nhỏ, thú bông, xe mô hình đặt trên xe khác.
- **Phản chiếu**: trong gương chiếu hậu, trên kính cửa hàng, trên mặt đường ướt.
- **Ngoại lệ (vẫn là vật thật):** xe có hình dáng đồ chơi nhưng **chạy được trên đường** (có biển số, có người lái) → gán. Xe độ trang trí nhưng còn bánh, yên, tay lái chạm đất → gán.
- Người hoá trang/nhân vật cosplay: chỉ gán `person` khi thấy rõ là người thật (da, mặt, tay chân); nếu không chắc → không gán và tick `can_review`.

### 3.5. Xe chủ (ego vehicle)
- Phần xe mà camera đang ngồi trong/trên (nắp capo, thân xe, gương thấy từ góc người lái) → **không gán**.
- Xe đỗ sát camera nhưng camera **không ở trong xe** (chụp từ ngoài, từ phía sau thùng) → **gán** bình thường, thường kèm `truncated=yes`.

### 3.6. Đám đông và vật dày đặc
- Vẽ `ignore_region` khi có **≥ 5 vật cùng lớp** chồng lấn mà **không vẽ được** từng box chắc chắn (đa số che ≥ 40 % hoặc cao < 20 px).
- Vật **ở rìa trước** cụm, cao ≥ 20 px và `occluded_level ≤ 2` → vẫn vẽ box riêng.
- `ignore_region` vẽ sát cụm, không phủ cả ảnh, không phủ lên vật lớn đã có box.
- Đám đông còn **tách được từng người** (cao ≳ 50 px, che ≤ mức 2) → vẽ từng người, **không** dùng `ignore_region`.

### 3.7. Nhoè, tối, mưa
- Nhận ra chắc chắn lớp → vẽ box quanh **phần thân đậm nhất**, không kéo theo vệt mờ đuôi; tick `can_review` nếu biên có thể lệch > 10 %.
- Không nhận ra lớp (quá tối, quá nhoè) → không vẽ; nếu rõ là có cụm người/xe → `ignore_region`.

---

## 4. Ca khó

Chưa điền. Mới xem ảnh chứ chưa gán nên chưa biết ca nào khó thật. Gán xong sẽ quay lại ghi.

| Ảnh | Tình huống | Quyết định | Lý do |
|---|---|---|---|
| | | | |

Gặp tình huống không có trong guideline khi gán: tick `can_review`, ghi chú ngắn, báo nhóm trưởng. **Không tự đoán.**

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

| Phiên bản | Thay đổi | Lý do |
|---|---|---|
| v0 | Bản khởi đầu của giảng viên: 5 lớp vật + `ignore_region`, 3 thuộc tính, chưa có ca khó | — |
| v1-cá-nhân | Viết định nghĩa, ví dụ, phản ví dụ cho từng lớp; pickup → `truck` | Xem qua 40 ảnh: v0 không phân biệt được pickup, van, xe tải nhỏ |
| v1-cá-nhân | Đề xuất thêm lớp `bus`, `bicycle`, `three_wheeler` | Xem qua 40 ảnh: có nhiều xe buýt, xe đạp, tuk-tuk/xích lô mà v0 không có lớp |
| v1-cá-nhân | `occluded_level` có ngưỡng % (10 / 40 / 70); bỏ nghĩa "3 = không rõ" | v0 không có ngưỡng đo được, nghĩa mức 3 trùng với `can_review` |
| v1-cá-nhân | `truncated` có điều kiện đo (≤ 3 px tới mép) | v0 không nói thế nào là "bị cắt" |
| v1-cá-nhân | Thêm thuộc tính `on_vehicle`; quy tắc người + xe hai box; người qua kính không gán | Xem qua 40 ảnh: nhiều người ngồi trên xe, v0 không nói gán mấy box |
| v1-cá-nhân | Quy tắc vật không thật, phản chiếu, hình in, xe chủ (ego) | Xem qua 40 ảnh: có tượng, ma-nơ-canh, poster, đồ chơi, gương chiếu hậu |
| v1-cá-nhân | Quy tắc vật nhỏ (< 20 px) và đám đông (≥ 5 vật) → `ignore_region` | Xem qua 40 ảnh: có cảnh xe máy dày đặc, đám đông; v0 không nói khi nào dùng `ignore_region` |
| v1-cá-nhân | Quy tắc hàng hoá, đồ cầm, sidecar, rơ-moóc | Xem qua 40 ảnh: xe chở hàng quá khổ, xe chở ô tô, xe gắn sidecar |
| v1-cá-nhân | Quy tắc nhoè/tối/mưa và tiêu chí tick `can_review` | Xem qua 40 ảnh: ảnh đêm, mưa, nhoè chuyển động |
| v1-cá-nhân | Mục 4 (Ca khó) để trống, chờ cập nhật | Mới xem ảnh, chưa gán nhãn nên chưa có ca khó thực tế |
| (dự kiến) | Điền mục 4 từ các ca gặp khi gán nhãn và calibration | Cập nhật sau khi gán nhãn xong |
