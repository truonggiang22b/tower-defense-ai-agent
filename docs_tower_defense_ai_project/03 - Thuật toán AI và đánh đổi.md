# Thuật toán AI và phân tích đánh đổi

## 1. Mục tiêu tài liệu
Tài liệu này trả lời câu hỏi: nên dùng thuật toán nào, dùng ở đâu, ưu tiên ra sao và rủi ro triển khai thế nào trong khuôn khổ 4 tháng cho nhóm 3 người.

## 2. Nguyên tắc chọn thuật toán
- Chọn thuật toán dễ giải thích và phù hợp với kiến thức môn học.
- Ưu tiên thuật toán giúp AI hành xử hợp lý hơn thay vì thuật toán nghe hiện đại.
- Thuật toán nào không phục vụ rõ cho demo và thực nghiệm thì không nên ôm vào quá sớm.

## 3. Thuật toán bắt buộc

## 3.1. Heuristic rule-based decision making
### Dùng ở đâu
- Điều khiển quyết định công, thủ, nâng cấp, tiết kiệm
- Sinh tập hành động ứng viên

### Đầu vào
- `AISummaryState`
- chỉ số lane
- tài nguyên
- cooldown
- ngưỡng nguy hiểm hoặc cơ hội

### Đầu ra
- danh sách hành động ứng viên hoặc hành động sơ bộ

### Ưu điểm
- Dễ cài đặt
- Dễ giải thích trong báo cáo
- Dễ tinh chỉnh
- Phù hợp với bản đồ lane cố định

### Nhược điểm
- Có thể cứng nhắc
- Phụ thuộc vào chất lượng luật viết tay

### Vì sao phù hợp bài tập lớn 4 tháng
- Cho kết quả nhanh
- Dễ debug
- Có thể dùng ngay từ giai đoạn đầu để tạo baseline

### Mức độ rủi ro
- Thấp

## 3.2. Greedy hoặc Best-first action selection
### Dùng ở đâu
- Chọn hành động tốt nhất trong tập ứng viên tại mỗi pha

### Đầu vào
- danh sách hành động ứng viên
- điểm heuristic hoặc utility của từng hành động

### Đầu ra
- hành động có điểm cao nhất

### Ưu điểm
- Rất phù hợp với game thời gian thực đơn giản
- Chi phí tính toán thấp
- Dễ kết hợp với rule-based

### Nhược điểm
- Dễ tối ưu cục bộ
- Không nhìn xa sâu

### Vì sao phù hợp bài tập lớn 4 tháng
- Đủ mạnh cho MVP
- Dễ kết hợp với logger để so sánh

### Mức độ rủi ro
- Thấp

## 3.3. BFS, UCS hoặc A* cho đường đi
### Dùng ở đâu
- Pathfinding cho quân nếu nhóm chọn map lưới

### Đầu vào
- điểm bắt đầu
- điểm đích
- ma trận bản đồ
- tập ô chặn hoặc chi phí ô

### Đầu ra
- đường đi hợp lệ
- hoặc đường đi tối ưu theo chi phí

### Ưu điểm
- Thể hiện rõ nội dung tìm kiếm cổ điển trong AI
- Tạo điểm nhấn học thuật nếu có map grid

### Nhược điểm
- Không cần thiết nếu dùng lane cố định
- Tốn thêm công thiết kế bản đồ và debug

### Vì sao phù hợp bài tập lớn 4 tháng
- Phù hợp nếu chỉ làm một bản đồ lưới nhỏ và đóng vai trò mở rộng

### Mức độ rủi ro
- Trung bình

## 4. Thuật toán nâng cao nên cân nhắc

## 4.1. Minimax độ sâu giới hạn
### Dùng ở đâu
- Pha quyết định rời rạc theo nhịp, ví dụ mỗi 5 giây AI xét một cây hành động nhỏ

### Đầu vào
- trạng thái trận
- tập hành động AI
- mô hình phản ứng giả định của người chơi
- độ sâu giới hạn

### Đầu ra
- hành động được xem là tốt nhất theo cây quyết định

### Ưu điểm
- Nêu bật bản chất đối kháng
- Có giá trị học thuật cao nếu triển khai được tối giản

### Nhược điểm
- Cần mô hình phản ứng người chơi
- Chi phí tăng nhanh nếu không gian hành động lớn
- Khó áp dụng trực tiếp cho game thời gian thực liên tục

### Vì sao phù hợp hoặc không phù hợp
- Chỉ phù hợp như phần mở rộng sau khi core ổn định

### Mức độ rủi ro
- Cao

## 4.2. Alpha-beta pruning
### Dùng ở đâu
- Tối ưu minimax nếu đã có cây quyết định rõ

### Đầu vào
- cây minimax
- hàm đánh giá

### Đầu ra
- hành động tốt với số nhánh cần duyệt ít hơn

### Ưu điểm
- Giảm số trạng thái phải xét

### Nhược điểm
- Chỉ có ích khi minimax đã được mô hình tốt
- Không giải quyết triệt để độ phức tạp nếu branching factor vẫn lớn

### Vì sao phù hợp hoặc không phù hợp
- Không phù hợp làm phần lõi cho nhóm 3 người trong 4 tháng

### Mức độ rủi ro
- Cao

## 4.3. Hill-climbing
### Dùng ở đâu
- Tìm cấu hình wave hoặc bộ trọng số utility tương đối tốt

