# 使用指南

## 快速开始

### 方式一：使用快速启动脚本（推荐）

```bash
./quick_start.sh
```

这会显示一个交互式菜单，让你选择要使用的工具：

1. 简单语音检测（无需模型）
2. 音频测试工具
3. Web 语音识别（浏览器版本）
4. 检查模型下载状态
5. 下载所有模型
6. 语音唤醒词检测（需要模型）
7. 语音识别（需要模型）
8. 退出

### 方式二：直接运行脚本

#### 简单语音检测（无需模型）

```bash
python scripts/simple_voice_detector.py
```

这个工具使用简单的能量检测来判断是否有语音，不需要下载任何模型。

#### Web 语音识别（浏览器版本）

在浏览器中打开 `web_voice.html` 文件：

```bash
# Linux
xdg-open web_voice.html

# macOS
open web_voice.html
```

或者直接双击 `web_voice.html` 文件在浏览器中打开。

#### 音频测试工具

```bash
python scripts/audio_test.py
```

测试音频设备是否正常工作。

## 完整功能使用

### 1. 下载模型

如果需要使用完整的语音唤醒和识别功能，需要先下载模型：

```bash
python scripts/download_models.py
```

这将下载以下模型：
- KWS 模型：关键词检测（约 3.3MB）
- ASR 模型：语音识别（约 100MB）
- VAD 模型：语音活动检测（约 60MB）

**注意**：模型下载可能需要较长时间，取决于网络速度。

### 2. 语音唤醒词检测

```bash
python scripts/wake_word_detector.py
```

默认唤醒词：`小爱同学`、`你好小爱`

自定义唤醒词：

```bash
python scripts/wake_word_detector.py --keywords "你好" "唤醒"
```

### 3. 语音识别

实时识别：

```bash
python scripts/speech_to_text.py
```

识别音频文件：

```bash
python scripts/speech_to_text.py --file audio.wav
```

## 音频设备配置

### 查看可用设备

```bash
python -c "import sounddevice; print(sounddevice.query_devices())"
```

### 指定音频设备

```bash
# 使用设备索引
python scripts/simple_voice_detector.py --device 0

# 使用设备名称
python scripts/simple_voice_detector.py --device "USB Audio Device"
```

## 常见问题

### 1. 音频设备访问错误

确保系统有可用的音频输入设备。

Linux 系统可能需要将用户添加到 `audio` 组：

```bash
sudo usermod -a -G audio $USER
```

### 2. 模型下载失败

如果 GitHub 下载速度慢，可以：

1. 使用代理
2. 手动下载模型文件
3. 使用简单语音检测工具（无需模型）

### 3. 检测不到语音

- 检查麦克风是否正常工作
- 调整检测阈值：`--threshold 0.01`
- 尝试不同的音频设备

### 4. 浏览器语音识别不工作

- 使用 Chrome 或 Edge 浏览器
- 确保浏览器有麦克风权限
- 检查网络连接（Web Speech API 需要网络）

## 推荐使用流程

### 快速测试

1. 运行 `python scripts/audio_test.py` 测试音频设备
2. 运行 `python scripts/simple_voice_detector.py` 测试语音检测
3. 在浏览器中打开 `web_voice.html` 测试语音识别

### 完整功能

1. 安装依赖：`pip install -r requirements.txt`
2. 下载模型：`python scripts/download_models.py`
3. 运行语音唤醒：`python scripts/wake_word_detector.py`
4. 运行语音识别：`python scripts/speech_to_text.py`

## 技术支持

如遇到问题，请检查：

1. Python 版本（需要 3.8+）
2. 音频设备是否正常
3. 模型文件是否完整
4. 系统权限设置