# Phân tích tổng hợp đề tài game thủ thành đối kháng người - AI

## 1. Tên đề tài đề xuất

### 1.1. Ba tên đề tài phù hợp
1. Thiết kế tác tử thông minh cho game thủ thành đối kháng người - AI trong môi trường 2D đơn giản
2. Mô hình hóa và xây dựng AI ra quyết định công - thủ cho game thủ thành đối kháng người với máy
3. Ứng dụng heuristic và tác tử thông minh trong game thủ thành đối kháng giữa người chơi và AI

### 1.2. Tên đề tài được chọn
`Thiết kế tác tử thông minh cho game thủ thành đối kháng người - AI trong môi trường 2D đơn giản`

### 1.3. Lý do chọn
- Có tính học thuật, nêu rõ đối tượng nghiên cứu là tác tử thông minh.
- Thể hiện đúng bản chất bài toán là game thủ thành đối kháng người với AI.
- Không phóng đại thành game thương mại.
- Phù hợp để triển khai trong phạm vi môn Nhập môn Trí tuệ nhân tạo.

## 2. Mô tả bài toán
Đề tài hướng tới việc xây dựng một môi trường game 2D đơn giản, trong đó người chơi và AI điều khiển hai căn cứ đối kháng. Mỗi bên có thể sử dụng tài nguyên để xây dựng hoặc nâng cấp tháp phòng thủ, đồng thời tạo đơn vị tấn công để gây áp lực lên căn cứ đối phương. Bài toán AI trung tâm là: từ trạng thái hiện tại của trận đấu, AI phải chọn ra hành động công, thủ hoặc kinh tế hợp lý nhằm tối đa hóa xác suất chiến thắng.

### 2.1. Đầu vào của hệ thống
- Bản đồ trận đấu dạng lane cố định hoặc lưới.
- Thông tin căn cứ người chơi và căn cứ AI: máu, vị trí, trạng thái.
- Lượng tài nguyên hiện tại của mỗi bên.
- Danh sách tháp đã xây: loại tháp, cấp độ, vị trí, máu, tầm bắn.
- Danh sách quân đang tồn tại: loại quân, máu, tốc độ, vị trí, lane.
- Thông tin lane hoặc đường đi.
- Trạng thái trận đấu tại thời điểm hiện tại: thời gian, cooldown, đợt tấn công, áp lực mỗi lane.

### 2.2. Đầu ra hoặc mục tiêu của hệ thống
- AI chọn hành động công, thủ hoặc chờ phù hợp ở mỗi tick hoặc pha quyết định.
- Người chơi có thể tương tác để xây, nâng cấp, gửi quân.
- Trận đấu kết thúc theo điều kiện thắng thua rõ ràng, ví dụ một căn cứ bị phá hoặc hết thời gian.
- Hệ thống sinh log và số liệu để đánh giá chất lượng AI.

### 2.3. Làm rõ phạm vi học thuật
Đây là phiên bản mô phỏng rút gọn phục vụ bài tập lớn học kỳ 4 tháng. Mục tiêu không phải tái hiện đầy đủ game Sinh Tử Môn hay phát triển một sản phẩm production, mà là chứng minh năng lực:

- Phân tích nghiệp vụ gameplay.
- Mô hình hóa tác tử và môi trường.
- Biểu diễn trạng thái và hành động.
- Thiết kế heuristic và utility function.
- Ứng dụng các thuật toán AI đã học vào bài toán cụ thể.

## 3. Phạm vi đề tài

### 3.1. MVP bắt buộc phải có
- Game 2D đơn giản dạng lane hoặc lưới nhỏ.
- Hai căn cứ: người chơi và AI.
- Người chơi có thể xây hoặc nâng cấp tháp, tạo quân tấn công.
- AI có thể tự quyết định xây tháp, nâng cấp tháp, gửi quân.
- Có cơ chế tài nguyên tăng theo thời gian hoặc tăng khi tiêu diệt quân.
- Có ít nhất 2 đến 3 loại tháp.
- Có ít nhất 2 đến 3 loại quân.
- Có điều kiện thắng thua rõ ràng.
- Có hệ thống ghi log và số liệu đánh giá.

