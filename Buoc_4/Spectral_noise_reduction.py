import noisereduce as nr
import soundfile as sf
import librosa
import numpy as np
import os

if __name__ == "__main__":
    # Load file đã qua bước lọc Band-pass
    temp_path = "Results/temp_bandpass.wav"
    if not os.path.exists(temp_path):
        print("Lỗi: Cần chạy Bandpass_filter.py trước!")
    else:
        data, sr = librosa.load(temp_path, sr=None)

        # Lấy mẫu nhiễu từ 0.5s đầu của file đã lọc dải tần
        noise_sample = data[:int(0.5 * sr)]

        # Thực hiện khử nhiễu thích nghi
        # Giảm prop_decrease xuống 0.85 để tránh méo giọng khi kết hợp nhiều bộ lọc
        clean = nr.reduce_noise(y=data, sr=sr, y_noise=noise_sample, prop_decrease=0.85, stationary=True)

        # Chuẩn hóa biên độ cuối cùng
        if np.max(np.abs(clean)) > 0:
            clean = clean / np.max(np.abs(clean))

        # Xuất file kết quả hoàn thiện
        sf.write("Results/output.wav", clean, sr)
        print("--- Bước 2: Đã hoàn thành Pipeline. File cuối lưu tại Results/output.wav ---")
