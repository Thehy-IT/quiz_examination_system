# 1. Chọn Base Image (Hình ảnh nền)
FROM python:3.13-slim

# 2. Thiết lập thư mục làm việc (Working Directory)
# Mọi lệnh sau dòng này sẽ chạy bên trong thư mục /app của container
WORKDIR /app

# 3. Cài đặt các thư viện
# Copy file requirements.txt vào container trước để tận dụng Docker Cache
COPY requirements.txt .
# Cài đặt, --no-cache-dir giúp giảm dung lượng image
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy mã nguồn (Source Code)
# Copy toàn bộ thư mục hiện tại (PROGANDTEST_GROUP15) vào /app
COPY . .

# 5. Thiết lập biến môi trường (Environment Variable)
# Giúp Python nhận diện folder 'quiz_app' là một module
ENV PYTHONPATH=/app

# 6. Mở cổng
# Thông báo cho Docker biết container này dùng port 8080
EXPOSE 8080

# 7. Lệnh chạy ứng dụng (Command)
# Sử dụng '-m' để chạy module, an toàn hơn việc gọi file trực tiếp
CMD ["python", "-m", "quiz_app.main"]