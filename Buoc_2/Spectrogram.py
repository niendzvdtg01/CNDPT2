import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os

# Import tín hiệu audio đã xử lý
# audio: waveform (miền thời gian)
# sr: sample rate
from Buoc_1.Load_audio import audio, sr


# --- Bước 1: Cắt đoạn audio để tối ưu RAM ---
# Vì audio có thể rất dài → STFT sẽ tốn RAM + thời gian
# → chỉ lấy 30 giây đầu để phân tích

start_sec = 0
end_sec = 30

# Chuyển giây → index mẫu
audio_segment = audio[int(start_sec * sr): int(end_sec * sr)]


# --- Bước 2: Thực hiện STFT (Short-Time Fourier Transform) ---

# STFT = chia tín hiệu thành các frame nhỏ rồi FFT từng frame
#
# n_fft = 2048:
# - kích thước cửa sổ FFT
# - quyết định độ phân giải tần số
#
# hop_length = 512:
# - bước nhảy giữa các frame
# - quyết định độ phân giải thời gian
#
# => Trade-off:
# - n_fft lớn → tốt về tần số, kém thời gian
# - hop nhỏ → chi tiết thời gian hơn

D = librosa.stft(audio_segment, n_fft=2048, hop_length=512)

# D là ma trận số phức:
# shape ≈ (tần số, thời gian)
#
# |D| = magnitude (biên độ)
# phase ít dùng trong visualization

# Chuyển magnitude → decibel (log scale)
S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)


# --- Bước 3: Vẽ Spectrogram ---

plt.figure(figsize=(12, 6))

# specshow:
# hiển thị ma trận STFT dưới dạng ảnh (heatmap)
librosa.display.specshow(
    S_db,
    sr=sr,
    hop_length=512,

    # Trục X: thời gian (giây)
    x_axis='time',

    # Trục Y: log scale (quan trọng)
    # giúp nhìn rõ:
    # - tần số thấp (bass, noise)
    # - giống cách tai người nghe
    y_axis='log',

    # cmap:
    # magma = màu tối → sáng (contrast tốt cho noise)
    cmap='magma'
)

# Thanh màu biểu diễn cường độ (dB)
plt.colorbar(format='%+2.0f dB')

plt.title("Spectrogram Analysis (Log Frequency Scale)")


# --- Bước 4: Lưu kết quả ---
if not os.path.exists('Results'):
    os.makedirs('Results')

plt.savefig('Results/Stft.png', dpi=300)

# Hiển thị
plt.show()