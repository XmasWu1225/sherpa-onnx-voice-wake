#!/usr/bin/env python3
import argparse
import os
import sys
import time
import numpy as np
import sounddevice as sd
from sherpa_onnx import VADModel


class VoiceActivityDetector:
    def __init__(self, model_path, sample_rate=16000, device="default", threshold=0.5):
        self.sample_rate = sample_rate
        self.device = device
        self.threshold = threshold
        self.is_running = False
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"VAD 模型不存在: {model_path}")
        
        self.vad = VADModel(model_path, sample_rate=sample_rate)
        print(f"VAD 模型加载成功: {model_path}")
    
    def audio_callback(self, indata, frames, time_info, status):
        if status:
            print(f"音频状态: {status}")
        
        audio = indata[:, 0]
        self.vad.accept_waveform(self.sample_rate, audio)
        is_speech = self.vad.is_speech()
        
        if is_speech:
            print("\r[检测到语音] 正在说话...", end="", flush=True)
        else:
            print("\r[静音] 等待语音...", end="", flush=True)
    
    def start(self):
        print(f"开始语音活动检测 (采样率: {self.sample_rate}Hz)")
        print(f"设备: {self.device}")
        print("按 Ctrl+C 停止检测\n")
        
        self.is_running = True
        try:
            with sd.InputStream(
                callback=self.audio_callback,
                channels=1,
                samplerate=self.sample_rate,
                device=self.device,
                blocksize=512,
            ):
                while self.is_running:
                    time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n停止检测")
        except Exception as e:
            print(f"\n错误: {e}")
        finally:
            self.is_running = False
    
    def stop(self):
        self.is_running = False


def main():
    parser = argparse.ArgumentParser(description="Sherpa-ONNX 语音活动检测工具")
    parser.add_argument(
        "--model-path",
        type=str,
        default="./models/vad/silero_vad.onnx",
        help="VAD 模型文件路径"
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=16000,
        help="音频采样率"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="default",
        help="音频设备名称或索引"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="语音检测阈值"
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.model_path):
        print(f"错误: VAD 模型不存在: {args.model_path}")
        print("\n请下载 VAD 模型:")
        print("  wget https://github.com/k2-fsa/sherpa-onnx/releases/download/vad-models/silero_vad.onnx -O models/vad/silero_vad.onnx")
        sys.exit(1)
    
    try:
        detector = VoiceActivityDetector(
            model_path=args.model_path,
            sample_rate=args.sample_rate,
            device=args.device,
            threshold=args.threshold
        )
        detector.start()
    except Exception as e:
        print(f"初始化失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()