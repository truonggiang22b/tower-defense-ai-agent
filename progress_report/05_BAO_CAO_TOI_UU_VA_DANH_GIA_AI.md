# BÁO CÁO 05 - TỐI ƯU VÀ ĐÁNH GIÁ AI HEURISTIC

**Dự án:** Tower Defense AI - Nhập môn Trí tuệ nhân tạo  
**Ngày lập báo cáo:** 2026-06-03  
**Phạm vi báo cáo:** Tổng hợp quá trình cải thiện AI heuristic, kết quả thực nghiệm trước/sau tối ưu, phân tích hành vi từng profile AI và hướng phát triển tiếp theo.

---

## 1. Mục tiêu báo cáo

Báo cáo này tập trung vào phần quan trọng nhất của dự án: đánh giá xem AI trong game thủ thành có thật sự thể hiện được năng lực ra quyết định hay không.

Mục tiêu cụ thể:

- Tổng hợp trạng thái AI trước khi tối ưu.
- Trình bày các thay đổi đã thực hiện trong `HeuristicEvaluator`.
- So sánh kết quả trước và sau tối ưu bằng số liệu.
- Kiểm chứng độ ổn định bằng batch 100 trận.
- Phân tích vì sao một số profile AI thắng tốt hơn profile khác.
- Chỉ ra hạn chế còn lại và hướng phát triển phù hợp với môn Nhập môn Trí tuệ nhân tạo.

Dự án không đặt mục tiêu xây dựng game thương mại hoàn chỉnh. Trọng tâm là mô hình hóa tác tử thông minh, biểu diễn trạng thái, thiết kế hành động, xây dựng hàm đánh giá heuristic và kiểm chứng bằng thực nghiệm.

---

## 2. Tóm tắt hệ thống AI hiện tại

Hệ thống AI của dự án gồm 5 cấu hình được dùng trong thực nghiệm:

| Cấu hình | Vai trò |
|---|---|
| `random_balanced` | Baseline ngẫu nhiên, dùng để so sánh mức thấp nhất |
| `rule_based_balanced` | Baseline có luật đơn giản |
| `heuristic_defensive` | AI heuristic thiên phòng thủ |
| `heuristic_balanced` | AI heuristic cân bằng giữa công và thủ |
| `heuristic_aggressive` | AI heuristic thiên tấn công |

Trong đó, phần AI chính của dự án là `HeuristicAI`. Pipeline ra quyết định:

```text
GameState
-> LaneSummary
-> Candidate Actions
-> Utility Score
-> Greedy Best Action
```

Ý nghĩa từng bước:

- `GameState`: trạng thái đầy đủ của trận đấu, gồm máu căn cứ, tài nguyên, tháp, quân, lane và thời gian.
- `LaneSummary`: tóm tắt từng lane bằng các chỉ số như nguy cơ bị thủng lane, cơ hội tấn công, sức mạnh tháp hai bên.
- `Candidate Actions`: danh sách hành động hợp lệ AI có thể chọn, ví dụ xây tháp, nâng cấp tháp, gửi quân, tiết kiệm tài nguyên.
- `Utility Score`: điểm số đánh giá mức độ tốt của từng hành động.
- `Greedy Best Action`: AI chọn hành động có điểm cao nhất ở thời điểm hiện tại.

Đây là cách tiếp cận AI cổ điển, phù hợp với môn Nhập môn Trí tuệ nhân tạo vì có thể giải thích được, đo lường được và không phụ thuộc vào mô hình hộp đen.

---

## 3. Tiêu chí đánh giá

Các chỉ số đánh giá được lấy từ hệ thống log của dự án:

| Chỉ số | Ý nghĩa |
|---|---|
| `Win rate` | Tỷ lệ trận AI thắng |
| `AI HP Avg` | Máu trung bình của căn cứ AI cuối trận |
| `Damage to Player Base` | Sát thương trung bình AI gây lên căn cứ người chơi |
| `Resource Eff` | Hiệu quả tài nguyên, tính theo damage vào base / tài nguyên đã tiêu |
| `Attack Avg` | Số lần AI chọn hành động tấn công trung bình |
| `Defense Avg` | Số lần AI chọn hành động phòng thủ trung bình |
| `Decision ms Avg` | Thời gian ra quyết định trung bình của AI |
| `Main Lane` | Lane AI tấn công nhiều nhất |
| `Most Effective Damage Lane` | Lane gây damage vào căn cứ hiệu quả nhất |