### 3.2. Phần nâng cao nên có nếu còn thời gian
- Bản đồ lưới kèm pathfinding bằng BFS, UCS hoặc A*.
- Nhiều profile AI: phòng thủ, tấn công, cân bằng.
- Heuristic có lookahead một bước.
- Minimax độ sâu nhỏ cho các pha ra quyết định rời rạc.
- Tinh chỉnh utility function dựa trên thực nghiệm.
- Giao diện dễ quan sát hơn, hiển thị log và thống kê trong game.

### 3.3. Phần không làm để tránh quá tải
- Multiplayer online.
- Đồ họa 3D hoặc hiệu ứng phức tạp.
- Hệ thống tài khoản, lưu hồ sơ, xếp hạng.
- Map editor phức tạp.
- Học sâu hoặc reinforcement learning phức tạp.
- Cân bằng game ở mức thương mại.
- Nội dung cốt truyện, âm thanh và UI ở mức sản phẩm hoàn thiện.

## 4. Phân tích nghiệp vụ gameplay

### 4.1. Vòng lặp gameplay chính
1. Người chơi quan sát trạng thái trận đấu.
2. Người chơi dùng tài nguyên để xây tháp, nâng cấp hoặc gửi quân.
3. AI quan sát trạng thái trận đấu.
4. AI chọn hành động công, thủ hoặc tiết kiệm.
5. Quân hai bên di chuyển theo lane hoặc đường đi.
6. Tháp tự động tấn công quân địch trong tầm bắn.
7. Quân đến căn cứ đối phương sẽ gây sát thương lên căn cứ.
8. Tài nguyên thay đổi theo thời gian và theo sự kiện, ví dụ hạ quân địch.
9. Trận đấu kết thúc khi một căn cứ bị phá hoặc thời gian hết.

### 4.2. Thực thể chính

#### PlayerBase
- Thuộc tính chính: `hp`, `max_hp`, `position`, `owner`, `resource_income_bonus`
- Hành vi chính: nhận sát thương, kiểm tra trạng thái sống, kích hoạt kết thúc trận
- Vai trò: mục tiêu cần bảo vệ của người chơi

#### AIBase
- Thuộc tính chính: `hp`, `max_hp`, `position`, `owner`, `resource_income_bonus`
- Hành vi chính: nhận sát thương, kiểm tra trạng thái sống
- Vai trò: trung tâm mục tiêu để AI phòng thủ

#### Tower
- Thuộc tính chính: `tower_type`, `level`, `damage`, `range`, `attack_speed`, `cost`, `lane`, `position`, `hp`
- Hành vi chính: tìm mục tiêu, tấn công, nâng cấp, bị phá hủy
- Vai trò: công cụ phòng thủ chính để chặn quân địch

#### Unit hoặc Monster
- Thuộc tính chính: `unit_type`, `hp`, `damage`, `speed`, `cost`, `lane`, `position`, `target_base`
- Hành vi chính: di chuyển, nhận sát thương, gây sát thương lên căn cứ
- Vai trò: lực lượng tấn công tạo áp lực lên đối phương

#### Resource
- Thuộc tính chính: `current_amount`, `income_rate`, `kill_reward_rule`
- Hành vi chính: tăng theo thời gian, cộng thưởng, trừ khi mua hành động
- Vai trò: ràng buộc quyết định chiến thuật

#### Lane hoặc Path hoặc MapCell
- Thuộc tính chính: `lane_id`, `cells`, `length`, `build_slots`, `danger_score`
- Hành vi chính: xác định vị trí xây tháp, đường di chuyển, đánh giá áp lực
- Vai trò: cấu trúc không gian của trận đấu

#### GameState
- Thuộc tính chính: toàn bộ snapshot của bản đồ, căn cứ, tài nguyên, tháp, quân, thời gian, cooldown, wave
- Hành vi chính: cập nhật theo tick, cung cấp dữ liệu cho AI, phục vụ logger
- Vai trò: biểu diễn trạng thái hệ thống để mô phỏng và ra quyết định

#### Action
- Thuộc tính chính: `action_type`, `target_lane`, `target_position`, `entity_type`, `cost`, `priority`
- Hành vi chính: kiểm tra hợp lệ, thực thi, tiêu hao tài nguyên, kích hoạt cooldown
- Vai trò: đơn vị thao tác mà người chơi và AI có thể lựa chọn

