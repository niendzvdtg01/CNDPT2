import numpy as np
import librosa
import os


def calculate_snr(signal, noise_reference):
    """Tính toán SNR dựa trên năng lượng tín hiệu và năng lượng nhiễu"""
    signal_power = np.mean(signal ** 2)
    noise_power = np.mean(noise_reference ** 2)
    if noise_power == 0:
        return float('inf')
    return 10 * np.log10(signal_power / noise_power)


def run_evaluation():
    input_path = 'input.wav'
    if not os.path.exists(input_path):
        print(f"Lỗi: Không tìm thấy file gốc {input_path}")
        return

    # Load file gốc làm chuẩn
    y_in, sr = librosa.load(input_path, sr=None)
    noise_in = y_in[:int(sr * 0.5)]
    snr_in = calculate_snr(y_in, noise_in)

    # Danh sách các file cần so sánh trong Results
    output_files = {
        "Low-pass Filter": "Results/output_lowpass.wav",
        "Band-pass Filter": "Results/output_bandpass.wav",
        "Spectral Gating (Final)": "Results/output.wav"
    }

    results = []

    print("\n" + "=" * 60)
    print(f"{'PHƯƠNG PHÁP':<25} | {'SNR (dB)':<10} | {'CẢI THIỆN':<10}")
    print("-" * 60)
    print(f"{'Original (Input)':<25} | {snr_in:>8.2f} dB | {'---':>10}")

    for name, path in output_files.items():
        if os.path.exists(path):
            y_out, _ = librosa.load(path, sr=None)
            noise_out = y_out[:int(sr * 0.5)]
            snr_out = calculate_snr(y_out, noise_out)
            improvement = snr_out - snr_in

            results.append({
                "name": name,
                "snr": snr_out,
                "imp": improvement
            })
            print(f"{name:<25} | {snr_out:>8.2f} dB | {f'+{improvement:.2f} dB':>10}")
        else:
            print(f"{name:<25} | {'N/A (Không tìm thấy file)':<22}")

    print("=" * 60)

if __name__ == "__main__":

    run_evaluation()