Trong báo cáo này, kết quả chính được đánh giá bằng batch `100 trận / AI`, vì mẫu lớn hơn giúp giảm nhiễu so với batch nhỏ.

Điều kiện kiểm chứng chính:

```text
Số trận mỗi AI: 100
Seed: 42
Player strategy: balanced
Map: fixed_lane
```

---

## 4. Trạng thái trước tối ưu

Trước vòng tối ưu mới, kết quả chính từ batch `30 trận / AI`, player `balanced`, seed `42` như sau:

| AI profile | Win rate | AI HP Avg | Damage vào Player Base | Resource Eff | Attack Avg | Defense Avg |
|---|---:|---:|---:|---:|---:|---:|
| `heuristic_defensive` | 43.3% | 377.5 | 113.3 | 0.024 | 87.8 | 4.9 |
| `heuristic_balanced` | 16.7% | 340.3 | 118.1 | 0.025 | 100.5 | 4.0 |
| `heuristic_aggressive` | 0.0% | 248.3 | 118.1 | 0.026 | 121.0 | 0.0 |

Nhận xét:

- `heuristic_defensive` có tỷ lệ thắng tốt nhất vì giữ căn cứ AI ổn định hơn.
- `heuristic_balanced` gây damage tốt nhưng tỷ lệ thắng thấp, cho thấy phòng thủ chưa đủ.
- `heuristic_aggressive` tấn công nhiều nhất nhưng không thắng trận nào, vì gần như không phòng thủ.
- Điểm yếu chính không nằm ở khả năng gây damage, mà nằm ở việc AI chưa cân bằng tốt giữa tấn công và sinh tồn.

Giả thuyết tối ưu:

```text
Balanced và aggressive đã biết tạo áp lực,
nhưng cần phanh tấn công khi lane nguy hiểm hoặc AI HP thấp.
```

---

## 5. Các cải thiện đã thực hiện

Các thay đổi được thực hiện trong `src/ai/heuristic_evaluator.py`.

### 5.1. Tăng phòng thủ khi AI gặp nguy hiểm

AI được tăng điểm cho hành động:

- `BUILD_TOWER`
- `UPGRADE_TOWER`

khi:

- máu căn cứ AI thấp;
- lane có nguy cơ bị thủng;
- chưa có đủ sức mạnh tháp ở lane đó.

Mục tiêu: tránh tình trạng AI tiếp tục gửi quân trong khi căn cứ của chính nó đang bị ép.

### 5.2. Thêm phanh an toàn cho `heuristic_balanced`

Profile cân bằng được điều chỉnh để:

- vẫn tấn công khi có cơ hội;
- giảm điểm `SEND_UNIT` nếu có lane nguy hiểm;
- ưu tiên xây hoặc nâng cấp tháp khi HP dưới ngưỡng an toàn.

Mục tiêu: giữ damage tốt nhưng tăng tỷ lệ thắng.

### 5.3. Thêm phanh an toàn cho `heuristic_aggressive`

Trước tối ưu, `heuristic_aggressive` gần như chỉ tấn công. Sau tối ưu, profile này vẫn giữ thiên hướng tấn công, nhưng:

- nếu AI HP thấp, giảm mạnh điểm gửi quân;
- nếu lane đang nguy hiểm, ưu tiên phòng thủ hơn;
- nếu chưa có cơ hội rõ ràng, không dồn wave quá sớm.

Mục tiêu: giữ bản sắc tấn công nhưng không tự thua vì bỏ thủ hoàn toàn.

### 5.4. Cải thiện chọn lane tấn công

AI được bổ sung logic đánh giá hiệu quả lane ngay trong trận:

- lane nào từng chuyển hóa attack thành damage vào base thì được cộng điểm;
- lane nào bị spam nhiều nhưng không gây damage thì bị trừ điểm;
- lane gây damage tốt nhất được ưu tiên hơn trong các quyết định tiếp theo.

Mục tiêu: tránh gửi quân lặp lại vào lane không hiệu quả.

### 5.5. Cải thiện wave tấn công

AI được bổ sung logic thưởng wave lớn khi:

