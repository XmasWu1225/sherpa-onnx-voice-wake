# Sherpa-ONNX 语音唤醒与识别工具

基于 [Sherpa-ONNX](https://github.com/k2-fsa/sherpa-onnx) 的语音唤醒词检测和语音识别工具，支持离线运行。

## 功能特性

- 语音唤醒词检测
- 实时语音识别
- 支持中文和英文
- 语音活动检测 (VAD)
- 文件语音识别
- 离线运行

## 项目结构

```
stt/
├── models/              # 模型文件目录
│   ├── kws/            # 关键词检测模型
│   ├── asr/            # 语音识别模型
│   └── vad/            # VAD 模型
├── scripts/            # 脚本目录
│   ├── wake_word_detector.py    # 语音唤醒词检测
│   ├── speech_to_text.py        # 语音识别
│   └── download_models.py       # 模型下载
├── config/             # 配置文件目录
├── requirements.txt    # Python 依赖
└── README.md          # 项目说明
```

## 快速开始

### 使用快速启动脚本

```bash
./quick_start.sh
```

这将提供一个交互式菜单，让你选择要使用的工具。

### 立即开始使用

如果你不想下载模型，可以使用以下工具：

#### 1. 简单语音检测（无需模型）

```bash
python scripts/simple_voice_detector.py
```

#### 2. Web 语音识别（浏览器版本）

在浏览器中打开 `web_voice.html` 文件，使用浏览器内置的语音识别功能。

#### 3. 音频测试工具

```bash
python scripts/audio_test.py
```

## 安装依赖

```bash
pip install -r requirements.txt
```

### 系统依赖

Linux 系统需要安装 PortAudio：

```bash
sudo apt-get install portaudio19-dev
```

### 依赖说明

- `sherpa-onnx`: 核心语音处理库
- `sounddevice`: 音频设备访问
- `soundfile`: 音频文件读写
- `numpy`: 数值计算

## 下载模型

### 下载所有模型

```bash
python scripts/download_models.py
```

### 下载指定模型

```bash
# 仅下载关键词检测模型
python scripts/download_models.py --models kws

# 仅下载语音识别模型 (默认 paraformer)
python scripts/download_models.py --models asr

# 仅下载 VAD 模型
python scripts/download_models.py --models vad

# 指定 ASR 模型类型
python scripts/download_models.py --models asr --asr-model zipformer
```

### ASR 模型类型

- `paraformer`: Paraformer 模型 (推荐，中文+英文)
- `zipformer`: Zipformer 模型 (流式识别，中文+英文)
- `whisper`: Whisper 模型 (英文)

## 使用方法

### 1. 语音唤醒词检测

```bash
python scripts/wake_word_detector.py
```

#### 参数说明

- `--model-dir`: 模型目录路径 (默认: `./models/kws`)
- `--keywords`: 唤醒词列表 (默认: `["小爱同学", "你好小爱"]`)
- `--sample-rate`: 音频采样率 (默认: `16000`)
- `--device`: 音频设备 (默认: `default`)

#### 示例

```bash
# 使用默认唤醒词
python scripts/wake_word_detector.py

# 自定义唤醒词
python scripts/wake_word_detector.py --keywords "你好" "唤醒"

# 指定采样率
python scripts/wake_word_detector.py --sample-rate 48000

# 查看可用音频设备
python -c "import sounddevice; print(sounddevice.query_devices())"
```

### 2. 语音识别

#### 实时语音识别

```bash
python scripts/speech_to_text.py
```

#### 识别音频文件

```bash
python scripts/speech_to_text.py --file audio.wav
```

#### 参数说明

- `--model-dir`: 模型目录路径 (默认: `./models/asr`)
- `--file`: 要识别的音频文件
- `--no-vad`: 不使用语音活动检测
- `--sample-rate`: 音频采样率 (默认: `16000`)
- `--device`: 音频设备 (默认: `default`)
- `--duration`: 识别时长（秒）

#### 示例

```bash
# 实时识别
python scripts/speech_to_text.py

# 识别文件
python scripts/speech_to_text.py --file test.wav

# 不使用 VAD
python scripts/speech_to_text.py --no-vad

# 识别 30 秒
python scripts/speech_to_text.py --duration 30
```

## 音频设备配置

### 查看可用设备

```bash
python -c "import sounddevice; print(sounddevice.query_devices())"
```

### 指定音频设备

```bash
# 使用设备索引
python scripts/wake_word_detector.py --device 0

# 使用设备名称
python scripts/wake_word_detector.py --device "USB Audio Device"
```

## 模型说明

### 关键词检测模型

- 模型: sherpa-onnx-kws-zipformer-wenetspeech-3.3M
- 语言: 中文
- 大小: 约 3.3MB

### 语音识别模型

#### Paraformer
- 模型: sherpa-onnx-paraformer-zh-2023-03-28
- 语言: 中文 + 英文
- 类型: 非流式识别
- 大小: 约 100MB

#### Zipformer
- 模型: sherpa-onnx-streaming-zipformer-bilingual-zh-en-2023-02-20
- 语言: 中文 + 英文
- 类型: 流式识别
- 大小: 约 50MB

#### Whisper
- 模型: sherpa-onnx-whisper-tiny.en
- 语言: 英文
- 类型: 非流式识别
- 大小: 约 40MB

### VAD 模型

- 模型: Silero VAD
- 语言: 多语言
- 大小: 约 60MB

## 常见问题

### 1. 音频设备访问错误

确保系统有可用的音频输入设备，并检查权限设置。

Linux 系统可能需要将用户添加到 `audio` 组：

```bash
sudo usermod -a -G audio $USER
```

### 2. 模型下载失败

如果 GitHub 下载速度慢，可以手动下载模型文件并解压到 `models` 目录。

### 3. 识别准确率低

- 确保音频采样率与模型匹配 (通常为 16000Hz)
- 检查音频质量，减少背景噪音
- 尝试不同的模型类型

### 4. 内存不足

- 使用较小的模型 (如 Zipformer)
- 减少音频缓冲区大小

## 系统要求

- Python 3.8+
- 麦克风
- 至少 2GB RAM
- 推荐使用 Linux 或 macOS

## 许可证

本项目基于 Sherpa-ONNX，遵循相应的开源许可证。

## 相关链接

- [Sherpa-ONNX GitHub](https://github.com/k2-fsa/sherpa-onnx)
- [Sherpa-ONNX 文档](https://k2-fsa.github.io/sherpa/onnx/)
- [预训练模型](https://github.com/k2-fsa/sherpa-onnx/releases)