#### Wave hoặc AttackGroup
- Thuộc tính chính: `unit_list`, `spawn_time`, `target_lane`, `formation_type`
- Hành vi chính: sinh nhóm quân, đồng bộ áp lực tấn công
- Vai trò: gói hóa hành vi tấn công để AI có thể triển khai chiến thuật rõ ràng hơn

## 5. Mô hình hóa bài toán AI

### 5.1. AI như một tác tử thông minh cạnh tranh
AI là tác tử cạnh tranh trực tiếp với người chơi. Mục tiêu của tác tử không phải tối ưu một bài toán tĩnh, mà liên tục thích nghi với thay đổi của môi trường và hành vi đối phương.

### 5.2. Percepts
AI có thể quan sát:
- Máu căn cứ hai bên.
- Tài nguyên hai bên.
- Số lượng và loại tháp của người chơi và AI.
- Số lượng và loại quân đang tồn tại trên từng lane.
- Lane nào đang mạnh hoặc yếu.
- Cooldown hành động.
- Thời gian trận đấu.
- Áp lực tấn công và nguy cơ thủng phòng tuyến.

### 5.3. Actions
AI có thể:
- Xây tháp ở lane cần phòng thủ.
- Nâng cấp tháp hiện có.
- Gửi một hoặc nhiều loại quân để tấn công.
- Chọn lane để tấn công.
- Tạm thời tiết kiệm tài nguyên.
- Không hành động trong tick hiện tại nếu các lựa chọn khác không hiệu quả.

### 5.4. Performance Measure
Hiệu quả AI được đánh giá qua:
- Khả năng phá căn cứ người chơi.
- Khả năng giữ máu căn cứ AI.
- Khả năng dùng tài nguyên hiệu quả.
- Khả năng tạo áp lực đều hoặc đúng thời điểm.
- Tính ổn định quyết định trong nhiều trận mô phỏng.

### 5.5. Environment
Môi trường game có các đặc điểm:
- Động: trạng thái thay đổi liên tục theo thời gian.
- Tuần tự: quyết định hiện tại ảnh hưởng đến trạng thái tương lai.
- Có ràng buộc thời gian: mỗi quyết định nên được tính nhanh.
- Có tính cạnh tranh: người chơi liên tục phản ứng.
- Quan sát gần như đầy đủ trong phiên bản bài tập lớn.
- Không yêu cầu AI hoàn hảo, nhưng cần hợp lý và giải thích được.

### 5.6. Mô hình PEAS
- Performance Measure: thắng trận, giữ máu căn cứ, gây sát thương, dùng tài nguyên hiệu quả
- Environment: bản đồ, lane, căn cứ, tháp, quân, tài nguyên, thời gian trận
- Actuators: xây tháp, nâng cấp, gửi quân, chọn lane, chờ
- Sensors: snapshot `GameState`, log từng lane, thông tin tài nguyên, trạng thái quân và tháp

## 6. Biểu diễn trạng thái

### 6.1. GameState đầy đủ
Một biểu diễn đủ dùng nên chứa:
- `player_base_hp`
- `ai_base_hp`
- `player_resource`
- `ai_resource`
- `player_towers`
- `ai_towers`
- `active_units`
- `lanes`
- `current_wave`
- `match_time`
- `action_cooldowns`
- `lane_danger_scores`

### 6.2. Rút gọn trạng thái cho AI
Để tránh quá tải:
- Gom mỗi lane thành một vector chỉ số: phòng thủ người chơi, phòng thủ AI, số quân đang tiến, mức áp lực, khả năng thủng.
- Gom quân theo loại và theo lane thay vì theo từng cá thể nếu cần quyết định nhanh.
- Gom tháp theo loại và vị trí chiến lược, ví dụ đầu lane, giữa lane, gần base.
- Chỉ xét một số hành động ứng viên thay vì tất cả tổ hợp có thể.

## 7. Không gian hành động của AI

