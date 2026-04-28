# Thực nghiệm, chỉ số và đánh giá

## 1. Mục tiêu đánh giá
Đề tài chỉ có giá trị học thuật rõ ràng nếu AI được đánh giá bằng số liệu cụ thể, thay vì chỉ demo cảm tính. Vì vậy, phần thực nghiệm phải được xem là bắt buộc.

## 2. Bộ tiêu chí định lượng

## 2.1. Tỷ lệ thắng của AI
- Định nghĩa: số trận AI thắng chia tổng số trận
- Ý nghĩa: thước đo tổng quát nhất

## 2.2. Máu căn cứ còn lại
- Ghi `HP còn lại của AI`
- Ghi `HP còn lại của người chơi`
- Ý nghĩa: phản ánh mức độ áp đảo hoặc mong manh của chiến thắng

## 2.3. Sát thương gây lên căn cứ đối phương
- Đo tổng damage AI gây lên căn cứ người chơi
- Ý nghĩa: phản ánh hiệu quả tấn công

## 2.4. Số quân tiêu diệt
- Đo số đơn vị đối phương bị hạ
- Có thể tách theo lane hoặc theo loại quân
- Ý nghĩa: phản ánh hiệu quả phòng thủ

## 2.5. Số tài nguyên sử dụng
- Ghi tổng tài nguyên đã tiêu
- Có thể tách `xây tháp`, `nâng cấp`, `gửi quân`
- Ý nghĩa: cơ sở để tính hiệu quả tài nguyên

## 2.6. Hiệu quả tài nguyên
Ví dụ:

```text
resource_efficiency = total_damage_to_enemy_base / total_resource_spent
```

Có thể mở rộng:

```text
combat_efficiency = (enemy_units_killed + damage_to_enemy_base_weighted) / total_resource_spent
```

## 2.7. Thời gian tính toán mỗi quyết định
- Đo bằng mili giây
- Ghi trung bình, lớn nhất và nhỏ nhất
- Ý nghĩa: kiểm tra khả năng chạy thời gian thực

## 2.8. Tần suất hành vi công và thủ
- Số lần AI chọn hành động phòng thủ
- Số lần AI chọn hành động tấn công
- Số lần AI chọn tiết kiệm
- Ý nghĩa: giúp giải thích phong cách AI

## 2.9. Chỉ số lane
- Số lần lane bị thủng
- Lane nào thường bị bỏ qua
- Lane nào thường là hướng tấn công chủ đạo
- Ý nghĩa: giúp phân tích điểm yếu chiến thuật

## 3. Bộ thí nghiệm so sánh

### 3.1. Random AI
- Chọn hành động ngẫu nhiên trong tập hợp hợp lệ
- Dùng làm baseline thấp nhất

### 3.2. Rule-based AI
- Dùng luật đơn giản, không chấm utility sâu
- Dùng làm baseline có logic

### 3.3. Heuristic AI
- Dùng rule để sinh ứng viên
- Dùng utility để chọn hành động tốt nhất

### 3.4. Heuristic + one-step lookahead
- Mô phỏng ngắn một bước sau hành động
- So sánh với heuristic thuần

### 3.5. Tùy chọn nếu còn thời gian
- Minimax AI
- Genetic AI
- Hill-climbing tuned AI

## 4. Kịch bản thực nghiệm đề xuất

## 4.1. Kịch bản 1: người chơi phòng thủ mạnh một lane
- Mục tiêu: xem AI có chuyển hướng tấn công lane khác không

## 4.2. Kịch bản 2: người chơi tấn công sớm
- Mục tiêu: xem AI có phản ứng phòng thủ hợp lý không

## 4.3. Kịch bản 3: người chơi tiết kiệm tài nguyên
- Mục tiêu: xem AI có tận dụng thời điểm cửa sổ yếu để gây áp lực không

## 4.4. Kịch bản 4: trận cân bằng thông thường
- Mục tiêu: so sánh hiệu quả chung giữa các profile AI

## 4.5. Kịch bản 5: AI ở thế bất lợi tài nguyên
- Mục tiêu: xem AI có chơi tiết kiệm và phòng thủ hiệu quả không

## 5. Thiết kế bảng thực nghiệm

| Mô hình AI | Số trận | Tỷ lệ thắng | HP AI còn lại TB | Damage lên base người chơi TB | Tài nguyên tiêu TB | Hiệu quả tài nguyên | Thời gian quyết định TB |
|---|---:|---:|---:|---:|---:|---:|---:|
| Random AI | 30 |  |  |  |  |  |  |
| Rule-based AI | 30 |  |  |  |  |  |  |
| Heuristic AI | 30 |  |  |  |  |  |  |
| Heuristic + lookahead | 30 |  |  |  |  |  |  |
| Optional: Minimax hoặc GA | 30 |  |  |  |  |  |  |

## 6. Bảng phân tích hành vi

| Mô hình AI | Số lần phòng thủ TB | Số lần tấn công TB | Số lần tiết kiệm TB | Lane tấn công chủ đạo | Lane bị thủng nhiều nhất |
|---|---:|---:|---:|---|---|
| Rule-based |  |  |  |  |  |
| Heuristic phòng thủ |  |  |  |  |  |
| Heuristic cân bằng |  |  |  |  |  |
| Heuristic tấn công |  |  |  |  |  |

## 7. Kịch bản chạy thí nghiệm
- Mỗi cấu hình AI nên chạy nhiều trận, ví dụ 30 trận hoặc hơn.
- Nếu có yếu tố ngẫu nhiên, dùng nhiều seed khác nhau.
- Giữ nguyên luật chơi và bản đồ khi so sánh giữa các AI.
- Chỉ thay đổi một yếu tố tại một thời điểm để dễ kết luận.

## 8. Điều cần ghi trong log
- `match_id`
- `seed`
- `ai_profile`
- `map_type`
- `match_duration`
- `winner`
- `player_base_hp_end`
- `ai_base_hp_end`
- `damage_to_player_base`
- `damage_to_ai_base`
- `enemy_units_killed`
- `friendly_units_lost`
- `resource_spent_on_towers`
- `resource_spent_on_units`
- `decision_time_ms_avg`
- `attack_action_count`
- `defense_action_count`
- `economy_action_count`

## 9. Cách trình bày kết quả
- Dùng bảng để so sánh tổng hợp.
- Dùng biểu đồ cột cho tỷ lệ thắng và hiệu quả tài nguyên.
- Dùng biểu đồ đường hoặc thanh ngang cho tần suất hành vi công và thủ.
- Có phần nhận xét định tính ngắn cho từng profile AI.

## 10. Kết luận đánh giá nên hướng tới
Một kết quả tốt cho bài tập lớn không nhất thiết là AI bất bại. Kết quả tốt là:
- AI heuristic thắng random AI rõ ràng
- AI các profile có hành vi khác nhau và giải thích được
- thời gian ra quyết định đủ thấp
- có số liệu đủ để chứng minh lựa chọn thuật toán là hợp lý
