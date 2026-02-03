import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import os
from Buoc_1.Load_audio import audio, sr

# 1. Đảm bảo thư mục Results tồn tại để lưu ảnh báo cáo
if not os.path.exists("Results"):
    os.makedirs("Results")

# 2. Tính toán FFT
# N là số lượng mẫu: 7,945,344 mẫu
N = len(audio)
# Sử dụng rfft (Real FFT) để tối ưu hiệu suất cho âm thanh thực tế
fft_data = np.fft.rfft(audio)
# Tính toán dải tần số tương ứng
freqs = np.fft.rfftfreq(N, 1/sr)

# 3. Chuyển đổi sang thang đo Decibel (dB)
# Giúp quan sát rõ các nhiễu môi trường có cường độ thấp
magnitude_db = 20 * np.log10(np.abs(fft_data) + 1e-6)

# 4. Vẽ đồ thị FFT
plt.figure(figsize=(10, 5))
plt.plot(freqs, magnitude_db, color='royalblue', linewidth=0.5, alpha=0.8)

plt.title("Phân tích Phổ tần số (FFT) - Dữ liệu Ghi âm Thực tế")
plt.xlabel("Tần số (Hz)")
plt.ylabel("Biên độ (dB)")
plt.grid(True, linestyle='--', alpha=0.6)

# Giới hạn hiển thị 0-8000Hz (Vùng tập trung giọng nói phỏng vấn/podcast)
plt.xlim(0, 8000)

# 5. Tự động lưu biểu đồ vào Results
save_path = os.path.join("Results", "FFT.png")
plt.savefig(save_path, dpi=300)
print(f"--- Đã cập nhật biểu đồ FFT tại: {save_path} ---")
plt.show()