### 7.1. Hành động phòng thủ
- Xây tháp mới ở lane yếu.
- Nâng cấp tháp đang giữ lane quan trọng.
- Ưu tiên lane có nhiều quân địch hoặc có nguy cơ thủng trong thời gian ngắn.

### 7.2. Hành động tấn công
- Gửi quân nhanh để vượt tháp bắn chậm.
- Gửi quân trâu nếu đối phương thiếu sát thương lớn.
- Gửi quân rẻ theo số đông để bào tài nguyên phòng thủ.
- Gửi quân theo một lane cụ thể để tập trung áp lực.
- Gửi `wave` phối hợp thay vì từng đơn vị lẻ nếu có thời gian làm.

### 7.3. Hành động kinh tế
- Chờ đủ tài nguyên cho một pha mạnh hơn.
- Không tiêu hết tài nguyên vào phòng thủ nếu chưa cần.
- Cân bằng giữa xây thêm tháp và giữ tài nguyên để phản công.

### 7.4. Vì sao không nên xét toàn bộ không gian hành động
Nếu AI xét toàn bộ hành động có thể, số tổ hợp sẽ tăng rất nhanh theo:
- số vị trí xây tháp
- số loại tháp
- số loại quân
- số lane
- số tổ hợp wave
- trạng thái tài nguyên và cooldown

Điều này làm chi phí tính toán tăng cao và khó phù hợp với bài tập lớn. Cách tốt hơn là sinh một tập hành động ứng viên theo ngữ cảnh, ví dụ:
- chỉ xét 1 đến 2 lane nguy hiểm nhất để phòng thủ
- chỉ xét 1 đến 2 lane yếu nhất của đối phương để tấn công
- chỉ xét một số cấu hình wave mẫu
- chỉ xét nâng cấp các tháp chủ lực hiện có

## 8. Hàm đánh giá hoặc Utility Function

### 8.1. Dạng utility đề xuất

```text
Utility_AI =
    w1 * damage_to_player_base
  + w2 * ai_base_hp_remaining
  + w3 * enemy_units_killed
  + w4 * pressure_on_player
  - w5 * resource_spent
  - w6 * damage_taken_by_ai_base
  - w7 * over_defense_penalty
```

### 8.2. Ý nghĩa từng thành phần
- `damage_to_player_base`: phản ánh mục tiêu thắng trận
- `ai_base_hp_remaining`: đảm bảo AI không bỏ mặc phòng thủ
- `enemy_units_killed`: đo hiệu quả phòng thủ trung gian
- `pressure_on_player`: khuyến khích AI ép người chơi phản ứng
- `resource_spent`: ngăn AI tiêu tiền thiếu kiểm soát
- `damage_taken_by_ai_base`: phạt tình huống bị thủng
- `over_defense_penalty`: tránh AI xây quá nhiều mà không phản công

### 8.3. Trọng số ảnh hưởng đến phong cách AI
- Tăng `w1`, `w4` sẽ tạo AI tấn công mạnh
- Tăng `w2`, `w3`, `w6` sẽ tạo AI thiên về phòng thủ
- Tăng `w5` làm AI tiết kiệm hơn
- Tăng `w7` giúp AI tránh lối chơi co cụm quá mức

### 8.4. Tạo nhiều độ khó AI
- Dễ: dùng tập rule nhỏ, trọng số thiên an toàn, quyết định chậm hơn và ít tối ưu hơn
- Trung bình: dùng utility cân bằng, có ưu tiên lane và chọn wave cơ bản
- Khó: dùng heuristic đầy đủ, nhiều rule ngữ cảnh, có thể thêm lookahead một bước

### 8.5. Ba kiểu AI khuyến nghị
- AI phòng thủ: ưu tiên giữ lane, nâng cấp tháp, phản công khi an toàn
- AI tấn công: ưu tiên gây áp lực liên tục, chọn lane yếu của người chơi
- AI cân bằng: chuyển đổi giữa thủ và công theo mức nguy hiểm và cơ hội

## 9. Các giải thuật AI ứng dụng thực tế