- lane có `attack_opportunity` tốt;
- lane đã từng gây damage vào Player Base;
- dùng `FAST` unit trong lane có phòng thủ yếu.

Riêng `heuristic_aggressive` được chỉnh để ưu tiên `FAST` wave hơn, giảm lạm dụng `SWARM` và `TANK` khi chưa có áp lực sẵn.

Mục tiêu: giúp AI tấn công có chủ ý hơn thay vì chỉ gửi quân đều đều.

---

## 6. Kết quả sau tối ưu - batch 30 trận

Sau vòng tối ưu đầu tiên, kết quả batch `30 trận / AI` với player `balanced`, seed `42`:

| AI profile | Win trước | Win sau | AI HP trước | AI HP sau | Damage trước | Damage sau | Defense trước | Defense sau |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `heuristic_defensive` | 43.3% | 46.7% | 377.5 | 377.8 | 113.3 | 113.3 | 4.9 | 10.0 |
| `heuristic_balanced` | 16.7% | 56.7% | 340.3 | 372.2 | 118.1 | 117.7 | 4.0 | 6.2 |
| `heuristic_aggressive` | 0.0% | 20.0% | 248.3 | 350.7 | 118.1 | 118.1 | 0.0 | 5.1 |

Nhận xét:

- `heuristic_balanced` cải thiện mạnh nhất, từ 16.7% lên 56.7%.
- `heuristic_aggressive` từ 0.0% lên 20.0%, chứng tỏ phanh an toàn có tác dụng.
- `heuristic_defensive` tăng nhẹ và không bị mất khả năng phòng thủ.
- Damage vào căn cứ người chơi gần như được giữ nguyên, nghĩa là tăng phòng thủ không làm AI mất sức tấn công.

Tuy nhiên, batch 30 vẫn có thể chịu ảnh hưởng bởi dao động mẫu. Vì vậy cần kiểm chứng thêm bằng batch 100 trận.

---

## 7. Kết quả kiểm chứng 100 trận

Batch kiểm chứng lớn hơn:

```text
python simulate.py --experiment -n 100 --player balanced --seed 42
```

Kết quả:

| AI profile | Win rate | AI HP Avg | Damage vào Player Base | Resource Eff | Attack Avg | Defense Avg | Main Lane | Damage Lane | Decision ms Avg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `random_balanced` | 3.0% | 323.9 | 20.0 | 0.004 | 94.3 | 9.6 | 0 | 2 | 0.0491 |
| `rule_based_balanced` | 0.0% | 256.4 | 39.6 | 0.009 | 89.1 | 1.2 | 0 | 1 | 0.0160 |
| `heuristic_defensive` | 46.0% | 390.1 | 97.8 | 0.021 | 83.3 | 9.2 | 2 | 2 | 0.2640 |
| `heuristic_balanced` | 48.0% | 393.0 | 104.2 | 0.022 | 100.0 | 5.0 | 2 | 2 | 0.2381 |
| `heuristic_aggressive` | 17.0% | 356.2 | 104.3 | 0.022 | 97.6 | 4.9 | 2 | 2 | 0.2721 |

Nhận xét chính:

- Cả 3 heuristic AI đều tốt hơn rõ ràng so với `RandomAI` và `RuleBasedAI`.
- `heuristic_balanced` là profile tổng thể tốt nhất trong batch 100, với win rate 48.0%.
- `heuristic_defensive` gần tương đương, win rate 46.0% và AI HP cao.
- `heuristic_aggressive` cải thiện so với trước tối ưu, nhưng vẫn thấp hơn balanced và defensive.
- Cả `heuristic_balanced` và `heuristic_aggressive` đã chọn lane tấn công chính là lane 2, trùng với lane gây damage tốt nhất. Điều này cho thấy logic chọn lane đã có tác dụng.

---

## 8. Phân tích từng AI profile

### 8.1. RandomAI

`RandomAI` chọn hành động ngẫu nhiên trong tập hành động hợp lệ.

Kết quả 100 trận:

- Win rate: 3.0%
- Damage vào Player Base: 20.0
- Resource Eff: 0.004

Ý nghĩa:

- Đây là baseline thấp nhất.
- Kết quả yếu là hợp lý vì AI không phân tích trạng thái.
- Việc heuristic AI vượt random chứng minh rằng hàm đánh giá và lane summary có tác dụng.

