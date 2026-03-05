#!/usr/bin/env python3
import argparse
import time
import numpy as np
import sounddevice as sd


def record_audio(duration=5, sample_rate=16000, device="default"):
    print(f"开始录音 {duration} 秒...")
    print(f"采样率: {sample_rate}Hz")
    print(f"设备: {device}")
    
    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        device=device
    )
    sd.wait()
    
    print(f"录音完成！音频长度: {len(audio)} 采样点")
    return audio


def play_audio(audio, sample_rate=16000, device="default"):
    print("播放录音...")
    sd.play(audio, samplerate=sample_rate, device=device)
    sd.wait()
    print("播放完成")


def analyze_audio(audio, sample_rate=16000):
    print("\n音频分析:")
    print(f"  采样点数: {len(audio)}")
    print(f"  时长: {len(audio) / sample_rate:.2f} 秒")
    print(f"  采样率: {sample_rate}Hz")
    print(f"  最大振幅: {np.max(np.abs(audio)):.4f}")
    print(f"  平均振幅: {np.mean(np.abs(audio)):.4f}")
    print(f"  RMS: {np.sqrt(np.mean(audio**2)):.4f}")
    
    if np.max(np.abs(audio)) > 0.01:
        print("  状态: 检测到音频信号")
    else:
        print("  状态: 音频信号较弱或为静音")


def main():
    parser = argparse.ArgumentParser(description="音频录制和测试工具")
    parser.add_argument(
        "--duration",
        type=int,
        default=5,
        help="录音时长（秒）"
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=16000,
        help="采样率"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="default",
        help="音频设备"
    )
    parser.add_argument(
        "--no-play",
        action="store_true",
        help="不播放录音"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="保存音频到文件"
    )
    
    args = parser.parse_args()
    
    try:
        audio = record_audio(
            duration=args.duration,
            sample_rate=args.sample_rate,
            device=args.device
        )
        
        analyze_audio(audio, sample_rate=args.sample_rate)
        
        if not args.no_play:
            play_audio(audio, sample_rate=args.sample_rate, device=args.device)
        
        if args.output:
            import soundfile as sf
            sf.write(args.output, audio, args.sample_rate)
            print(f"\n音频已保存到: {args.output}")
    
    except Exception as e:
        print(f"错误: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())