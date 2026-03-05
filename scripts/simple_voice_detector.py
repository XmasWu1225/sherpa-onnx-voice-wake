#!/usr/bin/env python3
import argparse
import os
import sys
import time
import json
import numpy as np
import sounddevice as sd


class SimpleVoiceDetector:
    def __init__(self, sample_rate=16000, device="default", threshold=0.02):
        self.sample_rate = sample_rate
        self.device = device
        self.threshold = threshold
        self.is_running = False
        self.buffer = []
        self.buffer_size = int(sample_rate * 0.5)  # 0.5秒缓冲
    
    def audio_callback(self, indata, frames, time_info, status):
        if status:
            print(f"音频状态: {status}")
        
        audio = indata[:, 0]
        
        # 计算音频能量
        energy = np.sqrt(np.mean(audio**2))
        
        # 检测语音活动
        if energy > self.threshold:
            print(f"\r[检测到语音] 能量: {energy:.4f}", end="", flush=True)
            self.buffer.extend(audio)
        else:
            print(f"\r[静音] 能量: {energy:.4f}", end="", flush=True)
    
    def start(self):
        print(f"开始简单语音检测 (采样率: {self.sample_rate}Hz)")
        print(f"设备: {self.device}")
        print(f"检测阈值: {self.threshold}")
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
    parser = argparse.ArgumentParser(description="简单语音检测工具")
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
        default=0.02,
        help="语音检测阈值"
    )
    
    args = parser.parse_args()
    
    try:
        detector = SimpleVoiceDetector(
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