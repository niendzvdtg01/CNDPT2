from scipy.signal import butter, filtfilt
import soundfile as sf
import numpy as np
import librosa
import os


def lowpass_filter(data, cutoff, sr, order=4):  # Dùng order 4 để cắt nhẹ nhàng hơn
    nyq = 0.5 * sr
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    y = filtfilt(b, a, data)
    return y


if __name__ == "__main__":
    # Lấy đầu ra của bước Spectral Gating làm đầu vào
    input_step5 = "Results/output.wav"

    if os.path.exists(input_step5):
        data, sr = librosa.load(input_step5, sr=None)

        # Lọc ở ngưỡng 3800Hz - 4000Hz để làm mịn giọng nói
        final_clean = lowpass_filter(data, 3800, sr)

        # Chuẩn hóa lần cuối
        if np.max(np.abs(final_clean)) > 0:
            final_clean = final_clean / np.max(np.abs(final_clean))

        # Lưu file hoàn thiện cuối cùng
        output_path = "Results/output_final.wav"
        sf.write(output_path, final_clean, sr)
        print(f"--- Đã hoàn thành Hậu xử lý. File cuối cùng: {output_path} ---")
    else:
        print("Lỗi: Hãy chạy Spectral_noise_reduction.py trước.")
