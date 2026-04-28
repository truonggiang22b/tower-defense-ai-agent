# Roadmap 4 tháng, rủi ro và sản phẩm bàn giao

## 1. Mục tiêu quản trị đề tài
Tài liệu này giúp nhóm kiểm soát tiến độ và tránh đi lệch hướng. Với đề tài game có AI, rủi ro lớn nhất không phải là không biết làm gì, mà là làm quá nhiều thứ không cần thiết.

## 2. Roadmap 4 tháng theo tháng

## Tháng 1: Chốt luật và dựng lõi mô phỏng
### Mục tiêu
- Chốt luật chơi tối thiểu
- Chốt bản đồ lane cố định
- Xây nền tảng vòng lặp game

### Đầu ra bắt buộc
- Có `GameState` sơ bộ
- Có căn cứ hai bên
- Có tài nguyên tăng theo thời gian
- Có lane và build slot
- Có ít nhất 1 loại tháp và 1 loại quân để test loop
- Có quân di chuyển tới căn cứ

### Việc nên hoàn thành
- Tài liệu luật chơi ngắn
- Danh sách loại tháp và loại quân
- Mock log cơ bản

## Tháng 2: Hoàn thiện gameplay cốt lõi
### Mục tiêu
- Hoàn thiện combat
- Mở rộng nội dung đủ cho MVP
- Tạo baseline AI

### Đầu ra bắt buộc
- Có 2 đến 3 loại tháp
- Có 2 đến 3 loại quân
- Có nâng cấp tháp
- Có AI random
- Có AI rule-based đơn giản
- Có log trận đấu

### Việc nên hoàn thành
- UI đủ thao tác
- Có màn hình thắng thua
- Có thống kê cuối trận cơ bản

## Tháng 3: Tập trung vào AI và đánh giá
### Mục tiêu
- Xây AI heuristic
- Tạo các profile AI
- Tinh chỉnh utility function

### Đầu ra bắt buộc
- Có `HeuristicEvaluator`
- Có AI phòng thủ, AI tấn công, AI cân bằng
- Có so sánh Random vs Rule-based vs Heuristic
- Nếu dùng map lưới, hoàn thành A* trong tháng này

### Việc nên hoàn thành
- Có batch simulation
- Có xuất dữ liệu thí nghiệm
- Có one-step lookahead nếu còn thời gian

## Tháng 4: Thực nghiệm, báo cáo và demo
### Mục tiêu
- Chạy thí nghiệm
- Viết báo cáo
- Chuẩn bị demo

### Đầu ra bắt buộc
- Bảng thực nghiệm hoàn chỉnh
- Báo cáo và slide
- Demo game chạy được
- Kịch bản thuyết trình

### Việc nên hoàn thành
- Video demo ngắn
- Giao diện trực quan hơn
- Dọn code và đóng gói source

## 3. Roadmap ngắn theo tuần

### Tuần 1 đến 2
- Chốt đề tài
- Chốt luật chơi
- Chốt `GameState`, `Action`, `Lane`

### Tuần 3 đến 4
- Dựng `GameEngine`
- Dựng lane và căn cứ
- Tạo vòng lặp tài nguyên và di chuyển cơ bản

### Tuần 5 đến 6
- Hoàn thiện tháp và combat
- Thêm tháp và quân mẫu

### Tuần 7 đến 8
- AI random và rule-based
- Logger cơ bản

### Tuần 9 đến 10
- HeuristicEvaluator
- Profile AI đầu tiên

### Tuần 11 đến 12
- Tinh chỉnh AI
- A* nếu cần
- So sánh nhiều profile

### Tuần 13 đến 14
- Chạy thực nghiệm
- Thu số liệu và làm bảng

### Tuần 15 đến 16
- Viết báo cáo
- Làm slide
- Tập demo

## 4. Phân công 3 thành viên

## Thành viên 1: Game engine và UI
### Phụ trách
- `GameEngine`
- `UIManager`
- một phần `MapManager`
- vòng lặp game
- màn hình thao tác và hiển thị

### Kết quả phải bàn giao
- game chạy được
- người chơi thao tác được
- UI hiển thị đủ thông tin

## Thành viên 2: Gameplay, combat, pathfinding
### Phụ trách
- `UnitManager`
- `TowerManager`
- `CombatSystem`
- `PathfindingSystem` nếu có grid
- cấu hình tháp và quân

