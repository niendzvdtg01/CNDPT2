from scipy.signal import butter, filtfilt
import soundfile as sf
import numpy as np
import librosa
import matplotlib.pyplot as plt
import os


# --- Bước 1: Định nghĩa Low-pass filter ---
def lowpass_filter(data, cutoff, sr, order=4):
    """
    Bộ lọc low-pass:
    - Giữ lại tần số THẤP hơn cutoff
    - Loại bỏ tần số CAO (high-frequency noise)

    data: tín hiệu audio (waveform)
    cutoff: tần số cắt (Hz)
    sr: sample rate
    order: bậc filter (độ dốc)
    """

    # Nyquist frequency = sr / 2
    # Đây là giới hạn tối đa của tần số trong tín hiệu số
    nyq = 0.5 * sr

    # Chuẩn hóa cutoff về [0,1] theo yêu cầu của butter()
    normal_cutoff = cutoff / nyq

    # Thiết kế Butterworth low-pass filter
    # - mượt, không ripple
    # - phù hợp audio
    b, a = butter(order, normal_cutoff, btype="low", analog=False)

    # filtfilt:
    # - lọc 2 chiều (forward + backward)
    # - không gây lệch pha (rất quan trọng với audio)
    y = filtfilt(b, a, data)

    return y


# --- Main ---
if __name__ == "__main__":

    # --- Bước 2: Định nghĩa đường dẫn ---
    input_original = "input.wav"        # audio gốc
    input_step5 = "Results/output.wav" # audio sau noise reduction
    output_path = "Results/output_final.wav"


    # Kiểm tra tồn tại file
    if os.path.exists(input_step5) and os.path.exists(input_original):

        # --- Bước 3: Load dữ liệu ---
        # data_filtered: audio đã qua pipeline
        data_filtered, sr = librosa.load(input_step5, sr=None)

        # data_original: audio gốc để so sánh
        data_original, _ = librosa.load(input_original, sr=None)


        # --- Bước 4: Low-pass filter hậu xử lý ---
        # cutoff = 3800 Hz:
        # - giữ lại phần quan trọng của giọng nói
        # - loại bỏ hiss/noise cao tần còn sót lại
        final_clean = lowpass_filter(data_filtered, 3800, sr)


        # --- Bước 5: Normalize lần cuối ---
        # đảm bảo tín hiệu không quá nhỏ / quá lớn
        if np.max(np.abs(final_clean)) > 0:
            final_clean = final_clean / np.max(np.abs(final_clean))


        # --- Bước 6: Lưu file hoàn chỉnh ---
        sf.write(output_path, final_clean, sr)

        print(f"--- Đã hoàn thành Hậu xử lý. File cuối cùng: {output_path} ---")


        # --- Bước 7: Visualization so sánh ---
        plt.figure(figsize=(12, 6), dpi=300)

        # Downsampling để vẽ nhanh + dễ nhìn
        # lấy 1/100 mẫu
        subsample = 100

        # Tín hiệu gốc (baseline)
        plt.plot(
            data_original[::subsample],
            color='silver',
            alpha=0.6,
            label="Original (Gốc)"
        )

        # Tín hiệu sau toàn bộ pipeline
        plt.plot(
            final_clean[::subsample],
            color='forestgreen',
            alpha=0.8,
            label="Filtered (Đã lọc Pipeline)"
        )

        # Thiết lập biểu đồ
        plt.title("So sánh tín hiệu: Original vs Final Pipeline Output")
        plt.xlabel("Mẫu dữ liệu (Downsampled x100)")
        plt.ylabel("Biên độ")

        plt.legend(loc='upper right')
        plt.grid(True, alpha=0.3, linestyle='--')


        # --- Bước 8: Lưu biểu đồ ---
        save_plot_path = "Results/Compare_sound.jpg"
        plt.savefig(save_plot_path)

        plt.close()

        print(f"--- Đã cập nhật biểu đồ so sánh cuối cùng tại: {save_plot_path} ---")

    else:
        print("Lỗi: Kiểm tra lại file input.wav và Results/output.wav")