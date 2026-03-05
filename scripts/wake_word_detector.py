#!/usr/bin/env python3
import argparse
import os
import sys
import time
import numpy as np
import sounddevice as sd
from sherpa_onnx import KeywordSpotter


class VoiceWakeWordDetector:
    def __init__(self, model_dir, keywords, sample_rate=16000, device="default"):
        self.sample_rate = sample_rate
        self.keywords = keywords
        self.device = device
        self.is_running = False
        
        tokens_path = os.path.join(model_dir, "tokens.txt")
        encoder_path = os.path.join(model_dir, "encoder.onnx")
        decoder_path = os.path.join(model_dir, "decoder.onnx")
        joiner_path = os.path.join(model_dir, "joiner.onnx")
        
        if not all(os.path.exists(p) for p in [tokens_path, encoder_path, decoder_path, joiner_path]):
            raise FileNotFoundError(f"模型文件不完整，请检查目录: {model_dir}")
        
        self.kws = KeywordSpotter(
            tokens=tokens_path,
            encoder=encoder_path,
            decoder=decoder_path,
            joiner=joiner_path,
        )
        
    def audio_callback(self, indata, frames, time_info, status):
        if status:
            print(f"音频状态: {status}")
        
        audio = indata[:, 0]
        stream = self.kws.create_stream()
        stream.accept_waveform(self.sample_rate, audio)
        
        self.kws.decode_stream(stream)
        result = self.kws.get_result(stream)
        
        if result.keyword:
            print(f"\n检测到唤醒词: {result.keyword} (置信度: {result.probability:.2f})")
            self.on_wake_word_detected(result.keyword, result.probability)
    
    def on_wake_word_detected(self, keyword, probability):
        print(f"唤醒词 '{keyword}' 触发！可以执行后续操作...")
    
    def start(self):
        print(f"开始监听唤醒词: {', '.join(self.keywords)}")
        print(f"采样率: {self.sample_rate}Hz")
        print(f"设备: {self.device}")
        print("按 Ctrl+C 停止监听\n")
        
        self.is_running = True
        try:
            with sd.InputStream(
                callback=self.audio_callback,
                channels=1,
                samplerate=self.sample_rate,
                device=self.device,
                blocksize=1600,
            ):
                while self.is_running:
                    time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n停止监听")
        except Exception as e:
            print(f"错误: {e}")
        finally:
            self.is_running = False
    
    def stop(self):
        self.is_running = False


def main():
    parser = argparse.ArgumentParser(description="Sherpa-ONNX 语音唤醒词检测工具")
    parser.add_argument(
        "--model-dir",
        type=str,
        default="./models/kws",
        help="模型文件目录路径"
    )
    parser.add_argument(
        "--keywords",
        type=str,
        nargs="+",
        default=["小爱同学", "你好小爱"],
        help="要检测的唤醒词列表"
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
    
    args = parser.parse_args()
    
    if not os.path.exists(args.model_dir):
        print(f"错误: 模型目录不存在: {args.model_dir}")
        print("请先运行模型下载脚本: python scripts/download_models.py")
        sys.exit(1)
    
    try:
        detector = VoiceWakeWordDetector(
            model_dir=args.model_dir,
            keywords=args.keywords,
            sample_rate=args.sample_rate,
            device=args.device
        )
        detector.start()
    except Exception as e:
        print(f"初始化失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()