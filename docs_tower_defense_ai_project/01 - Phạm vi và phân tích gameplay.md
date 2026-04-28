# Phạm vi đề tài và phân tích gameplay

## 1. Mục tiêu tài liệu
Tài liệu này chốt phạm vi thực thi và mô hình gameplay ở mức đủ để nhóm có thể bắt đầu xây dựng game ngay, đồng thời giữ đúng mục tiêu của môn Nhập môn Trí tuệ nhân tạo.

## 2. Định hướng sản phẩm
- Loại sản phẩm: game mô phỏng học thuật 2D
- Kiểu chơi: thủ thành đối kháng người với AI
- Trọng tâm: mô hình hóa và đánh giá AI
- Không phải: dự án thương mại, clone đầy đủ game gốc, game online nhiều người chơi

## 3. Phạm vi ba mức

### 3.1. MVP bắt buộc
- Bản đồ lane cố định, từ 2 đến 3 lane
- 2 căn cứ: người chơi và AI
- Có tài nguyên tăng theo thời gian
- Có thể thưởng thêm tài nguyên khi hạ quân địch nếu muốn
- Người chơi có thể xây tháp, nâng cấp tháp, gửi quân
- AI có thể xây tháp, nâng cấp tháp, gửi quân
- Tối thiểu 2 đến 3 loại tháp
- Tối thiểu 2 đến 3 loại quân
- Có cơ chế tháp tự bắn quân địch
- Có cơ chế quân di chuyển tới căn cứ đối phương
- Có điều kiện thắng thua
- Có logger ghi dữ liệu trận đấu

### 3.2. Nên có nếu còn thời gian
- 3 profile AI khác nhau
- Wave tấn công gồm nhiều đơn vị
- Bảng thống kê cuối trận
- Hiệu ứng hoặc UI rõ ràng hơn
- Lookahead một bước khi chấm điểm hành động
- Bản đồ lưới nhỏ để trình diễn A*

### 3.3. Không làm
- Multiplayer online
- PvP qua mạng
- Đồ họa 3D
- Hệ thống tài khoản
- Shop, inventory, progression dài hạn
- Map editor
- Học sâu hoặc RL phức tạp
- Cân bằng thương mại và nội dung phong phú như game thật

## 4. Khuyến nghị bản đồ MVP
Nên chọn `lane cố định` cho MVP.

### Lý do
- Luật chơi rõ, dễ debug
- Tiết kiệm thời gian hơn bản đồ lưới
- Vẫn đủ cho AI ra quyết định:
  - lane nào cần thủ
  - lane nào nên tấn công
  - nên xây hay nâng cấp
  - nên tung quân nào
- Phù hợp với nhóm 3 người trong 4 tháng

## 5. Vòng lặp gameplay chính
Gameplay được mô hình hóa theo chu kỳ sau:

1. Hệ thống cập nhật thời gian trận đấu.
2. Cộng tài nguyên định kỳ cho hai bên.
3. Người chơi quan sát trạng thái các lane, tài nguyên và căn cứ.
4. Người chơi thực hiện một hành động nếu đủ tài nguyên và không vướng cooldown.
5. AI quan sát `GameState` tại cùng thời điểm.
6. AI sinh danh sách hành động ứng viên.
7. AI chấm điểm và chọn một hành động.
8. Quân hai bên di chuyển trên lane.
9. Tháp hai bên khóa mục tiêu và tấn công quân địch trong tầm.
10. Quân tới được căn cứ sẽ gây sát thương lên căn cứ đối phương.
11. Đơn vị bị hạ sẽ bị loại khỏi trạng thái trận đấu và có thể tạo thưởng tài nguyên.
12. Kiểm tra điều kiện kết thúc trận.

## 6. Thực thể chính

## 6.1. PlayerBase
### Thuộc tính chính
- `id`
- `hp`
- `max_hp`
- `position`
- `owner = player`

### Hành vi chính
- Nhận sát thương từ quân AI
- Kiểm tra trạng thái sống
- Kích hoạt điều kiện thua khi `hp <= 0`

### Vai trò
- Là mục tiêu mà người chơi phải bảo vệ
- Là căn cứ để hệ thống xác định kết quả trận đấu

## 6.2. AIBase
### Thuộc tính chính
- `id`
- `hp`
- `max_hp`
- `position`
- `owner = ai`

### Hành vi chính
- Nhận sát thương từ quân người chơi
- Kiểm tra trạng thái sống
- Kích hoạt điều kiện thua của AI khi `hp <= 0`

### Vai trò
- Là đối tượng trọng tâm để AI bảo vệ
- Là căn cứ để đo hiệu quả chiến thuật của người chơi

## 6.3. Tower
### Thuộc tính chính
- `tower_type`
- `level`
- `damage`
- `range`
- `attack_interval`
- `cost`
- `upgrade_cost`
- `position`
- `lane`
- `owner`