### Kết quả phải bàn giao
- quân di chuyển đúng
- tháp bắn đúng
- combat ổn định
- A* hoạt động nếu là phần mở rộng

## Thành viên 3: AI, heuristic, evaluation
### Phụ trách
- `AIAgent`
- `HeuristicEvaluator`
- `GameLogger`
- script tổng hợp số liệu
- phân tích thực nghiệm

### Kết quả phải bàn giao
- AI random, rule-based, heuristic
- bộ chỉ số và bảng đánh giá
- log đủ để viết báo cáo

## 5. Cách phối hợp để tránh phụ thuộc
- Thống nhất schema `GameState` ngay tuần 1.
- Thống nhất enum `action_type` ngay tuần 1.
- Thành viên gameplay tạo mock state để thành viên AI làm song song.
- Thành viên AI định nghĩa format log sớm để engine bám theo.
- Mỗi tuần có một mốc tích hợp tối thiểu, không chờ đến cuối tháng.

## 6. Rủi ro và cách kiểm soát

## 6.1. Game quá phức tạp
### Rủi ro
- luật chơi nhiều
- nhiều loại tháp và quân
- khó cân bằng và debug

### Giảm thiểu
- chốt lane cố định
- chỉ 2 đến 3 loại tháp và quân
- bỏ cơ chế không phục vụ trực tiếp cho AI

## 6.2. AI không đủ thông minh
### Rủi ro
- hành vi nhìn ngẫu nhiên
- khó chứng minh giá trị học thuật

### Giảm thiểu
- xây baseline random rồi cải tiến dần
- dùng rule-based rõ ràng
- thêm utility function và lane summary
- tập trung AI giải thích được, không theo đuổi AI “rất mạnh”

## 6.3. A* không cần thiết nếu map quá đơn giản
### Rủi ro
- tốn công làm nhưng không tăng giá trị demo

### Giảm thiểu
- chỉ thêm A* khi chọn map lưới nhỏ
- nếu dùng lane cố định, trình bày rõ lý do không dùng A*

## 6.4. Minimax quá nặng
### Rủi ro
- cây trạng thái bùng nổ
- khó kịp tiến độ

### Giảm thiểu
- chỉ làm mở rộng
- giới hạn độ sâu rất nhỏ
- chỉ áp dụng cho pha rời rạc nếu thật sự cần

## 6.5. Genetic Algorithm mất thời gian mô phỏng
### Rủi ro
- cần nhiều trận mô phỏng
- khó ổn định kết quả

### Giảm thiểu
- chỉ cân nhắc sau khi có batch simulation
- nếu chưa có logger ổn, bỏ GA ngay

## 6.6. Cân bằng game khó
### Rủi ro
- AI thắng quá dễ hoặc thua quá dễ
- thực nghiệm thiếu ý nghĩa

### Giảm thiểu
- dùng ít loại thực thể
- điều chỉnh chi phí và chỉ số bằng thực nghiệm nhỏ
- chấp nhận cân bằng ở mức học thuật

## 6.7. Đồ họa tốn thời gian
### Rủi ro
- mất thời gian vào phần không trọng tâm

### Giảm thiểu
- dùng sprite đơn giản hoặc hình khối
- ưu tiên UI rõ hơn đẹp

## 6.8. Không đủ số liệu đánh giá
### Rủi ro
- báo cáo yếu
- khó chứng minh AI tốt hơn baseline

### Giảm thiểu
- hoàn thành logger từ tháng 2
- chạy nhiều trận tự động
- định nghĩa bảng thực nghiệm từ sớm

## 7. Sản phẩm cuối cùng nên nộp
- Source code hoàn chỉnh
- Demo game chạy được
- Báo cáo phân tích bài toán
- Báo cáo giải thuật AI
- Bảng thực nghiệm
- Slide thuyết trình
- Video demo ngắn nếu giảng viên yêu cầu

## 8. Tiêu chí chấp nhận cuối kỳ
- Có game mô phỏng chạy được
- Người chơi đấu được với AI
- AI không hoàn toàn ngẫu nhiên
- Có số liệu so sánh giữa ít nhất 2 mô hình AI
- Có báo cáo giải thích được cách mô hình hóa bài toán
- Có demo ổn định trong thời gian trình bày