### 9.1. Heuristic rule-based decision making
- Dùng ở đâu: quyết định công, thủ, nâng cấp, gửi quân
- Đầu vào: trạng thái tóm tắt của từng lane và tài nguyên
- Đầu ra: danh sách ứng viên hoặc hành động cụ thể
- Ưu điểm: dễ hiểu, dễ giải thích, rất phù hợp môn học
- Nhược điểm: dễ cứng nhắc nếu luật quá đơn giản
- Phù hợp 4 tháng: rất phù hợp
- Rủi ro triển khai: thấp

### 9.2. Greedy hoặc Best-first action selection
- Dùng ở đâu: chọn hành động có điểm utility cao nhất tại mỗi pha
- Đầu vào: tập hành động ứng viên và hàm chấm điểm
- Đầu ra: hành động tốt nhất hiện tại
- Ưu điểm: dễ cài đặt, đủ tốt cho MVP
- Nhược điểm: có thể nhìn ngắn hạn
- Phù hợp 4 tháng: rất phù hợp
- Rủi ro triển khai: thấp

### 9.3. BFS, UCS hoặc A*
- Dùng ở đâu: tìm đường đi cho quân nếu map là lưới
- Đầu vào: ô xuất phát, ô đích, bản đồ và chi phí
- Đầu ra: đường đi hợp lệ hoặc tối ưu
- Ưu điểm: thể hiện rõ kiến thức tìm kiếm
- Nhược điểm: không cần thiết nếu map lane cố định
- Phù hợp 4 tháng: phù hợp nếu chỉ làm grid nhỏ
- Rủi ro triển khai: trung bình

### 9.4. Minimax độ sâu giới hạn
- Dùng ở đâu: pha quyết định rời rạc, ví dụ chọn nhóm hành động trong một khoảng thời gian
- Đầu vào: trạng thái hiện tại, tập hành động AI, mô hình phản ứng người chơi
- Đầu ra: hành động tối ưu theo giả định lookahead
- Ưu điểm: thể hiện rõ tư duy đối kháng
- Nhược điểm: tốn chi phí và phụ thuộc vào mô hình đối thủ
- Phù hợp 4 tháng: chỉ nên làm mở rộng
- Rủi ro triển khai: cao

### 9.5. Alpha-beta pruning
- Dùng ở đâu: tối ưu minimax khi cây quyết định đủ rõ
- Đầu vào: cây quyết định, hàm đánh giá
- Đầu ra: hành động tốt với số nhánh cắt bớt
- Ưu điểm: giảm chi phí so với minimax thuần
- Nhược điểm: vẫn khó nếu game nhiều hành động liên tục
- Phù hợp 4 tháng: không ưu tiên
- Rủi ro triển khai: cao

### 9.6. Hill-climbing hoặc Genetic Algorithm
- Dùng ở đâu: tối ưu cấu hình wave, cấu hình tham số AI hoặc lịch tấn công
- Đầu vào: tập cấu hình ứng viên, hàm fitness
- Đầu ra: cấu hình tốt hơn sau nhiều lần thử
- Ưu điểm: hay về mặt học thuật nếu có mô phỏng batch
- Nhược điểm: tốn thời gian mô phỏng, khó kịp tiến độ
- Phù hợp 4 tháng: chỉ nên làm khi core ổn
- Rủi ro triển khai: cao

### 9.7. CSP đơn giản
- Dùng ở đâu: kiểm tra hành động hợp lệ theo tài nguyên, cooldown, vị trí
- Đầu vào: ràng buộc tài nguyên, lane, vị trí, loại tháp
- Đầu ra: tập hành động hợp lệ
- Ưu điểm: hợp lý nếu muốn mô hình hóa ràng buộc rõ ràng
- Nhược điểm: có thể thừa nếu logic hợp lệ đơn giản
- Phù hợp 4 tháng: mức trung bình
- Rủi ro triển khai: thấp đến trung bình

### 9.8. Q-learning hoặc RL
- Dùng ở đâu: phần mở rộng nghiên cứu
- Đầu vào: trạng thái, reward, hành động
- Đầu ra: chính sách học được
- Ưu điểm: hiện đại
- Nhược điểm: khó huấn luyện, khó đánh giá, lệch trọng tâm môn học nhập môn
- Phù hợp 4 tháng: không ưu tiên
- Rủi ro triển khai: rất cao

## 10. Cách thiết kế AI cụ thể

