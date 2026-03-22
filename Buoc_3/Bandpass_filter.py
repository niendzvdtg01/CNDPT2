import numpy as np
import librosa
import soundfile as sf
from scipy.signal import butter, filtfilt
import os

# Import tín hiệu audio đã xử lý từ bước trước
# audio: waveform (numpy array)
# sr: sample rate (Hz)
from Load_audio import audio, sr


# --- Bước 1: Thiết kế bộ lọc Butterworth (Band-pass filter) ---
def butter_bandpass(lowcut, highcut, fs, order=5):
    """
    Tạo bộ lọc Butterworth dạng band-pass

    lowcut: tần số cắt dưới (Hz)
    highcut: tần số cắt trên (Hz)
    fs: sample rate (Hz)
    order: bậc của bộ lọc (độ dốc)

    Trả về:
        b, a: hệ số bộ lọc (numerator, denominator)
    """

    # Nyquist frequency = fs / 2
    # Đây là tần số tối đa có thể biểu diễn trong tín hiệu số
    nyq = 0.5 * fs

    # Chuẩn hóa tần số về khoảng [0, 1]
    # (theo yêu cầu của scipy.signal.butter)
    low = lowcut / nyq
    high = highcut / nyq

    # butter():
    # thiết kế bộ lọc Butterworth:
    # - đáp ứng mượt (không ripple)
    # - phù hợp audio
    #
    # btype='band':
    # giữ lại dải [lowcut → highcut]
    b, a = butter(order, [low, high], btype='band')

    return b, a


# --- Bước 2: Áp dụng bộ lọc ---
def apply_bandpass_filter(data, lowcut, highcut, fs, order=5):
    """
    Áp dụng band-pass filter lên tín hiệu

    data: waveform đầu vào
    return: waveform đã lọc
    """

    # Lấy hệ số filter
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)

    # filtfilt:
    # - lọc 2 chiều (forward + backward)
    # - KHÔNG gây lệch pha (zero-phase filtering)
    # - rất quan trọng với audio (giữ nguyên timing)
    return filtfilt(b, a, data)


# --- Main ---
if __name__ == "__main__":

    # Tạo thư mục lưu kết quả nếu chưa có
    if not os.path.exists('Results'):
        os.makedirs('Results')

    # --- Bước 3: Lọc tín hiệu ---
    # Giữ lại dải tần 300Hz → 4000Hz
    #
    # Ý nghĩa:
    # - < 300Hz → thường là:
    #     + tiếng ù (hum)
    #     + tiếng gió
    #
    # - > 4000Hz → thường là:
    #     + noise cao tần
    #     + hiss / rít
    #
    # => Đây là dải tần chính của giọng nói
    filtered_bp = apply_bandpass_filter(audio, 300, 4000, sr)

    # --- Bước 4: Lưu file ---
    # Ghi audio ra file .wav
    # sf.write:
    # - ghi waveform thành file audio
    # - giữ nguyên sample rate
    sf.write("Results/temp_bandpass.wav", filtered_bp, sr)

    print("--- Bước 1: Đã lọc Band-pass và lưu file trung gian ---")