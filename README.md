## Audio Processing Pipeline

Project này thực hiện xử lý và giảm nhiễu âm thanh thông qua các bước sau:

### 1. Audio Input
Thu nhận hoặc đọc file âm thanh đầu vào để xử lý.

### 2. Waveform Analysis
Phân tích dạng sóng trong miền thời gian để hiểu cấu trúc tín hiệu ban đầu.

### 3. FFT / STFT Analysis
Chuyển tín hiệu sang miền tần số bằng:
- FFT để xem phổ tổng thể
- STFT để xem phổ theo thời gian (spectrogram)

### 4. Noise Identification
Xác định các thành phần nhiễu dựa trên phân bố năng lượng trong phổ tần.

### 5. Filter Design
Thiết kế bộ lọc phù hợp:
- Low-pass filter
- Band-pass filter
- hoặc các bộ lọc khác tùy mục đích.

### 6. Noise Reduction
Áp dụng thuật toán giảm nhiễu như spectral gating hoặc filtering.

### 7. Quality Evaluation
So sánh tín hiệu trước và sau xử lý bằng:
- Waveform
- Spectrogram
- Đánh giá cảm nhận khi nghe.

### 8. Output Audio
Xuất file âm thanh đã được xử lý và lưu kết quả.