### 10.1. Pipeline ra quyết định
1. Cập nhật trạng thái trận đấu.
2. Phân tích nguy cơ phòng thủ phía AI.
3. Phân tích điểm yếu phòng thủ của người chơi.
4. Sinh danh sách hành động ứng viên.
5. Chấm điểm từng hành động bằng heuristic hoặc utility.
6. Chọn hành động tốt nhất.
7. Thực thi hành động.
8. Ghi log để phục vụ đánh giá và điều chỉnh.

### 10.2. Ví dụ ra quyết định
- Nếu người chơi có nhiều tháp bắn chậm, AI ưu tiên quân nhanh hoặc quân số đông.
- Nếu người chơi thiếu sát thương lớn, AI ưu tiên quân trâu.
- Nếu một lane phòng thủ yếu, AI tập trung tấn công lane đó.
- Nếu căn cứ AI đang ở mức nguy hiểm, AI ưu tiên xây hoặc nâng cấp tháp phòng thủ.
- Nếu AI có nhiều tài nguyên và người chơi phòng thủ yếu, AI tung đợt tấn công mạnh theo wave.

## 11. Thiết kế bản đồ và gameplay tối giản

### 11.1. Bản đồ lane cố định
- Dễ làm nhất cho MVP.
- Mỗi lane có đường đi xác định sẵn.
- Người chơi và AI chủ yếu ra quyết định ở mức chọn lane, chọn loại tháp, chọn loại quân.
- Vẫn thể hiện AI rõ ở khâu công thủ, phân bổ tài nguyên, chọn mục tiêu và thời điểm.

### 11.2. Bản đồ lưới có tìm đường
- Phức tạp hơn nhưng thể hiện rõ A*.
- Quân phải tìm đường từ điểm sinh đến căn cứ đối phương.
- Có thể thêm ô cản, ô xây tháp và chi phí đường đi khác nhau.

### 11.3. Khuyến nghị
Nên chọn `lane cố định` cho bài tập lớn vì:
- phù hợp thời gian 4 tháng
- giảm rủi ro kỹ thuật
- vẫn đủ đất diễn cho AI
- dễ đánh giá và debug hơn

Nếu chọn lưới, nên giữ kích thước nhỏ như 8x8 hoặc 10x10 và dùng:

```text
f(n) = g(n) + h(n)
```

Trong đó:
- `g(n)` là chi phí đi từ đầu đến nút hiện tại
- `h(n)` là heuristic ước lượng đến đích, ví dụ Manhattan distance

## 12. Thiết kế dữ liệu và class hoặc module

### 12.1. Kiến trúc module
- `GameEngine`: điều phối vòng lặp chính, tick, trạng thái trận
- `MapManager`: quản lý lane, ô bản đồ, vị trí xây dựng, đường đi
- `ResourceManager`: quản lý thu nhập, thưởng, chi phí
- `TowerManager`: sinh tháp, nâng cấp, mục tiêu, trạng thái tháp
- `UnitManager`: sinh quân, di chuyển, cập nhật trạng thái quân
- `CombatSystem`: tính sát thương, va chạm logic, bắn và hủy diệt
- `PathfindingSystem`: tìm đường cho quân khi dùng bản đồ lưới
- `AIAgent`: quan sát và ra quyết định
- `HeuristicEvaluator`: chấm điểm trạng thái hoặc hành động
- `GameLogger`: ghi snapshot và chỉ số
- `UIManager`: hiển thị bản đồ, chỉ số, nút thao tác và kết quả

### 12.2. Class chính
- `GameState`
- `Base`
- `Tower`
- `Unit`
- `Lane`
- `MapCell`
- `Action`
- `AIAgent`
- `HeuristicEvaluator`

### 12.3. Interface logic đề xuất
- `AIAgent.decide_action(game_state) -> Action`
- `HeuristicEvaluator.score(action, game_state) -> float`
- `PathfindingSystem.find_path(start, goal, map_state) -> path`
- `GameLogger.record_tick(snapshot, action, metrics)`

## 13. Đánh giá kết quả

