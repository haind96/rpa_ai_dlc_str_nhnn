# Cấu hình kết nối các Service (Mock Server, Kafka, RabbitMQ)

Tài liệu này tổng hợp toàn bộ thông tin cấu hình, link kết nối, thông tin xác thực (username/password), và cách gửi request (cURL) của các service đang chạy trên Docker trong dự án này.

---

## 1. Mock Server (FastAPI)
- **Base URL:** `http://192.168.0.2:8831`

### 1.1 Service 1: Authentication (Lấy Token)
- **Endpoint:** `POST /auth/realms/ms-core/protocol/openid-connect/token`
- **Username:** `rpa_user2`
- **Password:** `paxaKjlEcJ1W3R8j7hvom8mFP2ZFK5Fq`
- **Body Data (x-www-form-urlencoded):**
  - `grant_type`: `client_credentials`
  - `client_id`: `rpa_user2`
  - `client_secret`: `paxaKjlEcJ1W3R8j7hvom8mFP2ZFK5Fq`

**cURL mẫu:**
```bash
curl --location 'http://192.168.0.2:8831/auth/realms/ms-core/protocol/openid-connect/token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=client_credentials' \
--data-urlencode 'client_id=rpa_user2' \
--data-urlencode 'client_secret=paxaKjlEcJ1W3R8j7hvom8mFP2ZFK5Fq'
```

### 1.2 Service 2: Search Files
- **Endpoint:** `POST /ecm-core-v1.0/businesses/{business_code}/files/search`
- **Header Required:** `Authorization: Bearer <TOKEN>`
- **Business Codes hỗ trợ:** `mb_smart_channel`, `customer_info_ca`, `ss_customer_doc`, `ss_auto_upload_customer_info`, `customer_information`, `biz_onboarding`
- **Body JSON:**
```json
{
    "metadata": {
        "customerCode": {
            "type": "eq",
            "value": "6670501"
        }
    },
    "pagination": {
        "page": 1,
        "size": 100
    }
}
```

**cURL mẫu:**
```bash
curl --location 'http://192.168.0.2:8831/ecm-core-v1.0/businesses/mb_smart_channel/files/search' \
--header 'ClientMessageId: 345345345322323' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <TOKEN_TU_API_1>' \
--data '{
    "metadata": {
        "customerCode": {
            "type": "eq",
            "value": "66@70501)()*^"
        }
    },
    "pagination": {
        "page": 1,
        "size": 100
    }
}'
```

### 1.3 Service 3: Get File Content (Download)
- **Endpoint:** `GET /ecm-core-v1.0/files/{doc_id}/content`
- **Header Required:** `Authorization: Bearer <TOKEN>`
- **Ví dụ `doc_id`:** `mb01e9fed8047d5c`

**cURL mẫu:**
```bash
curl --location 'http://192.168.0.2:8831/ecm-core-v1.0/files/mb01e9fed8047d5c/content' \
--header 'Authorization: Bearer <TOKEN_TU_API_1>'
```
*(Response trả về là file PDF thật).*

---

## 2. Kafka & Kafka UI

### 2.1 Kafka Broker
- **Port kết nối từ máy Host:** `192.168.0.2:9093`
- **Port kết nối giữa các container trong Docker:** `kafka:29092`
- **Protocol:** `SASL_PLAINTEXT`
- **Xác thực (Username/Password):**
  - Username: `admin`
  - Password: `admin123`
- **Topic tự động tạo:** `RPA_STR_NHNN_INPUT`

### 2.2 Kafka UI
- **URL Truy cập:** `http://192.168.0.2:8080`
- **Chức năng:** Giao diện trực quan để xem Topics, Messages, Consumers, v.v...
- Không yêu cầu mật khẩu đăng nhập UI.

---

## 3. RabbitMQ

### 3.1 Giao diện quản trị (Management UI)
- **URL Truy cập:** `http://localhost:15672`
- **Username:** `guest`
- **Password:** `guest`

### 3.2 Kết nối API/AMQP
- **Host / Port:** `localhost:5672`
- **Giao thức:** AMQP
- **Username/Password mặc định:** `guest` / `guest`
