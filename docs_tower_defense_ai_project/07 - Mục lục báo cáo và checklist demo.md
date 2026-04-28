# Mục lục báo cáo và checklist demo

## 1. Mục tiêu tài liệu
Tài liệu này giúp nhóm hoàn thiện phần nộp cuối kỳ: báo cáo, slide và phần trình bày demo.

## 2. Mục lục báo cáo đề xuất

### 1. Giới thiệu đề tài
- Bối cảnh chọn đề tài
- Mô tả ngắn loại game
- Mục tiêu học thuật

### 2. Lý do chọn đề tài
- Vì sao game là môi trường tốt để áp dụng AI
- Vì sao chọn bài toán thủ thành đối kháng người với AI
- Tính phù hợp với môn Nhập môn Trí tuệ nhân tạo

### 3. Phân tích bài toán
- Mô tả bài toán
- Đầu vào, đầu ra
- Giới hạn phạm vi
- Giả định và đơn giản hóa

### 4. Mô hình hóa tác tử và môi trường
- Tác tử AI
- PEAS
- Thuộc tính môi trường
- Biểu diễn trạng thái
- Không gian hành động

### 5. Thiết kế gameplay
- Luật chơi
- Vòng lặp gameplay
- Thực thể chính
- Bản đồ và lane
- Tài nguyên, tháp, quân, điều kiện thắng thua

### 6. Các thuật toán AI sử dụng
- Rule-based heuristic
- Greedy action selection
- A* nếu có
- Thuật toán mở rộng nếu có
- Utility function và profile AI

### 7. Thiết kế hệ thống
- Kiến trúc module
- Class chính
- Luồng dữ liệu
- Cơ chế log

### 8. Cài đặt
- Công nghệ sử dụng
- Cấu trúc source code
- Minh họa một số đoạn logic chính

### 9. Thực nghiệm và đánh giá
- Kịch bản thực nghiệm
- Chỉ số đánh giá
- Bảng kết quả
- Phân tích kết quả

### 10. Kết luận và hướng phát triển
- Kết quả đạt được
- Điểm mạnh và hạn chế
- Hướng mở rộng

## 3. Cấu trúc slide thuyết trình 10 đến 12 slide
1. Tên đề tài và thành viên nhóm
2. Bối cảnh và mục tiêu đề tài
3. Mô tả bài toán
4. Mô hình tác tử và môi trường
5. Gameplay và các thực thể chính
6. Kiến trúc hệ thống
7. Thiết kế AI và utility function
8. Thuật toán sử dụng
9. Kết quả thực nghiệm
10. Demo game
11. Kết luận
12. Hướng phát triển và hỏi đáp

## 4. Checklist nội dung báo cáo
- Có nêu rõ đây là mô phỏng học thuật, không phải sản phẩm production
- Có mô tả đầu vào và đầu ra của bài toán
- Có mô hình PEAS
- Có định nghĩa `GameState`
- Có giải thích không gian hành động của AI
- Có utility function hoặc heuristic
- Có mô tả thuật toán bắt buộc đã dùng
- Có bảng thực nghiệm
- Có so sánh với baseline
- Có kết luận về ưu nhược điểm

## 5. Checklist slide
- Ít chữ, nhiều ý chính
- Có hình gameplay hoặc sơ đồ lane
- Có sơ đồ kiến trúc đơn giản
- Có bảng kết quả rút gọn
- Có slide kết luận rõ ràng

## 6. Kịch bản demo 3 đến 5 phút

### Phần 1: Giới thiệu nhanh
- Nêu mục tiêu đề tài
- Nêu trọng tâm là AI công thủ trong game thủ thành đối kháng

### Phần 2: Giải thích luật chơi
- Hai căn cứ
- Xây tháp, nâng cấp, gửi quân
- Tài nguyên tăng theo thời gian
- Điều kiện thắng thua

### Phần 3: Demo một trận ngắn
- Cho người chơi thực hiện vài hành động
- Chỉ ra AI đang phản ứng thế nào
- Nếu có thể, hiện lane danger hoặc log quyết định AI

### Phần 4: Trình bày kết quả thí nghiệm
- So sánh Random AI với Heuristic AI
- Nêu tỷ lệ thắng hoặc hiệu quả tài nguyên

### Phần 5: Kết luận
- Nhấn mạnh bài toán AI đã được mô hình hóa rõ
- Nhấn mạnh dự án khả thi trong phạm vi môn học

## 7. Checklist demo kỹ thuật
- Game chạy ổn định từ đầu đến cuối trận
- Không cần internet
- Có sẵn cấu hình demo dễ tái hiện
- Có sẵn một kịch bản dự phòng nếu game lỗi
- Có sẵn ảnh chụp màn hình hoặc video dự phòng

## 8. Những điều nên tránh khi trình bày
- Không nói dự án là game thương mại hoàn chỉnh
- Không dành quá nhiều thời gian nói về đồ họa
- Không giới thiệu quá nhiều thuật toán chưa triển khai thật
- Không dùng kết luận cảm tính nếu không có số liệu đi kèm

## 9. Thông điệp kết thúc nên nhấn mạnh
- Nhóm đã xây được một môi trường game mô phỏng có AI đối kháng.
- AI được mô hình hóa bằng trạng thái, hành động, heuristic và utility rõ ràng.
- Dự án chứng minh được khả năng áp dụng thuật toán AI nhập môn vào bài toán game cụ thể.
