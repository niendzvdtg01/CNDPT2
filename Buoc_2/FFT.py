import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import os

# Import dữ liệu audio đã xử lý từ bước trước
# audio: mảng tín hiệu (waveform)
# sr: sample rate (Hz)
from Buoc_1.Load_audio import audio, sr


# --- Bước 1: Chuẩn bị thư mục lưu kết quả ---
# Kiểm tra xem thư mục "Results" đã tồn tại chưa
# Nếu chưa thì tạo mới để lưu ảnh FFT
if not os.path.exists("Results"):
    os.makedirs("Results")


# --- Bước 2: Biến đổi FFT (Fast Fourier Transform) ---

# N = tổng số mẫu trong tín hiệu
# Ví dụ: 7,945,344 mẫu
# Ý nghĩa: độ dài tín hiệu trong miền thời gian
N = len(audio)

# np.fft.rfft:
# - Thực hiện FFT cho tín hiệu THỰC (real signal)
# - Tối ưu hơn fft thường vì:
#     + Không cần tính phần tần số âm (đối xứng)
#     + Nhanh hơn ~2 lần
#
# Kết quả:
# fft_data là số phức (complex numbers)
# mỗi phần tử chứa:
#   - magnitude (biên độ)
#   - phase (pha)
fft_data = np.fft.rfft(audio)


# np.fft.rfftfreq:
# Tạo ra mảng tần số tương ứng với từng phần tử trong fft_data
#
# Công thức:
# freq = k * (sr / N)
#
# với:
#   k = chỉ số phần tử
#   sr = sample rate
#   N = số mẫu
#
# => giúp mapping:
#   "index trong FFT" → "tần số thực (Hz)"
freqs = np.fft.rfftfreq(N, 1/sr)


# --- Bước 3: Chuyển sang thang Decibel (dB) ---

# np.abs(fft_data):
# Lấy độ lớn (magnitude) của số phức
#
# FFT trả về:
# X = a + bi
# magnitude = sqrt(a^2 + b^2)
#
# 20 * log10(...):
# Chuyển sang thang log (dB)
#
# Lý do:
# - Tai người nghe theo log scale
# - Dễ thấy cả tín hiệu mạnh và yếu
#
# + 1e-6:
# Tránh log(0) → -∞ (lỗi)
magnitude_db = 20 * np.log10(np.abs(fft_data) + 1e-6)


# --- Bước 4: Vẽ biểu đồ phổ tần số ---

plt.figure(figsize=(10, 5))

# freqs: trục X (tần số)
# magnitude_db: trục Y (biên độ dB)
#
# color: màu đường
# linewidth: độ dày nét
# alpha: độ trong suốt (0 → 1)
plt.plot(freqs, magnitude_db, color='royalblue', linewidth=0.5, alpha=0.8)


# Tiêu đề biểu đồ
plt.title("Phân tích Phổ tần số (FFT) - Dữ liệu Ghi âm Thực tế")

# Nhãn trục
plt.xlabel("Tần số (Hz)")
plt.ylabel("Biên độ (dB)")

# Thêm lưới để dễ đọc
plt.grid(True, linestyle='--', alpha=0.6)


# Giới hạn trục X từ 0 → 8000 Hz
# Vì:
# - Giọng nói người thường nằm trong:
#     ~80 Hz → 4000 Hz
# - 8000 Hz là vùng đủ để phân tích speech/podcast
plt.xlim(0, 8000)


# --- Bước 5: Lưu ảnh kết quả ---

# Tạo đường dẫn file lưu
save_path = os.path.join("Results", "FFT.png")

# dpi=300:
# - Chất lượng cao (dùng cho report)
plt.savefig(save_path, dpi=300)

print(f"--- Đã cập nhật biểu đồ FFT tại: {save_path} ---")

# Hiển thị biểu đồ
plt.show()