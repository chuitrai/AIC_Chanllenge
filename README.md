# AIC_Chanllenge
A system for querying images using a sequence of characters or a similar image across thousands of videos.

# Hệ thống truy vấn hình ảnh từ video 

##  Giới thiệu
Đây là hệ thống truy vấn hình ảnh tương tự dựa trên một chuỗi ký tự hoặc một hình ảnh đầu vào. Hệ thống hỗ trợ tìm kiếm hình ảnh trong một tập lớn video bằng cách:
- Sử dụng **Streamlit** để tạo giao diện web.
- Áp dụng **TransNet** để trích xuất keyframes từ video.
- Dùng **FAISS Cosine Similarity** để so sánh hình ảnh và truy vấn ký tự.
- Hỗ trợ tìm kiếm dựa trên nội dung văn bản hoặc hình ảnh do người dùng cung cấp.

##  Chức năng chính
- Tải lên video hoặc sử dụng dữ liệu có sẵn.
- Tiền xử lí ảnh, tạo file json để truy xuất ảnh
- Tìm kiếm bằng hình ảnh hoặc chuỗi ký tự.
- Trả về hình ảnh tương tự nhất từ bộ dữ liệu video.
- Hỗ trợ vẽ bounding box hoặc annotation

##  Cài đặt
Yêu cầu Python 3.8+ và các thư viện sau:
```bash
pip install -r requirements.txt
```
## Cách sử dụng
1. Chạy ứng dụng Streamlit
```bash
streamlit run app.py
```
2. Tải lên video hoặc sử dụng dữ liệu sẵn có.
   Nếu tải ảnh lên, bạn phải đảm bảo đã tạo ra file faiss_cosin.bin sẵn và chạy file create_json_path.py
   ![image](https://github.com/user-attachments/assets/7a57f597-14b1-4181-8c7b-206b96a37e43)

4. Nhập chuỗi văn bản hoặc tải lên một hình ảnh để tìm kiếm.
5. Nhận kết quả là các hình ảnh tương tự từ video đã phân tích.
## Hiệu suất hệ thống
## 📊 Hiệu suất mô hình

| Tiêu chí                     | Giá trị (Cần bổ sung)   |
|-----------------------------|----------------------|
| Số video xử lý              | 1471 video, 20 ~ 30 phút/video           |
| Số keyframe trích xuất | ~870k ảnh 640x340 |
| Thời gian trích xuất keyframes | 300 giây/video    |
| Tốc độ truy vấn trung bình  | 1s /query        |
| Độ chính xác tìm kiếm       | ~90 %               |



1️⃣ Giao diện web
![image](https://github.com/user-attachments/assets/6fe11436-3185-4465-b5c2-ff25e40373c0)


2️⃣ Ví dụ truy vấn ảnh
![image](https://github.com/user-attachments/assets/b730c46b-b78a-4c41-b4b0-a62087e6fa77)


3️⃣ Kết quả tìm kiếm
![image](https://github.com/user-attachments/assets/1895f2b6-dcc1-43a7-80c1-aee812e97c44)


## Giấy phép
Hệ thống này được phát triển phục vụ mục đích nghiên cứu và thử nghiệm.

