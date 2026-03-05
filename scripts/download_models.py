#!/usr/bin/env python3
import os
import sys
import urllib.request
import zipfile
import argparse
from pathlib import Path


def download_file(url, dest_path):
    print(f"下载: {url}")
    print(f"保存到: {dest_path}")
    
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    def progress_hook(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percent = min(downloaded * 100 / total_size, 100)
            sys.stdout.write(f"\r进度: {percent:.1f}% ({downloaded / (1024*1024):.1f}MB / {total_size / (1024*1024):.1f}MB)")
            sys.stdout.flush()
    
    try:
        urllib.request.urlretrieve(url, dest_path, progress_hook)
        print("\n下载完成")
        return True
    except Exception as e:
        print(f"\n下载失败: {e}")
        return False


def extract_zip(zip_path, extract_to):
    print(f"解压: {zip_path}")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print("解压完成")
        os.remove(zip_path)
        return True
    except Exception as e:
        print(f"解压失败: {e}")
        return False


def download_kws_model(model_dir):
    print("\n=== 下载关键词检测模型 ===")
    
    base_url = "https://github.com/k2-fsa/sherpa-onnx/releases/download/kws-models/sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01.tar.bz2"
    tar_path = Path(model_dir) / "kws.tar.bz2"
    
    if download_file(base_url, tar_path):
        import tarfile
        try:
            print(f"解压: {tar_path}")
            with tarfile.open(tar_path, 'r:bz2') as tar:
                tar.extractall(model_dir)
            print("解压完成")
            os.remove(tar_path)
            return True
        except Exception as e:
            print(f"解压失败: {e}")
            return False
    return False


def download_asr_model(model_dir, model_type="paraformer"):
    print(f"\n=== 下载语音识别模型 ({model_type}) ===")
    
    if model_type == "paraformer":
        url = "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-paraformer-zh-2023-03-28.tar.bz2"
    elif model_type == "zipformer":
        url = "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-streaming-zipformer-bilingual-zh-en-2023-02-20.tar.bz2"
    elif model_type == "whisper":
        url = "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-tiny.en.tar.bz2"
    else:
        print(f"不支持的模型类型: {model_type}")
        return False
    
    tar_path = Path(model_dir) / f"{model_type}.tar.bz2"
    
    if download_file(url, tar_path):
        import tarfile
        try:
            print(f"解压: {tar_path}")
            with tarfile.open(tar_path, 'r:bz2') as tar:
                tar.extractall(model_dir)
            print("解压完成")
            os.remove(tar_path)
            return True
        except Exception as e:
            print(f"解压失败: {e}")
            return False
    return False


def download_vad_model(model_dir):
    print("\n=== 下载 VAD 模型 ===")
    
    url = "https://github.com/k2-fsa/sherpa-onnx/releases/download/vad-models/silero_vad.onnx"
    vad_path = Path(model_dir) / "silero_vad.onnx"
    
    Path(model_dir).mkdir(parents=True, exist_ok=True)
    return download_file(url, vad_path)


def main():
    parser = argparse.ArgumentParser(description="Sherpa-ONNX 模型下载工具")
    parser.add_argument(
        "--model-dir",
        type=str,
        default="./models",
        help="模型保存目录"
    )
    parser.add_argument(
        "--models",
        type=str,
        nargs="+",
        choices=["kws", "asr", "vad", "all"],
        default=["all"],
        help="要下载的模型类型"
    )
    parser.add_argument(
        "--asr-model",
        type=str,
        choices=["paraformer", "zipformer", "whisper"],
        default="paraformer",
        help="ASR 模型类型"
    )
    
    args = parser.parse_args()
    
    model_dir = Path(args.model_dir)
    success = True
    
    for model_type in args.models:
        if model_type == "kws":
            kws_dir = model_dir / "kws"
            if not download_kws_model(kws_dir):
                success = False
        
        elif model_type == "asr":
            asr_dir = model_dir / "asr"
            if not download_asr_model(asr_dir, args.asr_model):
                success = False
        
        elif model_type == "vad":
            vad_dir = model_dir / "vad"
            if not download_vad_model(vad_dir):
                success = False
        
        elif model_type == "all":
            kws_dir = model_dir / "kws"
            asr_dir = model_dir / "asr"
            vad_dir = model_dir / "vad"
            
            if not download_kws_model(kws_dir):
                success = False
            if not download_asr_model(asr_dir, args.asr_model):
                success = False
            if not download_vad_model(vad_dir):
                success = False
    
    if success:
        print("\n=== 所有模型下载完成 ===")
        print(f"模型保存在: {model_dir.absolute()}")
    else:
        print("\n=== 部分模型下载失败 ===")
        sys.exit(1)


if __name__ == "__main__":
    main()