### 13.1. Tiêu chí định lượng
- Tỷ lệ thắng của AI
- Máu căn cứ còn lại
- Sát thương gây lên căn cứ đối phương
- Số quân tiêu diệt
- Số tài nguyên sử dụng
- Hiệu quả tài nguyên = sát thương hoặc áp lực chia cho tài nguyên
- Thời gian tính toán mỗi quyết định
- Số lần AI chọn phòng thủ hoặc tấn công
- So sánh heuristic AI với random AI
- So sánh AI cân bằng với AI tấn công hoặc phòng thủ

### 13.2. Bảng thực nghiệm đề xuất
- Random AI
- Rule-based AI
- Heuristic AI
- Heuristic + lookahead một bước
- Nếu còn thời gian: Minimax hoặc Genetic AI

## 14. Kế hoạch triển khai 4 tháng cho nhóm 3 người

### Tháng 1
- Chốt luật chơi
- Chốt bản đồ lane
- Xây game engine cơ bản
- Có căn cứ, tài nguyên, tháp, quân di chuyển cơ bản

### Tháng 2
- Hoàn thiện combat
- Thêm nhiều loại tháp và quân
- Xây AI random và rule-based
- Bổ sung logger trận đấu

### Tháng 3
- Xây heuristic AI
- Thêm A* nếu nhóm chọn map lưới
- Thử nghiệm utility function
- Tinh chỉnh cân bằng cơ bản

### Tháng 4
- Chạy thực nghiệm
- Hoàn thiện giao diện demo
- Viết báo cáo
- Làm slide và tập demo

### Phân công 3 thành viên
- Thành viên 1: game engine và UI
- Thành viên 2: gameplay, combat, pathfinding
- Thành viên 3: AI, heuristic, evaluation

### Cách phối hợp tránh phụ thuộc
- Chốt schema `GameState` từ tuần đầu
- Làm mock data để thành viên AI có thể phát triển song song
- Chốt format log từ sớm
- Dùng interface ổn định giữa engine và AI

## 15. Rủi ro và cách kiểm soát
- Game quá phức tạp: giảm về lane cố định, ít loại tháp, ít loại quân
- AI không đủ thông minh: chấp nhận AI hợp lý và giải thích được, so với baseline random
- A* không cần thiết nếu map quá đơn giản: chỉ dùng khi có grid
- Minimax quá nặng: chỉ để phần mở rộng
- Genetic Algorithm mất thời gian mô phỏng: bỏ nếu log và heuristic chưa ổn
- Cân bằng game khó: chấp nhận mức cân bằng học thuật, không tối ưu thương mại
- Đồ họa tốn thời gian: dùng sprite đơn giản hoặc hình khối cơ bản
- Không đủ số liệu đánh giá: logger phải hoàn thành từ sớm

## 16. Sản phẩm cuối cùng nên nộp
- Source code
- Demo game chạy được
- Báo cáo phân tích bài toán
- Báo cáo giải thuật AI
- Bảng thực nghiệm
- Slide thuyết trình
- Video demo ngắn nếu giảng viên yêu cầu

## 17. Cấu trúc báo cáo đề xuất
1. Giới thiệu đề tài
2. Lý do chọn đề tài
3. Phân tích bài toán
4. Mô hình hóa tác tử và môi trường
5. Thiết kế gameplay
6. Các thuật toán AI sử dụng
7. Thiết kế hệ thống
8. Cài đặt
9. Thực nghiệm và đánh giá
10. Kết luận và hướng phát triển

## 18. Kết luận
Đề tài này phù hợp với bài tập lớn môn Nhập môn Trí tuệ nhân tạo nếu nhóm giữ đúng trọng tâm học thuật. Giá trị chính của đề tài không nằm ở việc làm một game lớn hay đẹp, mà nằm ở việc chứng minh khả năng mô hình hóa tác tử thông minh, môi trường, trạng thái, hành động, heuristic và hàm đánh giá.

Khuyến nghị cuối cùng:
- Ưu tiên phiên bản đơn giản nhưng chạy được.
- Phải có AI rõ ràng, có log và có số liệu đánh giá.
- Không nên ôm quá nhiều thuật toán nâng cao nếu phần lõi chưa hoàn thiện.
- Hãy xem đây là mô phỏng học thuật có thể giải thích được, không phải sản phẩm production.
