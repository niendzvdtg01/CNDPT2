import noisereduce as nr
import soundfile as sf
import librosa
import numpy as np
import os


if __name__ == "__main__":

    # --- Bước 1: Load file sau khi đã lọc band-pass ---
    # Đây là output từ bước trước:
    # → đã loại bỏ phần lớn nhiễu thấp và cao
    temp_path = "Results/temp_bandpass.wav"

    # Kiểm tra file tồn tại
    if not os.path.exists(temp_path):
        print("Lỗi: Cần chạy Bandpass_filter.py trước!")

    else:
        # Load audio (giữ nguyên sample rate)
        data, sr = librosa.load(temp_path, sr=None)


        # --- Bước 2: Lấy mẫu nhiễu (noise profile) ---
        # Giả định:
        # - 0.5 giây đầu KHÔNG có giọng nói
        # - chỉ chứa noise môi trường
        #
        # Đây là bước cực quan trọng:
        # → model sẽ học "noise trông như thế nào"
        noise_sample = data[:int(0.5 * sr)]


        # --- Bước 3: Khử nhiễu (Noise Reduction) ---
        # nr.reduce_noise sử dụng kỹ thuật:
        # → Spectral gating (dựa trên STFT)
        #
        # Ý tưởng:
        # - phân tích noise_sample → tạo profile nhiễu
        # - so sánh với toàn bộ tín hiệu
        # - giảm các thành phần giống noise
        #
        # Các tham số quan trọng:

        clean = nr.reduce_noise(
            y=data,              # tín hiệu đầu vào
            sr=sr,               # sample rate
            y_noise=noise_sample, # mẫu noise tham chiếu

            # prop_decrease:
            # mức độ giảm noise (0 → 1)
            # - 1.0 → giảm mạnh (dễ méo giọng)
            # - 0.85 → cân bằng (giữ giọng tự nhiên hơn)
            prop_decrease=0.85,

            # stationary=True:
            # giả định noise KHÔNG thay đổi theo thời gian
            # (vd: tiếng quạt, điều hòa)
            stationary=True
        )


        # --- Bước 4: Chuẩn hóa lại biên độ ---
        # Sau khi filter + noise reduction:
        # → tín hiệu có thể bị giảm volume
        #
        # Normalize lại về [-1, 1]
        if np.max(np.abs(clean)) > 0:
            clean = clean / np.max(np.abs(clean))


        # --- Bước 5: Xuất file hoàn chỉnh ---
        # File output cuối pipeline
        sf.write("Results/output.wav", clean, sr)

        print("--- Bước 2: Đã hoàn thành Pipeline. File cuối lưu tại Results/output.wav ---")