#!/usr/bin/env python3
import argparse
import os
import sys
import time
import numpy as np
import sounddevice as sd
from sherpa_onnx import (
    OfflineRecognizer,
    OnlineRecognizer,
    VADModel,
    OnlineStream,
)


class SpeechToText:
    def __init__(self, model_dir, use_vad=True, sample_rate=16000, device="default"):
        self.sample_rate = sample_rate
        self.device = device
        self.use_vad = use_vad
        self.is_running = False
        
        tokens_path = os.path.join(model_dir, "tokens.txt")
        encoder_path = os.path.join(model_dir, "encoder.onnx")
        decoder_path = os.path.join(model_dir, "decoder.onnx")
        joiner_path = os.path.join(model_dir, "joiner.onnx")
        
        if not all(os.path.exists(p) for p in [tokens_path, encoder_path, decoder_path, joiner_path]):
            raise FileNotFoundError(f"模型文件不完整，请检查目录: {model_dir}")
        
        self.recognizer = OnlineRecognizer(
            tokens=tokens_path,
            encoder=encoder_path,
            decoder=decoder_path,
            joiner=joiner_path,
            sample_rate=sample_rate,
        )
        
        if use_vad:
            vad_path = os.path.join(model_dir, "silero_vad.onnx")
            if os.path.exists(vad_path):
                self.vad = VADModel(vad_path, sample_rate=sample_rate)
            else:
                print(f"VAD 模型不存在，将不使用 VAD: {vad_path}")
                self.vad = None
        else:
            self.vad = None
        
        self.stream = None
        self.last_text = ""
    
    def audio_callback(self, indata, frames, time_info, status):
        if status:
            print(f"音频状态: {status}")
        
        audio = indata[:, 0]
        
        if self.stream is None:
            self.stream = self.recognizer.create_stream()
        
        self.stream.accept_waveform(self.sample_rate, audio)
        
        if self.use_vad and self.vad:
            self.vad.accept_waveform(self.sample_rate, audio)
            is_speech = self.vad.is_speech()
            
            if not is_speech:
                self.stream.input_finished()
        
        self.recognizer.decode_stream(self.stream)
        result = self.recognizer.get_result(self.stream)
        
        if result.text and result.text != self.last_text:
            print(f"\r识别结果: {result.text}", end="", flush=True)
            self.last_text = result.text
    
    def start(self, duration=None):
        print(f"开始语音识别 (采样率: {self.sample_rate}Hz)")
        print(f"使用 VAD: {'是' if self.use_vad else '否'}")
        print(f"设备: {self.device}")
        print("按 Ctrl+C 停止识别\n")
        
        self.is_running = True
        start_time = time.time()
        
        try:
            with sd.InputStream(
                callback=self.audio_callback,
                channels=1,
                samplerate=self.sample_rate,
                device=self.device,
                blocksize=1600,
            ):
                while self.is_running:
                    if duration and (time.time() - start_time) >= duration:
                        break
                    time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n停止识别")
        except Exception as e:
            print(f"\n错误: {e}")
        finally:
            self.is_running = False
            if self.stream:
                self.stream.input_finished()
                self.recognizer.decode_stream(self.stream)
                final_result = self.recognizer.get_result(self.stream)
                if final_result.text:
                    print(f"\n最终结果: {final_result.text}")
    
    def stop(self):
        self.is_running = False
    
    def recognize_file(self, audio_file):
        print(f"识别文件: {audio_file}")
        
        if not os.path.exists(audio_file):
            print(f"错误: 文件不存在: {audio_file}")
            return None
        
        recognizer = OfflineRecognizer(
            tokens=os.path.join(self.recognizer.config.tokens),
            encoder=os.path.join(self.recognizer.config.encoder),
            decoder=os.path.join(self.recognizer.config.decoder),
            joiner=os.path.join(self.recognizer.config.joiner),
            sample_rate=self.sample_rate,
        )
        
        import soundfile as sf
        audio, sr = sf.read(audio_file)
        
        if sr != self.sample_rate:
            print(f"警告: 音频采样率 {sr}Hz 与模型采样率 {self.sample_rate}Hz 不匹配")
        
        if len(audio.shape) > 1:
            audio = audio[:, 0]
        
        duration = len(audio) / sr
        print(f"音频时长: {duration:.2f}秒")
        
        stream = recognizer.create_stream()
        stream.accept_waveform(self.sample_rate, audio)
        
        recognizer.decode(stream)
        result = recognizer.get_result(stream)
        
        print(f"识别结果: {result.text}")
        return result.text


def main():
    parser = argparse.ArgumentParser(description="Sherpa-ONNX 语音识别工具")
    parser.add_argument(
        "--model-dir",
        type=str,
        default="./models/asr",
        help="模型文件目录路径"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="识别音频文件"
    )
    parser.add_argument(
        "--no-vad",
        action="store_true",
        help="不使用语音活动检测"
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
        "--duration",
        type=int,
        help="识别时长（秒）"
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.model_dir):
        print(f"错误: 模型目录不存在: {args.model_dir}")
        print("请先运行模型下载脚本: python scripts/download_models.py")
        sys.exit(1)
    
    try:
        stt = SpeechToText(
            model_dir=args.model_dir,
            use_vad=not args.no_vad,
            sample_rate=args.sample_rate,
            device=args.device
        )
        
        if args.file:
            stt.recognize_file(args.file)
        else:
            stt.start(duration=args.duration)
    except Exception as e:
        print(f"初始化失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()