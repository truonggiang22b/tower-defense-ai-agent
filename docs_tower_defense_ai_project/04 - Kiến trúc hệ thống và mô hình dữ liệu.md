# Kiến trúc hệ thống và mô hình dữ liệu

## 1. Mục tiêu thiết kế
Kiến trúc cần đủ đơn giản để nhóm 3 người triển khai trong 4 tháng, nhưng vẫn đủ rõ để:

- tách phần gameplay khỏi phần AI
- hỗ trợ nhiều profile AI
- ghi log và chạy thực nghiệm
- không phụ thuộc chặt vào một engine cụ thể

## 2. Nguyên tắc thiết kế
- `GameState` là nguồn sự thật trung tâm.
- `AIAgent` chỉ đọc trạng thái và trả về `Action`, không tự ý sửa logic gameplay.
- `GameLogger` chạy xuyên suốt từ sớm, không bổ sung vào cuối kỳ.
- Mọi quyết định chiến thuật nên có thể tái hiện từ log.

## 3. Kiến trúc module đề xuất

## 3.1. GameEngine
### Trách nhiệm
- Điều phối game loop chính
- Cập nhật tick hoặc frame logic
- Gọi các subsystem theo đúng thứ tự
- Kiểm tra điều kiện thắng thua

### Phụ thuộc chính
- `MapManager`
- `ResourceManager`
- `TowerManager`
- `UnitManager`
- `CombatSystem`
- `AIAgent`
- `GameLogger`
- `UIManager`

## 3.2. MapManager
### Trách nhiệm
- Tạo và lưu cấu trúc lane hoặc grid
- Quản lý build slot
- Cung cấp thông tin vị trí hợp lệ cho tháp
- Trả dữ liệu đường đi cho quân

## 3.3. ResourceManager
### Trách nhiệm
- Cộng tài nguyên theo thời gian
- Trừ tài nguyên khi thực hiện hành động
- Cộng thưởng khi kích hoạt sự kiện thưởng
- Kiểm tra đủ tiền cho hành động

## 3.4. TowerManager
### Trách nhiệm
- Tạo tháp mới
- Nâng cấp tháp
- Quản lý cooldown bắn
- Chọn mục tiêu cho tháp

## 3.5. UnitManager
### Trách nhiệm
- Sinh quân
- Cập nhật vị trí quân
- Xóa quân chết hoặc quân tới căn cứ
- Quản lý đội hình wave nếu có

## 3.6. CombatSystem
### Trách nhiệm
- Xử lý tháp tấn công quân
- Xử lý sát thương lên căn cứ
- Tính toán tiêu diệt đơn vị
- Gửi sự kiện cho `ResourceManager` và `GameLogger`

## 3.7. PathfindingSystem
### Trách nhiệm
- Tìm đường đi cho quân nếu dùng map lưới
- Cung cấp đường đi hợp lệ hoặc tối ưu
- Không cần bật ở MVP lane cố định

## 3.8. AIAgent
### Trách nhiệm
- Đọc `GameState`
- Tạo trạng thái rút gọn phục vụ suy luận
- Sinh hành động ứng viên
- Chấm điểm và chọn hành động
- Trả về `Action`

## 3.9. HeuristicEvaluator
### Trách nhiệm
- Chấm điểm từng hành động
- Tính lane danger, lane opportunity
- Tính utility hoặc expected value
- Có thể chứa nhiều profile trọng số

## 3.10. GameLogger
### Trách nhiệm
- Ghi trạng thái theo tick hoặc theo sự kiện
- Ghi hành động của AI và người chơi
- Ghi số liệu cuối trận
- Hỗ trợ xuất dữ liệu cho thí nghiệm

## 3.11. UIManager
### Trách nhiệm
- Hiển thị lane, căn cứ, tháp, quân
- Hiển thị tài nguyên, máu căn cứ, thời gian
- Hiển thị nút thao tác cho người chơi
- Hiển thị kết quả trận và thống kê cơ bản

## 4. Class chính đề xuất

## 4.1. GameState
### Dữ liệu chính
- `player_base`
- `ai_base`
- `player_resource`
- `ai_resource`
- `player_towers`
- `ai_towers`
- `active_units`
- `lanes`
- `match_time`
- `cooldowns`
- `wave_state`

