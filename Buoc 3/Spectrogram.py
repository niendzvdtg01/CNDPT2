import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os
from Load_audio import audio, sr

# 1. Thực hiện STFT với cửa sổ phân tích tối ưu cho giọng nói
# n_fft=2048, hop_length=512 là thông số chuẩn để cân bằng độ phân giải
D = librosa.stft(audio, n_fft=2048, hop_length=512)
S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

# 2. Vẽ biểu đồ Spectrogram
plt.figure(figsize=(12, 6))
librosa.display.specshow(
    S_db, sr=sr,
    hop_length=512,
    x_axis='time',
    y_axis='log', # Chuyển sang thang Log để soi nhiễu tần số thấp tốt hơn
    cmap='magma'  # Dùng bảng màu 'magma' để tương phản nhiễu rõ hơn
)
# Chỉ phân tích 30 giây đầu để tránh tràn RAM
start_sec = 0
end_sec = 30
audio_segment = audio[int(start_sec*sr) : int(end_sec*sr)]

D = librosa.stft(audio_segment)
# ... tiếp tục các bước vẽ như cũ
plt.colorbar(format='%+2.0f dB')
plt.title("Spectrogram Analysis (Log Frequency Scale)")

# 3. Tự động lưu kết quả cho báo cáo
if not os.path.exists('Results'):
    os.makedirs('Results')
plt.savefig('Results/Stft.png', dpi=300)
plt.show()
