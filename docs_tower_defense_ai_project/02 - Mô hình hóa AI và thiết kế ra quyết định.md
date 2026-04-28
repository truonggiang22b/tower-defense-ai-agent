# Mô hình hóa AI và thiết kế ra quyết định

## 1. Vai trò của AI trong đề tài
AI trong đề tài này là một tác tử thông minh cạnh tranh với người chơi trong môi trường game động. AI không cần hoàn hảo, nhưng phải ra quyết định hợp lý, giải thích được và tạo ra khác biệt rõ ràng so với AI ngẫu nhiên.

## 2. Mô hình PEAS

### Performance Measure
- Thắng trận
- Giữ máu căn cứ AI ở mức cao
- Gây nhiều sát thương lên căn cứ người chơi
- Tiêu diệt được nhiều quân của người chơi
- Sử dụng tài nguyên hiệu quả
- Thời gian ra quyết định đủ nhanh

### Environment
- Game 2D dạng lane hoặc lưới
- Có hai căn cứ đối kháng
- Có tháp, quân, tài nguyên, cooldown
- Trạng thái thay đổi liên tục theo tick
- Có yếu tố cạnh tranh và giới hạn thời gian

### Actuators
- Xây tháp
- Nâng cấp tháp
- Gửi quân
- Chọn lane tấn công
- Chờ để tiết kiệm tài nguyên

### Sensors
- Trạng thái máu căn cứ
- Tài nguyên hiện tại
- Danh sách tháp và quân trên từng lane
- Chỉ số nguy hiểm từng lane
- Cooldown còn lại
- Thời gian trận đấu

## 3. Đặc điểm môi trường
- Động: quân di chuyển và trạng thái thay đổi liên tục
- Tuần tự: quyết định ở hiện tại ảnh hưởng tương lai
- Cạnh tranh: người chơi liên tục tác động vào kết quả
- Hữu hạn thời gian: trận đấu có giới hạn
- Gần như quan sát đầy đủ: trong bản học thuật, AI được phép nhìn thấy gần hết trạng thái
- Không xác định hoàn toàn nếu người chơi là người thật, nhưng có thể coi là xác định theo trạng thái vật lý game

## 4. Percepts của AI
AI nên quan sát ít nhất các nhóm thông tin sau:

### 4.1. Trạng thái căn cứ
- `ai_base_hp`
- `player_base_hp`
- tỷ lệ phần trăm máu còn lại

### 4.2. Trạng thái tài nguyên
- `ai_resource`
- `player_resource` nếu cho phép quan sát đầy đủ
- tốc độ tăng tài nguyên hiện tại

### 4.3. Trạng thái lane
- số quân địch đang tiến vào AI theo từng lane
- số quân AI đang tiến vào người chơi theo từng lane
- mật độ tháp của người chơi trên từng lane
- mật độ tháp của AI trên từng lane
- chỉ số nguy hiểm từng lane
- chỉ số cơ hội tấn công từng lane

### 4.4. Trạng thái chiến thuật
- cooldown xây hoặc nâng cấp
- cooldown sinh quân
- thời gian còn lại của trận
- wave đang diễn ra

## 5. Không gian hành động

## 5.1. Nhóm hành động phòng thủ
- Xây tháp nhanh ở lane có nhiều quân nhanh địch
- Xây tháp nặng ở lane có quân trâu địch
- Nâng cấp tháp chủ lực ở lane nguy hiểm
- Tăng phòng thủ gần căn cứ khi áp lực quá lớn

## 5.2. Nhóm hành động tấn công
- Gửi quân nhanh vào lane có nhiều tháp bắn chậm
- Gửi quân trâu vào lane thiếu sát thương cao
- Gửi quân rẻ số đông để kéo giãn tài nguyên phòng thủ của người chơi
- Gửi wave kết hợp, ví dụ 1 quân trâu + 2 quân nhanh

