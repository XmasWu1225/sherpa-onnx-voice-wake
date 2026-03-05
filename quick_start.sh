#!/bin/bash

echo "========================================"
echo "  Sherpa-ONNX 语音唤醒工具快速启动"
echo "========================================"
echo ""

echo "请选择要启动的工具:"
echo "1. 简单语音检测 (无需模型)"
echo "2. 音频测试工具"
echo "3. Web 语音识别 (浏览器版本)"
echo "4. 检查模型下载状态"
echo "5. 下载所有模型"
echo "6. 语音唤醒词检测 (需要模型)"
echo "7. 语音识别 (需要模型)"
echo "8. 退出"
echo ""

read -p "请输入选项 (1-8): " choice

case $choice in
    1)
        echo "启动简单语音检测..."
        python scripts/simple_voice_detector.py
        ;;
    2)
        echo "启动音频测试工具..."
        python scripts/audio_test.py
        ;;
    3)
        echo "在浏览器中打开 Web 语音识别工具..."
        if command -v xdg-open > /dev/null; then
            xdg-open web_voice.html
        elif command -v open > /dev/null; then
            open web_voice.html
        else
            echo "请手动在浏览器中打开: $(pwd)/web_voice.html"
        fi
        ;;
    4)
        echo "检查模型下载状态..."
        echo ""
        echo "KWS 模型目录:"
        ls -lh models/kws/ 2>/dev/null || echo "  目录不存在"
        echo ""
        echo "ASR 模型目录:"
        ls -lh models/asr/ 2>/dev/null || echo "  目录不存在"
        echo ""
        echo "VAD 模型目录:"
        ls -lh models/vad/ 2>/dev/null || echo "  目录不存在"
        echo ""
        echo "正在运行的下载进程:"
        ps aux | grep wget | grep -v grep || echo "  无"
        ;;
    5)
        echo "开始下载所有模型..."
        python scripts/download_models.py
        ;;
    6)
        echo "启动语音唤醒词检测..."
        python scripts/wake_word_detector.py
        ;;
    7)
        echo "启动语音识别..."
        python scripts/speech_to_text.py
        ;;
    8)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效选项"
        exit 1
        ;;
esac