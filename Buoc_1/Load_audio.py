import librosa
import numpy as np
import os


def load_processed_audio(file_path):
    """
    Hàm này thực hiện:
    1. Kiểm tra file tồn tại
    2. Load audio từ file (wav, mp3, ...)
    3. Chuyển về mono (1 kênh)
    4. Chuẩn hóa biên độ (normalize)
    
    Trả về:
        audio: mảng numpy chứa tín hiệu âm thanh (dạng waveform)
        sr: sample rate (tần số lấy mẫu)
    """

    # --- Bước 1: Kiểm tra file có tồn tại không ---
    # os.path.exists giúp tránh lỗi khi load file không tồn tại
    if not os.path.exists(file_path):
        print(f"Lỗi: Không tìm thấy file tại {file_path}")
        return None, None

    # --- Bước 2: Load audio ---
    # librosa.load thực hiện:
    # - Đọc file âm thanh (wav, mp3, flac...)
    # - Decode thành dạng waveform (mảng số thực)
    # - sr=None: giữ nguyên sample rate gốc (không resample)
    # - mono=True: nếu file là stereo (2 kênh), sẽ trộn về 1 kênh:
    #     mono_signal = (left + right) / 2
    #
    # audio: numpy array dạng [x1, x2, x3, ..., xn]
    # sr: số mẫu trên 1 giây (ví dụ 44100 Hz)
    audio, sr = librosa.load(file_path, sr=None, mono=True)

    # --- Bước 3: Chuẩn hóa biên độ (Peak Normalization) ---
    # Mục đích:
    # - Đưa tín hiệu về khoảng [-1, 1]
    # - Tránh tín hiệu quá nhỏ (khó xử lý) hoặc quá lớn (clipping)
    #
    # np.abs(audio): lấy trị tuyệt đối từng mẫu
    # np.max(...): tìm giá trị lớn nhất (biên độ đỉnh)
    #
    # Nếu max > 0:
    # -> chia toàn bộ tín hiệu cho max
    # -> giá trị lớn nhất sẽ trở thành 1 hoặc -1
    #
    # Ví dụ:
    # audio = [0.2, -0.5, 0.8]
    # max = 0.8
    # => audio_new = [0.25, -0.625, 1.0]
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio))

    # Trả về waveform + sample rate
    return audio, sr


# --- Phần main (chạy thực tế) ---

# Đường dẫn file audio đầu vào
path = "./input.wav"

# Gọi hàm load và xử lý
audio, sr = load_processed_audio(path)

# --- Bước 4: In thông tin ---
if audio is not None:
    print(f"--- Thông số file đầu vào ---")

    # Sample rate:
    # Số mẫu trên mỗi giây
    # Ví dụ: 44100 Hz = 44100 mẫu / giây
    print(f"Sample rate: {sr} Hz")

    # Độ dài audio (giây):
    # len(audio): tổng số mẫu
    # len(audio) / sr = số giây
    print(f"Độ dài: {len(audio) / sr:.2f} giây")

    # Tổng số mẫu trong file
    print(f"Số lượng mẫu: {len(audio)}")