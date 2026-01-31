# 🎙️ Hệ Thống Lọc Nhiễu Âm Thanh Ghi Âm Thực Tế (Noise Reduction System)

## 📝 Giới thiệu đề tài
Dự án tập trung vào việc xây dựng hệ thống xử lý tín hiệu số để cải thiện chất lượng âm thanh từ các nguồn ghi âm thực tế bị lẫn nhiễu môi trường. Hệ thống được thiết kế để Cải thiện chất lượng ghi âm thực tế khỏi các tạp âm thông qua các kỹ thuật phân tích phổ và bộ lọc số.

## ⚙️ Quy trình xử lý (Audio Processing Pipeline)
Hệ thống được triển khai theo một quy trình DSP (Digital Signal Processing) chuẩn hóa:

1.  **Audio Input:** Thu nhận hoặc đọc file âm thanh đầu vào (`input.wav`) thông qua thư viện `librosa` hoặc `scipy`.
2.  **Waveform Analysis:** Phân tích dạng sóng trong miền thời gian để hiểu cấu trúc tín hiệu và biên độ ban đầu.
3.  **FFT / STFT Analysis:** Chuyển tín hiệu sang miền tần số bằng FFT để xem phổ tổng thể và STFT để xem phổ theo thời gian (spectrogram).
4.  **Noise Identification:** Xác định các thành phần nhiễu (white noise, hum, hiss) dựa trên phân bố năng lượng trong phổ tần.
5.  **Filter Design:** Thiết kế bộ lọc phù hợp như Low-pass, Band-pass hoặc kiến trúc lọc thích nghi tùy mục đích.
6.  **Noise Reduction:** Áp dụng thuật toán giảm nhiễu chính là **Spectral Gating** dựa trên việc trích xuất Noise Profile.
7.  **Quality Evaluation:** So sánh tín hiệu thông qua chỉ số toán học (SNR, RMSE) và biểu đồ trực quan.
8.  **Output Audio:** Xuất file âm thanh sạch (`output.wav`) và lưu trữ kết quả phân tích.

---

## 🔬 Phân tích Kỹ thuật và Đánh giá Thực nghiệm

Phần này trình bày kết quả phân tích chuyên sâu các biến đổi của tín hiệu âm thanh thông qua hệ thống xử lý, nhằm chứng minh hiệu quả của các thuật toán đã cài đặt.

### 1. Phân tích Phổ tần số (FFT Spectrum)
Biến đổi Fourier nhanh (FFT) giúp chúng ta chuyển đổi tín hiệu từ miền thời gian sang miền tần số để xác định đặc tính của nhiễu.

![Phân tích FFT](Results/FFT.png)

* **Quan sát kỹ thuật:** Đồ thị FFT hiển thị mức năng lượng (Magnitude) tập trung cực lớn tại dải tần số thấp ($0Hz - 1000Hz$), đạt ngưỡng trên $60$ dB. Đây là dấu hiệu của nhiễu nền (Background Noise) có cường độ mạnh, thường là tiếng ù từ môi trường hoặc thiết bị ghi.
* **Phân tích IT:** Năng lượng nhiễu trải dài liên tục trên toàn bộ phổ tần cho thấy sự hiện diện của nhiễu trắng (White Noise). Việc phân tích FFT khẳng định nhiễu trong mẫu thực tế là nhiễu băng rộng, xác nhận việc kết hợp Band-pass để cô lập dải giọng nói là bước tiền xử lý bắt buộc trước khi áp dụng thuật toán thích nghi.

### 2. Phân tích Phổ thời gian (Spectrogram/STFT)
Đồ thị Spectrogram cung cấp cái nhìn ba chiều về cường độ tín hiệu theo cả thời gian và tần số.

![Phân tích Spectrogram](Results/Stft.png)

* **Quan sát:** Thang màu biểu thị cường độ (dB) cho thấy một "noise floor" (nền nhiễu) bao phủ đồng nhất trên toàn bộ các khung thời gian.
* **Phân tích kỹ thuật:** Sự phân bố này xác nhận đây là **nhiễu tĩnh (Stationary Noise)**. Nhờ đặc tính này, thuật toán có thể trích xuất "Noise Profile" chính xác từ các đoạn không chứa giọng nói (silence) để tạo ra một mặt nạ phổ (Spectral Mask), giúp triệt tiêu nhiễu mà vẫn bảo tồn được các dải hài âm (Harmonics) cần thiết của tiếng người.

### 3. Đánh giá sự biến đổi Dạng sóng (Waveform Comparison)
Phép so sánh trực tiếp biên độ tín hiệu trong miền thời gian giữa file gốc (Original) và file sau lọc (Filtered).

![So sánh Waveform](Results/Compare_sound.png)

* **Đường màu xanh (Original):** Biên độ dao động dày đặc, bao phủ toàn bộ dải thời gian, cho thấy nhiễu lấp đầy các khoảng lặng giữa các câu nói.
* **Đường màu cam (Filtered):** Biên độ nhiễu tại các đoạn lặng đã được làm phẳng về gần mức $0$.
* **Phân tích:** Việc đường màu cam giữ nguyên được cấu trúc của các đỉnh (peaks) của đường màu xanh cho thấy hệ thống đã loại bỏ nhiễu hiệu quả mà không gây ra hiện tượng méo tiếng (distortion) hay xén ngọn tín hiệu (clipping). Điều này chứng minh thuật toán đã cải thiện đáng kể **Tỷ số tín hiệu trên nhiễu (SNR)**.

---
| Giai đoạn | Phương pháp | SNR (dB) | Cải thiện |
| :--- | :--- | :---: | :---: |
| **Đầu vào** | File gốc (Chưa xử lý) | 3.62 dB | --- |
| **Đầu ra** | **Pipeline (BP + Spectral + LP)** | 17.74 dB | **+14.12 dB** |

* **Kết luận:** Với file đầu vào có độ nhiễu cực cao (3.62 dB), mức cải thiện +14.12 dB tương đương với việc giảm năng lượng nhiễu đi khoảng 25 lần. Hệ thống đã chuyển đổi thành công một bản ghi âm thực tế từ trạng thái không đạt chuẩn sang trạng thái có thể sử dụng cho các mục đích truyền thông chuyên nghiệp.
---
## 🚀 Hướng phát triển thêm (Future Work)
* **Voice Activity Detection (VAD):** Tự động nhận diện đoạn im lặng để trích xuất Noise Profile tự động.
* **Adaptive Filtering:** Nghiên cứu thuật toán LMS để xử lý nhiễu thay đổi theo thời gian (non-stationary noise).
* **Performance Optimization:** Tối ưu hóa code để giảm độ trễ (latency), hướng tới xử lý thời gian thực.

---