## 5.3. Nhóm hành động kinh tế
- Chờ đủ tiền để tung đợt tấn công lớn hơn
- Không mua tháp mới khi lane đang an toàn
- Giữ một phần tài nguyên dự phòng nếu nhiều lane cùng nguy hiểm

## 6. Biểu diễn GameState

### 6.1. Biểu diễn đầy đủ

```text
GameState = {
  player_base_hp,
  ai_base_hp,
  player_resource,
  ai_resource,
  player_towers[],
  ai_towers[],
  active_units[],
  lanes[],
  current_wave,
  match_time,
  cooldowns,
  lane_danger_scores[]
}
```

### 6.2. Rút gọn trạng thái cho AI
Để quyết định nhanh, AI không cần dùng toàn bộ chi tiết cấp cá thể. Một dạng trạng thái rút gọn nên gồm:

```text
LaneSummary = {
  lane_id,
  enemy_unit_pressure,
  friendly_unit_pressure,
  enemy_tower_strength,
  friendly_tower_strength,
  breakthrough_risk,
  attack_opportunity
}
```

Với toàn trận:

```text
AISummaryState = {
  ai_base_hp_ratio,
  player_base_hp_ratio,
  ai_resource,
  player_resource,
  lane_summaries[],
  attack_cooldown_ready,
  defense_cooldown_ready,
  time_remaining
}
```

## 7. Tại sao phải sinh tập hành động ứng viên
Nếu xét mọi khả năng:
- mọi loại tháp
- mọi vị trí xây
- mọi cấp nâng cấp
- mọi loại quân
- mọi lane
- mọi tổ hợp wave

thì số lượng hành động sẽ bùng nổ rất nhanh. Điều này không cần thiết cho một bài tập lớn 4 tháng.

### Chiến lược hợp lý
- Chỉ lấy 1 đến 2 lane nguy hiểm nhất để tạo ứng viên phòng thủ.
- Chỉ lấy 1 đến 2 lane yếu nhất của người chơi để tạo ứng viên tấn công.
- Chỉ chọn từ một thư viện wave mẫu nhỏ.
- Chỉ xét nâng cấp cho các tháp đang giữ vai trò chủ lực.

### Ví dụ thư viện ứng viên
- `BUILD_FAST_TOWER(lane_weakest_defense)`
- `BUILD_HEAVY_TOWER(lane_with_tank_enemy)`
- `UPGRADE_BEST_TOWER(lane_most_dangerous)`
- `SEND_FAST_UNIT(lane_enemy_has_slow_towers)`
- `SEND_TANK_UNIT(lane_enemy_lacks_burst_damage)`
- `SEND_CHEAP_SWARM(lane_enemy_resource_low)`
- `SAVE_RESOURCE`

## 8. Utility Function đề xuất

### 8.1. Công thức cơ bản

```text
Utility_AI(action, state) =
    w1 * projected_damage_to_player_base
  + w2 * projected_ai_base_hp_remaining
  + w3 * expected_enemy_units_killed
  + w4 * projected_pressure_on_player
  - w5 * resource_spent
  - w6 * projected_damage_taken_by_ai_base
  - w7 * idle_penalty_when_advantage_exists
```

### 8.2. Ý nghĩa các thành phần
- `projected_damage_to_player_base`: đo lợi ích chiến thắng trực tiếp
- `projected_ai_base_hp_remaining`: ép AI không bỏ thủ
- `expected_enemy_units_killed`: đo hiệu quả trung gian của phòng thủ
- `projected_pressure_on_player`: khuyến khích AI tạo nhịp ép
- `resource_spent`: phạt quyết định lãng phí
- `projected_damage_taken_by_ai_base`: phạt hành động làm hở phòng tuyến
- `idle_penalty_when_advantage_exists`: tránh AI bỏ lỡ cơ hội tấn công

## 9. Ba profile AI mẫu

## 9.1. AI phòng thủ
Trọng số gợi ý:

```text
w1=2, w2=5, w3=4, w4=2, w5=2, w6=5, w7=1
```