### Hành vi chính
- Tìm mục tiêu trong tầm
- Gây sát thương theo chu kỳ
- Nâng cấp để tăng sức mạnh
- Bị phá nếu hệ thống có thêm cơ chế công phá tháp

### Vai trò
- Trụ cột của phòng thủ
- Công cụ chính để người chơi và AI giữ lane

## 6.4. Unit hoặc Monster
### Thuộc tính chính
- `unit_type`
- `hp`
- `damage_to_base`
- `speed`
- `cost`
- `position`
- `lane`
- `owner`

### Hành vi chính
- Sinh ra ở đầu lane
- Di chuyển tới căn cứ đối phương
- Nhận sát thương từ tháp
- Gây sát thương khi đến căn cứ

### Vai trò
- Nguồn áp lực tấn công
- Yếu tố buộc AI phải cân bằng giữa công và thủ

## 6.5. Resource
### Thuộc tính chính
- `current_amount`
- `income_per_second`
- `kill_reward`

### Hành vi chính
- Tăng theo thời gian
- Trừ khi xây tháp, nâng cấp, gửi quân
- Cộng khi có sự kiện thưởng

### Vai trò
- Ràng buộc tài nguyên của quyết định
- Tạo chiều sâu chiến lược

## 6.6. Lane hoặc Path hoặc MapCell
### Thuộc tính chính
- `lane_id`
- `length`
- `build_slots`
- `danger_score`
- `occupancy_state`

### Hành vi chính
- Xác định đường đi của quân
- Chứa vị trí hợp lệ để xây tháp
- Cung cấp số liệu áp lực cho AI

### Vai trò
- Không gian chiến thuật chính của trò chơi

## 6.7. GameState
### Thuộc tính chính
- `bases`
- `resources`
- `towers`
- `units`
- `lanes`
- `match_time`
- `cooldowns`
- `wave_state`

### Hành vi chính
- Cập nhật theo tick
- Cung cấp thông tin cho AI
- Cung cấp snapshot cho logger và UI

### Vai trò
- Ảnh chụp chuẩn hóa của toàn bộ trận đấu

## 6.8. Action
### Thuộc tính chính
- `action_type`
- `actor`
- `target_lane`
- `target_position`
- `entity_type`
- `cost`
- `cooldown`

### Hành vi chính
- Kiểm tra hợp lệ
- Thực thi và thay đổi trạng thái
- Ghi log kết quả hành động

### Vai trò
- Đơn vị thao tác của hệ thống ra quyết định

## 6.9. Wave hoặc AttackGroup
### Thuộc tính chính
- `wave_id`
- `unit_composition`
- `spawn_schedule`
- `target_lane`

### Hành vi chính
- Sinh nhiều quân theo cấu hình
- Tạo áp lực tập trung hoặc phân tán

### Vai trò
- Trình bày ý tưởng tấn công ở mức chiến thuật thay vì từng đơn vị đơn lẻ

## 7. Luật chơi tối thiểu nên chốt sớm
- Mỗi bên có cùng bộ loại tháp và loại quân.
- Tài nguyên tăng tự động theo thời gian.
- Mỗi hành động đều có chi phí rõ ràng.
- Mỗi tháp có vị trí xây hợp lệ xác định trước.
- Quân không đánh nhau trực tiếp nếu nhóm muốn đơn giản, chỉ bị tháp bắn và tấn công căn cứ.
- Trận đấu có giới hạn thời gian, ví dụ 3 đến 5 phút.
- Nếu hết thời gian, bên có căn cứ còn nhiều máu hơn sẽ thắng.

## 8. Gợi ý bộ loại tháp và quân cho MVP

### Tháp
1. Tháp nhanh
- Sát thương thấp
- Tốc độ bắn cao
- Hiệu quả với quân nhanh, máu thấp

2. Tháp nặng
- Sát thương cao
- Tốc độ bắn chậm
- Hiệu quả với quân trâu

3. Tháp cân bằng
- Chỉ số trung bình
- Dễ dùng cho cả người chơi và AI

### Quân
1. Quân nhanh
- Máu thấp
- Tốc độ cao
- Dùng để vượt tháp bắn chậm

2. Quân trâu
- Máu cao
- Tốc độ thấp
- Dùng để chịu đòn

3. Quân rẻ
- Chi phí thấp
- Có thể spam số lượng
- Dùng để tạo áp lực tài nguyên

## 9. Kết luận phạm vi
Phạm vi hợp lý nhất cho nhóm là:
- Chốt game lane cố định
- Làm AI rule-based và heuristic rõ ràng
- Làm logger và thực nghiệm nghiêm túc
- Nếu thiếu thời gian, giảm đồ họa và bỏ pathfinding nâng cao trước

Tiêu chí thành công của gameplay không phải là đẹp hoặc phong phú, mà là:
- luật chơi dễ hiểu
- trạng thái rõ ràng
- AI có cơ hội thể hiện quyết định chiến thuật
- có thể chạy lặp lại nhiều trận để đánh giá
