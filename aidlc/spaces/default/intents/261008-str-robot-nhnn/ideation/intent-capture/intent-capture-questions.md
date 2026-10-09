# Sources

- [desc] Initial description: "Xây dựng robot tự động nhập liệu thông tin báo cáo giao dịch đáng ngờ (STR) trên web portal của NHNN theo luồng: STR_NHNN_ConsumeData_Enqueue -> STR_NHNN_DataEntry_Accuity -> STR_NHNN_TraCuuThue -> STR_NHNN_DataEntry_ALMD -> STR_NHNN_Consume_SendMail. Code tham khảo từ /Users/hainguyen/Projects/RPA_NHAPBAOCAO_STR. Đặc biệt, STR_NHNN_ConsumeData_Enqueue sử dụng code từ src/kafka_consumer.py và src/api_client.py để call API và lấy dữ liệu từ Kafka."
- [scope] Workflow-selected scope: `feature`.

# Questions

## Q1. Business Problem

What specific business problem are we solving with this STR robot?

- A. Tự động hóa việc thu thập và xử lý dữ liệu khách hàng từ Kafka để giảm thiểu công việc thủ công
- B. Tích hợp dữ liệu từ nhiều nguồn (ECM, Accuity, TraCuuThue, ALMD) vào một hệ thống tập trung
- C. Tạo báo cáo giao dịch đáng ngờ (STR) định kỳ và gửi email thông báo
- D. Không rõ - cần phân tích thêm về nghiệp vụ
- E. Khác (vui lòng nêu rõ)
- [Answer]: A. Tự động hóa việc thu thập và xử lý dữ liệu khách hàng từ Kafka để giảm thiểu công việc thủ công

## Q2. Target Customer

Who is the customer (internal/external) and what pain are they experiencing?

- A. Internal - Team Operate cần tự động hóa việc nhập liệu STR từ các folder khách hàng
- B. Internal - Team Risk/Compliance cần báo cáo STR chính xác và kịp thời
- C. External - NHNN yêu cầu hệ thống tự động gửi báo cáo giao dịch đáng ngờ
- D. Cả A và B - đội nội bộ cần công cụ để xử lý STR hiệu quả hơn
- E. Khác (vui lòng nêu rõ)
- [Answer]: D. Cả A và B - đội nội bộ cần công cụ để xử lý STR hiệu quả hơn

## Q3. Success Metrics

What does success look like? What metrics matter?

- A. Thời gian xử lý giảm từ X giờ xuống Y giờ
- B. Số lượng bản ghi STR được xử lý mỗi ngày đạt Z bản ghi
- C. Độ chính xác dữ liệu đạt 99% trở lên
- D. Không có lỗi trong quy trình và email thông báo được gửi đúng hạn
- E. Khác (vui lòng nêu rõ)
- [Answer]: B. Số lượng bản ghi STR được xử lý mỗi ngày đạt Z bản ghi

## Q4. Initiative Trigger

Why are we starting this initiative now? (Market pressure, tech debt, regulation, opportunity)

- A. Yêu cầu từ regulator (NHNN) về việc báo cáo giao dịch đáng ngờ
- B. Team đang làm thủ công và cần tự động hóa
- C. Có sẵn code tham khảo từ RPA_NHAPBAOCAO_STR cần được tái sử dụng
- D. Công nghệ Kafka đã được thiết lập và sẵn sàng tích hợp
- E. Khác (vui lòng nêu rõ)
- [Answer]: B. Team đang làm thủ công và cần tự động hóa

## Q5. Key Stakeholders

Who are the key stakeholders and what does each care about?

- A. Team Operate - cần công cụ dễ sử dụng và ít lỗi
- B. Team Risk/Compliance - cần dữ liệu chính xác và đầy đủ
- C. IT Operations - cần hệ thống ổn định và dễ giám sát
- D. Tech Lead - cần code dễ bảo trì và mở rộng
- E. Khác (vui lòng nêu rõ)
- [Answer]: A. Team Operate - cần công cụ dễ sử dụng và ít lỗi

## Q6. Decision-Makers

Who decides scope or priority, and who influences those decisions?

- A. Tech Lead và Product Owner
- B. Team Leader Operate
- C. Business Analyst
- D. Collaboration giữa các team (Operate, Risk, IT)
- E. Không rõ - cần làm rõ sau
- [Answer]: A. Tech Lead và Product Owner

## Q7. Communication Requirements

Are there any communication requirements or reporting cadence?

- A. Email thông báo hàng ngày/tuần về tiến độ xử lý
- B. Dashboard giám sát real-time
- C. Report định kỳ gửi cho regulator
- D. Không có yêu cầu đặc biệt
- E. Khác (vui lòng nêu rõ)
- [Answer]: A. Email thông báo hàng ngày/tuần về tiến độ xử lý

## Q8. Scope Confirmation

The workflow was started with scope `feature`; does that match the intended product boundary?

- A. Yes - `feature` scope phù hợp với nhu cầu hiện tại
- B. No - cần `enterprise` scope vì có nhiều integration points
- C. No - `mvp` scope là đủ cho phiên bản đầu
- D. No - cần `express` scope vì đã có code tham khảo
- E. Chưa chắc chắn - cần phân tích thêm
- [Answer]: A. Yes - `feature` scope phù hợp với nhu cầu hiện tại

# Assumptions & Open Questions

None.

## Assumption Confirmation

A. Accept assumptions
B. Convert to follow-up questions
- [Answer]: A. Accept assumptions

