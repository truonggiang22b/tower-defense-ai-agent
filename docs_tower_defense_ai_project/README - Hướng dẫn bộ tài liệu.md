# Bộ tài liệu phân tích đề tài game thủ thành người vs AI

## Mục đích
Bộ tài liệu này phục vụ hai mục tiêu:

1. Giúp nhóm sinh viên chốt phạm vi, kiến trúc, cách mô hình hóa và hướng viết báo cáo.
2. Làm nguồn tham chiếu cho AI Agent trong quá trình phát triển dự án, tránh việc phải phân tích lại từ đầu.

Đây là bộ tài liệu cho một đề tài học thuật môn Nhập môn Trí tuệ nhân tạo. Dự án được định nghĩa là một game 2D thủ thành đối kháng đơn giản giữa người chơi và AI, tập trung vào mô hình hóa bài toán AI thay vì xây dựng sản phẩm thương mại hoàn chỉnh.

## Quyết định cốt lõi đã chốt sẵn
- Tên đề tài khuyến nghị dùng trong báo cáo: `Thiết kế tác tử thông minh cho game thủ thành đối kháng người - AI trong môi trường 2D đơn giản`
- Hướng MVP ưu tiên: bản đồ `lane cố định`
- Hướng AI MVP: `rule-based + heuristic + greedy action selection`
- `A*` chỉ dùng khi nhóm chủ động mở rộng sang bản đồ lưới
- Không đưa `multiplayer online`, `đồ họa 3D`, `học sâu`, `reinforcement learning phức tạp`, `hệ thống tài khoản` vào phạm vi lõi

## Thứ tự đọc khuyến nghị
1. [00 - Phân tích tổng hợp đề tài.md](./00%20-%20Ph%C3%A2n%20t%C3%ADch%20t%E1%BB%95ng%20h%E1%BB%A3p%20%C4%91%E1%BB%81%20t%C3%A0i.md)
2. [01 - Phạm vi và phân tích gameplay.md](./01%20-%20Ph%E1%BA%A1m%20vi%20v%C3%A0%20ph%C3%A2n%20t%C3%ADch%20gameplay.md)
3. [02 - Mô hình hóa AI và thiết kế ra quyết định.md](./02%20-%20M%C3%B4%20h%C3%ACnh%20h%C3%B3a%20AI%20v%C3%A0%20thi%E1%BA%BFt%20k%E1%BA%BF%20ra%20quy%E1%BA%BFt%20%C4%91%E1%BB%8Bnh.md)
4. [03 - Thuật toán AI và đánh đổi.md](./03%20-%20Thu%E1%BA%ADt%20to%C3%A1n%20AI%20v%C3%A0%20%C4%91%C3%A1nh%20%C4%91%E1%BB%95i.md)
5. [04 - Kiến trúc hệ thống và mô hình dữ liệu.md](./04%20-%20Ki%E1%BA%BFn%20tr%C3%BAc%20h%E1%BB%87%20th%E1%BB%91ng%20v%C3%A0%20m%C3%B4%20h%C3%ACnh%20d%E1%BB%AF%20li%E1%BB%87u.md)
6. [05 - Thực nghiệm, chỉ số và đánh giá.md](./05%20-%20Th%E1%BB%B1c%20nghi%E1%BB%87m%2C%20ch%E1%BB%89%20s%E1%BB%91%20v%C3%A0%20%C4%91%C3%A1nh%20gi%C3%A1.md)
7. [06 - Lộ trình, rủi ro và sản phẩm bàn giao.md](./06%20-%20L%E1%BB%99%20tr%C3%ACnh%2C%20r%E1%BB%A7i%20ro%20v%C3%A0%20s%E1%BA%A3n%20ph%E1%BA%A9m%20b%C3%A0n%20giao.md)
8. [07 - Mục lục báo cáo và checklist demo.md](./07%20-%20M%E1%BB%A5c%20l%E1%BB%A5c%20b%C3%A1o%20c%C3%A1o%20v%C3%A0%20checklist%20demo.md)

## Recommended Build Path
Đây là trình tự triển khai khuyến nghị cho cả nhóm và AI Agent:

1. Chốt luật chơi ở mức tối thiểu: 2 căn cứ, 2 đến 3 lane, tài nguyên, tháp, lính, điều kiện thắng thua.
2. Làm bản đồ lane cố định trước để giảm rủi ro về pathfinding.
3. Hoàn thiện game loop cơ bản: sinh quân, di chuyển, bắn, mất máu căn cứ, cộng trừ tài nguyên.
4. Xây AI random và rule-based trước để có baseline.
5. Thêm heuristic evaluator và cơ chế chấm điểm hành động để AI ra quyết định hợp lý hơn.
6. Bổ sung logger và bộ chỉ số đánh giá sớm, không để đến cuối kỳ.
7. Chỉ cân nhắc bản đồ lưới và A* sau khi MVP đã chạy ổn định.
8. Chỉ thêm minimax, GA hoặc RL nếu phần lõi đã hoàn chỉnh và còn nhiều thời gian.

## Nguyên tắc sử dụng bộ tài liệu
- Luôn ưu tiên phần `bắt buộc` trước phần `mở rộng`.
- Nếu thiếu thời gian, bỏ các thuật toán nâng cao trước, không bỏ phần log và đánh giá.
- Khi phát triển code, xem `GameState`, `Action`, `AIAgent`, `HeuristicEvaluator`, `GameLogger` là các hợp đồng lõi cần ổn định sớm.
- Nếu phải chọn giữa giao diện đẹp và số liệu đánh giá tốt, ưu tiên số liệu đánh giá tốt.

## Tóm tắt định hướng học thuật
Điểm mạnh học thuật của đề tài không nằm ở đồ họa hay độ lớn của game, mà nằm ở:

- Mô hình hóa tác tử cạnh tranh trong môi trường động.
- Biểu diễn trạng thái và rút gọn trạng thái.
- Xây dựng không gian hành động và chiến lược sinh ứng viên.
- Thiết kế hàm utility và heuristic.
- So sánh nhiều chiến lược AI bằng số liệu định lượng.

## Gợi ý cách dùng cho AI Agent
- Nếu cần viết báo cáo hoặc phân tích tổng quan, bắt đầu từ `00 - Phân tích tổng hợp đề tài.md`.
- Nếu cần làm gameplay, đọc `01 - Phạm vi và phân tích gameplay.md` và `04 - Kiến trúc hệ thống và mô hình dữ liệu.md`.
- Nếu cần làm AI, đọc `02 - Mô hình hóa AI và thiết kế ra quyết định.md` và `03 - Thuật toán AI và đánh đổi.md`.
- Nếu cần làm thí nghiệm và so sánh mô hình, đọc `05 - Thực nghiệm, chỉ số và đánh giá.md`.
- Nếu cần lên kế hoạch nhóm, quản lý rủi ro hoặc chuẩn bị demo, đọc `06 - Lộ trình, rủi ro và sản phẩm bàn giao.md` và `07 - Mục lục báo cáo và checklist demo.md`.