### 8.2. RuleBasedAI

`RuleBasedAI` dùng một số luật đơn giản:

- nếu bị ép thì phòng thủ;
- nếu an toàn thì tấn công lane yếu;
- nếu không rõ thì xây tháp hoặc tiết kiệm.

Kết quả 100 trận:

- Win rate: 0.0%
- Damage vào Player Base: 39.6
- Resource Eff: 0.009

Ý nghĩa:

- Rule-based tốt hơn random về damage nhưng vẫn cứng nhắc.
- AI này không đánh giá sâu từng hành động.
- Đây là baseline có logic nhưng chưa đủ thích nghi.

### 8.3. Heuristic Defensive

`heuristic_defensive` ưu tiên bảo vệ căn cứ AI.

Kết quả 100 trận:

- Win rate: 46.0%
- AI HP Avg: 390.1
- Defense Avg: 9.2

Ý nghĩa:

- Đây là profile ổn định.
- Không gây damage cao nhất, nhưng giữ máu tốt.
- Phù hợp khi mục tiêu là sinh tồn và thắng bằng HP cuối trận.

### 8.4. Heuristic Balanced

`heuristic_balanced` cân bằng giữa tấn công và phòng thủ.

Kết quả 100 trận:

- Win rate: 48.0%
- Damage vào Player Base: 104.2
- AI HP Avg: 393.0

Ý nghĩa:

- Đây là profile tổng thể tốt nhất hiện tại.
- Vừa giữ HP tốt, vừa gây damage ổn.
- Sau tối ưu, profile này thể hiện rõ giá trị của việc kết hợp công và thủ.

### 8.5. Heuristic Aggressive

`heuristic_aggressive` ưu tiên tấn công và gây áp lực.

Kết quả 100 trận:

- Win rate: 17.0%
- Damage vào Player Base: 104.3
- AI HP Avg: 356.2

Ý nghĩa:

- Profile này đã cải thiện so với trạng thái trước tối ưu, khi win rate là 0.0%.
- Tuy nhiên, aggressive vẫn chưa vượt balanced vì tấn công nhiều không đồng nghĩa với gây damage vào căn cứ.
- Nếu quân bị tháp tiêu diệt giữa đường, số lần tấn công cao nhưng damage vào base không tăng.
- Profile này cần chiến thuật wave sâu hơn hoặc lookahead để chọn thời điểm dồn quân tốt hơn.

---

## 9. Vì sao AI tấn công chưa gây damage vượt trội?

Trong game thủ thành, hành động gửi quân chỉ có giá trị nếu quân đi đến được căn cứ đối phương. Vì vậy:

```text
Attack count cao không đồng nghĩa với base damage cao.
```

Các nguyên nhân chính:

### 9.1. Quân bị chặn trước khi chạm căn cứ

Nếu người chơi có tháp đủ mạnh, quân AI bị tiêu diệt giữa lane. Khi đó AI vẫn tiêu tài nguyên và vẫn được tính là đã tấn công, nhưng không tạo damage vào căn cứ.

### 9.2. Tấn công thiếu phối hợp dài hạn

AI hiện tại chọn hành động tốt nhất ở trạng thái hiện tại. Nó chưa mô phỏng sâu kiểu:

```text
Gửi tank trước để hút damage
-> gửi fast sau để xuyên lane
-> đổi lane nếu đối thủ xây tháp phản ứng
```

Vì vậy profile aggressive có xu hướng tạo áp lực, nhưng chưa có chiến thuật dồn đợt đủ sâu.

### 9.3. Phanh an toàn làm aggressive bớt cực đoan

Sau tối ưu, aggressive không còn bỏ thủ hoàn toàn. Điều này giúp AI sống lâu hơn, nhưng cũng làm số lần tấn công cực đoan giảm xuống. Đây là đánh đổi cần thiết vì mục tiêu cuối cùng là thắng trận, không chỉ gây damage.

### 9.4. Player balanced là đối thủ tương đối ổn định

AutoPlayer balanced có khả năng xây tháp, gửi quân và phản ứng ở nhiều lane. Vì vậy việc chỉ tấn công nhiều hơn không đủ để xuyên thủ.

---

