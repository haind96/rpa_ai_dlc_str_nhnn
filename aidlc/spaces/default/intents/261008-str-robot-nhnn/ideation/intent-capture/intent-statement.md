# Intent Statement

## Problem Statement

Cần tự động hóa việc xử lý báo cáo giao dịch đáng ngờ (STR - Suspicious Transaction Report) trên web portal của NHNN (Ngân hàng Nhà nước Việt Nam). Hiện tại team Operate đang thực hiện thủ công việc thu thập, xử lý và nhập liệu cho các báo cáo STR, gây tốn thời gian và dễ phát sinh lỗi. Giải pháp RPA sẽ tự động hóa quy trình từ thu thập dữ liệu từ Kafka, tích hợp với nhiều hệ thống (ECM, Accuity, TraCuuThue, ALMD), đến tạo báo cáo và gửi email thông báo.

## Target Customer

**Internal - Team Operate và Team Risk/Compliance**
- **Team Operate**: Cần công cụ tự động để giảm tải công việc nhập liệu thủ công, tăng hiệu suất xử lý
- **Team Risk/Compliance**: Cần dữ liệu STR chính xác, đầy đủ và kịp thời để thực hiện các bước phân tích và báo cáo lên cấp trên

## Success Metrics

- Số lượng bản ghi STR được xử lý mỗi ngày: Z bản ghi (mục tiêu cụ thể cần xác định)
- Thời gian xử lý mỗi batch giảm từ X giờ xuống Y giờ
- Độ chính xác dữ liệu đạt 99% trở lên
- Không có lỗi trong quy trình và email thông báo được gửi đúng hạn
- Khả năng mở rộng xử lý khi số lượng bản ghi tăng

## Initiative Trigger

**Team đang làm thủ công và cần tự động hóa**
- Quy trình hiện tại yêu cầu xử lý nhiều folder khách hàng (CUS.T24.*) với nhiều bước phức tạp
- Mỗi bước (Accuity, TraCuuThue, ALMD) cần thao tác manual trên các web portal
- Cần tái sử dụng code tham khảo từ dự án RPA_NHAPBAOCAO_STR để đẩy nhanh development

## Initial Scope Signal

**Workflow-selected scope**: `feature`

**User-confirmed product boundary**: `feature` scope phù hợp với nhu cầu hiện tại

### In Scope
- Xây dựng robot RPA theo luồng: `STR_NHNN_ConsumeData_Enqueue` -> `STR_NHNN_DataEntry_Accuity` -> `STR_NHNN_TraCuuThue` -> `STR_NHNN_DataEntry_ALMD` -> `STR_NHNN_Consume_SendMail`
- Tích hợp với Kafka để consume message từ source system
- Tích hợp với các hệ thống: ECM, Accuity, TraCuuThue, ALMD
- Tự động hóa việc tạo báo cáo PDF và gửi email thông báo
- Xử lý error case và retry logic

### Out of Scope
- Thiết kế lại UI/UX của các web portal
- Thay đổi quy trình nghiệp vụ hiện tại
- Phát triển hệ thống backend mới - chỉ tích hợp existing systems