### Đầu vào
- cấu hình hiện tại
- tập lân cận
- hàm đánh giá

### Đầu ra
- cấu hình được cải thiện cục bộ

### Ưu điểm
- Dễ hơn GA
- Có thể dùng cho tối ưu tham số nhỏ

### Nhược điểm
- Kẹt cực trị cục bộ
- Phụ thuộc vào cách sinh láng giềng

### Vì sao phù hợp hoặc không phù hợp
- Có thể dùng như một thí nghiệm phụ nếu nhóm muốn tinh chỉnh trọng số

### Mức độ rủi ro
- Trung bình

## 4.4. Genetic Algorithm
### Dùng ở đâu
- Tối ưu cấu hình wave
- Tối ưu profile chiến thuật hoặc bộ trọng số

### Đầu vào
- quần thể cá thể, ví dụ các bộ wave hoặc bộ trọng số
- hàm fitness qua mô phỏng nhiều trận

### Đầu ra
- một cá thể hoặc tập cấu hình tốt hơn sau nhiều thế hệ

### Ưu điểm
- Thú vị về mặt học thuật
- Dễ trình bày trong phần hướng phát triển hoặc mở rộng

### Nhược điểm
- Cần nhiều lượt mô phỏng
- Tốn thời gian và khó ổn định
- Khó kịp tiến độ nếu game loop chưa vững

### Vì sao phù hợp hoặc không phù hợp
- Chỉ nên làm nếu logger, batch simulation và heuristic đã ổn

### Mức độ rủi ro
- Cao

## 4.5. CSP đơn giản
### Dùng ở đâu
- Kiểm tra tính hợp lệ của hành động
- Lọc vị trí đặt tháp hợp lệ
- Lọc tổ hợp không vi phạm tài nguyên và cooldown

### Đầu vào
- tập biến: loại hành động, lane, vị trí, chi phí
- tập ràng buộc: tài nguyên, cooldown, build slot, lane rules

### Đầu ra
- tập hành động hợp lệ

### Ưu điểm
- Biến phần kiểm tra hợp lệ thành mô hình rõ ràng
- Phù hợp khi muốn trình bày bài toán ràng buộc

### Nhược điểm
- Có thể thừa nếu logic hợp lệ đơn giản

### Vì sao phù hợp hoặc không phù hợp
- Phù hợp ở mức vừa phải, đặc biệt nếu nhóm muốn thể hiện thêm một kỹ thuật AI nhẹ

### Mức độ rủi ro
- Thấp đến trung bình

## 5. Thuật toán không bắt buộc

## 5.1. Q-learning hoặc reinforcement learning
### Dùng ở đâu
- Học chính sách điều khiển AI qua nhiều trận

### Đầu vào
- trạng thái
- hành động
- phần thưởng
- nhiều vòng huấn luyện

### Đầu ra
- chính sách hoặc bảng Q

### Ưu điểm
- Hiện đại
- Có thể tạo điểm nhấn nếu làm được

### Nhược điểm
- Dễ lệch trọng tâm môn học nhập môn
- Cần nhiều mô phỏng
- Khó tinh chỉnh reward
- Khó giải thích hơn rule-based và heuristic

### Vì sao phù hợp hoặc không phù hợp
- Không phù hợp cho phần lõi
- Chỉ để mục mở rộng hoặc hướng phát triển

### Mức độ rủi ro
- Rất cao

## 6. Khuyến nghị ưu tiên triển khai

### Mức 1. Phải có
- Rule-based heuristic
- Greedy action selection
- Logger
- So sánh với random AI

### Mức 2. Nên có nếu còn thời gian
- Heuristic + lookahead một bước
- A* nếu dùng grid
- CSP đơn giản để lọc hành động

### Mức 3. Chỉ làm khi phần lõi đã tốt
- Minimax hoặc alpha-beta
- Hill-climbing hoặc GA
- Q-learning hoặc RL

## 7. Bảng tổng hợp mức độ ưu tiên

| Thuật toán | Vai trò | Ưu tiên | Rủi ro |
|---|---|---|---|
| Rule-based heuristic | Quyết định công thủ | Rất cao | Thấp |
| Greedy action selection | Chọn hành động tốt nhất | Rất cao | Thấp |
| BFS/UCS/A* | Tìm đường trên grid | Trung bình | Trung bình |
| CSP đơn giản | Lọc hành động hợp lệ | Trung bình | Thấp |
| Minimax | Lookahead đối kháng | Thấp | Cao |
| Alpha-beta | Tối ưu minimax | Thấp | Cao |
| Hill-climbing | Tinh chỉnh tham số | Thấp | Trung bình |
| Genetic Algorithm | Tối ưu wave hoặc trọng số | Thấp | Cao |
| Q-learning/RL | Học chính sách | Rất thấp | Rất cao |

## 8. Kết luận
Nếu mục tiêu là một bài tập lớn khả thi, có demo chạy được, có số liệu so sánh và thể hiện đúng tinh thần môn học, tổ hợp tốt nhất là:

- `Rule-based heuristic` để sinh và định hướng hành động
- `Greedy` để chọn hành động tốt nhất ở thời điểm hiện tại
- `A*` chỉ thêm khi nhóm thật sự dùng `map grid`

Mọi thuật toán nâng cao khác nên được xem là phần cộng điểm, không phải nền tảng của dự án.