### Vai trò
- Đại diện chuẩn hóa cho toàn bộ trận đấu
- Là đầu vào chính của AI và logger

## 4.2. Base
### Dữ liệu chính
- `owner`
- `hp`
- `max_hp`
- `position`

### Hành vi
- `take_damage(amount)`
- `is_destroyed()`

## 4.3. Tower
### Dữ liệu chính
- `tower_type`
- `level`
- `damage`
- `range`
- `attack_interval`
- `lane_id`
- `position`
- `owner`

### Hành vi
- `can_attack(target)`
- `select_target(units)`
- `attack(target)`
- `upgrade()`

## 4.4. Unit
### Dữ liệu chính
- `unit_type`
- `hp`
- `speed`
- `damage_to_base`
- `lane_id`
- `position`
- `owner`

### Hành vi
- `move(delta_time)`
- `take_damage(amount)`
- `reached_base()`

## 4.5. Lane
### Dữ liệu chính
- `lane_id`
- `path_points`
- `build_slots`
- `length`

### Hành vi
- `get_spawn_point(owner)`
- `get_base_target(owner)`
- `is_build_slot_available(slot_id)`

## 4.6. MapCell
### Dữ liệu chính
- `x`
- `y`
- `cell_type`
- `movement_cost`
- `buildable`
- `occupied`

### Hành vi
- `is_walkable()`
- `is_buildable()`

## 4.7. Action
### Dữ liệu chính
- `action_type`
- `actor`
- `target_lane`
- `target_position`
- `entity_type`
- `cost`
- `metadata`

### Hành vi
- `is_valid(game_state)`
- `execute(game_state)`

## 4.8. AIAgent
### Dữ liệu chính
- `profile_name`
- `weights`
- `rule_set`

### Hành vi
- `observe(game_state)`
- `build_summary(game_state)`
- `generate_candidate_actions(summary_state)`
- `decide_action(game_state)`

## 4.9. HeuristicEvaluator
### Dữ liệu chính
- `weights`
- `thresholds`

### Hành vi
- `score(action, game_state)`
- `estimate_lane_danger(lane_state)`
- `estimate_attack_opportunity(lane_state)`

## 5. Interface logic nên chốt sớm

```text
AIAgent.decide_action(game_state) -> Action
HeuristicEvaluator.score(action, game_state) -> float
PathfindingSystem.find_path(start, goal, map_state) -> path
GameLogger.record_tick(snapshot, action, metrics)
```

## 6. Luồng dữ liệu chính
1. `GameEngine` cập nhật thời gian và tài nguyên.
2. Người chơi gửi hành động vào hệ thống.
3. `AIAgent` đọc `GameState` và trả về `Action`.
4. `GameEngine` kiểm tra hợp lệ và thực thi hành động.
5. `UnitManager` và `TowerManager` cập nhật trạng thái.
6. `CombatSystem` tính sát thương và loại bỏ đơn vị.
7. `GameLogger` ghi snapshot, action và metrics.
8. `UIManager` render trạng thái mới.

## 7. Dữ liệu tối thiểu cần log
- thời gian tick
- tài nguyên hai bên
- HP căn cứ hai bên
- số lượng tháp theo lane
- số lượng quân theo loại và lane
- hành động AI đã chọn
- điểm heuristic của hành động
- kết quả trận

## 8. Cách phối hợp giữa 3 thành viên
- Thành viên 1 làm `GameEngine`, `UIManager`, một phần `MapManager`
- Thành viên 2 làm `UnitManager`, `TowerManager`, `CombatSystem`, `PathfindingSystem`
- Thành viên 3 làm `AIAgent`, `HeuristicEvaluator`, `GameLogger`, batch evaluation

### Các hợp đồng phải thống nhất sớm
- schema của `GameState`
- enum các `action_type`
- cấu trúc `LaneSummary` cho AI
- format log xuất ra

## 9. Khuyến nghị kỹ thuật
- Tách logic gameplay khỏi render.
- Dùng dữ liệu cấu hình cho loại tháp và loại quân thay vì hard-code rải rác.
- Đảm bảo có thể chạy mô phỏng tự động không cần thao tác UI để phục vụ thực nghiệm.
- Nếu thiếu thời gian, ưu tiên giao diện đủ dùng và log tốt hơn là kiến trúc quá cầu kỳ.
