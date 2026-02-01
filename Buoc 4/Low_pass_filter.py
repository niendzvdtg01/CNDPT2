from scipy.signal import butter, filtfilt
import soundfile as sf
import numpy as np
import librosa
import matplotlib.pyplot as plt
import os

def lowpass_filter(data, cutoff, sr, order=4):
    nyq = 0.5 * sr
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    y = filtfilt(b, a, data)
    return y

if __name__ == "__main__":
    # 1. Đường dẫn các file
    input_original = "input.wav"        # File gốc để làm mốc so sánh
    input_step5 = "Results/output.wav"  # Kết quả từ bước Spectral Gating
    output_path = "Results/output_final.wav"

    if os.path.exists(input_step5) and os.path.exists(input_original):
        # 2. Load dữ liệu
        data_filtered, sr = librosa.load(input_step5, sr=None)
        data_original, _ = librosa.load(input_original, sr=None)

        # 3. Thực hiện lọc Low-pass hậu xử lý
        final_clean = lowpass_filter(data_filtered, 3800, sr)

        # 4. Chuẩn hóa biên độ cuối cùng
        if np.max(np.abs(final_clean)) > 0:
            final_clean = final_clean / np.max(np.abs(final_clean))

        # 5. Lưu file hoàn thiện cuối cùng
        sf.write(output_path, final_clean, sr)
        print(f"--- Đã hoàn thành Hậu xử lý. File cuối cùng: {output_path} ---")

        # 6. BỔ SUNG: Vẽ biểu đồ so sánh ĐẦU - CUỐI (Compare_sound.jpg)
        plt.figure(figsize=(12, 6), dpi=300)
        
        # Downsampling để biểu đồ thanh thoát (x100 mẫu)
        subsample = 100
        
        # Vẽ tín hiệu gốc (màu xám)
        plt.plot(data_original[::subsample], color='silver', alpha=0.6, label="Original (Gốc)")
        
        # Vẽ tín hiệu sau khi qua toàn bộ Pipeline (màu xanh lá)
        plt.plot(final_clean[::subsample], color='forestgreen', alpha=0.8, label="Filtered (Đã lọc Pipeline)")

        plt.title("So sánh tín hiệu: Original vs Final Pipeline Output")
        plt.xlabel("Mẫu dữ liệu (Downsampled x100)")
        plt.ylabel("Biên độ")
        plt.legend(loc='upper right')
        plt.grid(True, alpha=0.3, linestyle='--')

        # Lưu biểu đồ "đẹp" nhất cho báo cáo
        save_plot_path = "Results/Compare_sound.jpg"
        plt.savefig(save_plot_path)
        plt.close()
        print(f"--- Đã cập nhật biểu đồ so sánh cuối cùng tại: {save_plot_path} ---")

    else:
        print("Lỗi: Kiểm tra lại file input.wav và Results/output.wav")