## 10. Đánh giá theo tinh thần môn Nhập môn AI

Dự án hiện tại đáp ứng tốt các yếu tố cốt lõi của môn học:

| Yếu tố AI | Thể hiện trong dự án |
|---|---|
| Tác tử thông minh | AI quan sát trạng thái và chọn hành động |
| Môi trường | Game thủ thành 2D đối kháng theo lane |
| Trạng thái | `GameState` |
| Hành động | Xây tháp, nâng cấp, gửi quân, tiết kiệm |
| Hàm đánh giá | `HeuristicEvaluator.score()` |
| Heuristic | Danger, opportunity, tower strength, unit pressure |
| Baseline | RandomAI, RuleBasedAI |
| Thực nghiệm | Batch simulation 30 và 100 trận |
| Đánh giá định lượng | Win rate, HP, damage, resource efficiency, decision time |

Không dùng neural network không làm dự án sai tinh thần AI. Ngược lại, với môn nhập môn, cách tiếp cận heuristic có ưu điểm là giải thích được và kiểm chứng được.

---

## 11. Hạn chế còn lại

Các hạn chế hiện tại:

- AI chưa có lookahead, tức chưa mô phỏng kết quả tương lai của từng hành động.
- Aggressive chưa biết phối hợp wave phức tạp theo nhiều bước.
- Chọn lane đã cải thiện, nhưng vẫn dựa vào thống kê trong trận, chưa dự đoán phản ứng tiếp theo của người chơi.
- Chưa có tối ưu tự động trọng số bằng hill-climbing hoặc genetic algorithm.
- Batch simulation dùng AutoPlayer, chưa đại diện hoàn toàn cho người chơi thật.
- Max decision time của aggressive có spike trong batch 100, cần theo dõi nếu tiếp tục thêm scoring phức tạp.

---

## 12. Hướng phát triển tiếp theo

Các hướng phát triển hợp lý:

### 12.1. One-step lookahead

AI thử mô phỏng ngắn hạn sau từng hành động ứng viên:

```text
Nếu chọn hành động này,
sau vài giây trạng thái có tốt hơn không?
```

Cách này giống tư tưởng nhìn trước nước đi trong game đối kháng, nhưng đơn giản hơn minimax sâu.

### 12.2. Tối ưu wave phối hợp

Thêm chiến thuật:

```text
Tank đi trước
Fast đi sau
Swarm dùng khi lane phòng thủ yếu
```

Mục tiêu là giúp aggressive không chỉ tấn công nhiều, mà tấn công đúng thời điểm.

### 12.3. Tự động tìm trọng số

Có thể dùng hill-climbing hoặc genetic algorithm để thử nhiều bộ trọng số heuristic:

```text
Sinh bộ trọng số
-> chạy simulation
-> đo win rate/resource efficiency
-> giữ bộ tốt hơn
```

Đây là hướng phù hợp nếu muốn nâng chất lượng AI mà vẫn giữ khả năng giải thích.

### 12.4. Đánh giá với người chơi thật

Sau khi hoàn thiện báo cáo, có thể cho nhiều người chơi thử và so sánh cảm nhận với kết quả AutoPlayer.

---

## 13. Kết luận

Dự án đã đạt mức đủ tốt để đưa vào báo cáo cuối kỳ. AI heuristic không chỉ chạy được mà còn có quá trình cải thiện rõ ràng:

```text
Baseline
-> phát hiện vấn đề
-> tinh chỉnh heuristic
-> chạy lại thực nghiệm
-> kiểm chứng bằng 100 trận
-> phân tích hạn chế
```

Kết quả quan trọng nhất:

- Heuristic AI vượt rõ RandomAI và RuleBasedAI.
- `heuristic_balanced` là profile tổng thể tốt nhất hiện tại.
- `heuristic_defensive` ổn định và giữ HP tốt.
- `heuristic_aggressive` thể hiện đúng xu hướng tấn công nhưng còn hạn chế về phối hợp wave.
- Hệ thống log và simulation đủ để chứng minh kết quả bằng số liệu thay vì cảm tính.

Với phạm vi môn Nhập môn Trí tuệ nhân tạo, dự án đã thể hiện đúng các yếu tố: tác tử, môi trường, trạng thái, hành động, heuristic, hàm đánh giá và thực nghiệm định lượng.