Đặc trưng:
- xây và nâng cấp nhiều
- chỉ phản công khi an toàn
- khó bị vỡ lane sớm nhưng có thể thiếu đột biến

## 9.2. AI tấn công
Trọng số gợi ý:

```text
w1=5, w2=2, w3=2, w4=5, w5=1, w6=3, w7=3
```

Đặc trưng:
- gây áp lực liên tục
- tiêu tiền mạnh vào wave
- có thể thắng sớm hoặc tự hở phòng thủ

## 9.3. AI cân bằng
Trọng số gợi ý:

```text
w1=4, w2=4, w3=3, w4=3, w5=2, w6=4, w7=2
```

Đặc trưng:
- chuyển trạng thái theo tình hình
- phù hợp làm profile mặc định

## 10. Tạo nhiều độ khó AI

### Dễ
- Ít luật
- Tập ứng viên nhỏ
- Không nhìn xa
- Có ngưỡng phản ứng chậm hơn

### Trung bình
- Có phân tích lane
- Có utility cân bằng
- Có chọn wave theo tình huống đơn giản

### Khó
- Có nhiều rule ngữ cảnh
- Có utility đầy đủ
- Có thể thêm lookahead một bước
- Phản ứng nhanh và phân bổ tài nguyên hợp lý hơn

## 11. Pipeline ra quyết định đề xuất

### Bước 1. Cập nhật trạng thái trận đấu
- đọc `GameState`
- chuẩn hóa dữ liệu thành `AISummaryState`

### Bước 2. Phân tích nguy cơ phòng thủ của AI
- lane nào có `breakthrough_risk` cao
- lane nào gần căn cứ bị áp lực mạnh

### Bước 3. Phân tích điểm yếu của người chơi
- lane nào có `enemy_tower_strength` thấp
- lane nào dễ tạo sát thương lên căn cứ

### Bước 4. Sinh danh sách hành động ứng viên
- 2 đến 3 hành động phòng thủ
- 2 đến 3 hành động tấn công
- 1 hành động tiết kiệm

### Bước 5. Chấm điểm từng hành động
- dùng heuristic rule
- dùng utility function
- nếu có thể, mô phỏng ngắn hạn một bước

### Bước 6. Chọn hành động tốt nhất
- chọn action có điểm cao nhất
- nếu chênh lệch điểm nhỏ, có thể ưu tiên hành động rẻ hơn hoặc an toàn hơn

### Bước 7. Thực thi hành động
- kiểm tra tài nguyên
- kiểm tra cooldown
- cập nhật trạng thái

### Bước 8. Ghi log
- action đã chọn
- điểm số action
- trạng thái lane trước và sau
- thời gian tính toán

## 12. Ví dụ luật heuristic cụ thể
- Nếu người chơi có nhiều tháp nặng và ít tháp nhanh ở lane 2, ưu tiên `SEND_FAST_UNIT(lane_2)`.
- Nếu lane 1 của AI có `breakthrough_risk > 0.8`, ưu tiên `BUILD_OR_UPGRADE_DEFENSE(lane_1)`.
- Nếu căn cứ người chơi còn dưới 30 phần trăm máu và lane 3 phòng thủ yếu, ưu tiên `ALL_IN_ATTACK(lane_3)`.
- Nếu AI có trên 70 phần trăm máu căn cứ và nhiều tài nguyên hơn người chơi, cho phép mở rộng tập ứng viên tấn công.
- Nếu mọi lane đều ổn định và không có cơ hội rõ, chọn `SAVE_RESOURCE`.

## 13. Khuyến nghị triển khai thực tế
- Bắt đầu từ rule-based đơn giản trước.
- Sau khi game loop ổn định mới thêm utility chấm điểm.
- Không viết AI trực tiếp phụ thuộc vào UI.
- Tách `AIAgent` và `HeuristicEvaluator` thành module riêng để dễ so sánh nhiều profile AI.
- Ghi log mọi quyết định từ đầu để tránh thiếu dữ liệu khi viết báo cáo.
