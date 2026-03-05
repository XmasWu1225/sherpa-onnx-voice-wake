# GitHub 仓库创建和推送指南

## 第一步：在 GitHub 上创建仓库

1. 访问 [GitHub](https://github.com)
2. 点击右上角的 `+` 按钮，选择 `New repository`
3. 填写仓库信息：
   - **Repository name**: `sherpa-onnx-voice-wake`（或你喜欢的名称）
   - **Description**: `基于 Sherpa-ONNX 的语音唤醒与识别工具`
   - **Public/Private**: 选择 `Public` 或 `Private`
   - **Initialize this repository**: 不要勾选（因为我们已经有本地代码）
4. 点击 `Create repository` 按钮

## 第二步：连接本地仓库到 GitHub

创建仓库后，GitHub 会显示一些命令。复制类似下面的命令：

```bash
cd /hdd_data/aaod/stt
git remote add origin https://github.com/你的用户名/仓库名.git
```

**替换示例**：
```bash
git remote add origin https://github.com/username/sherpa-onnx-voice-wake.git
```

## 第三步：推送代码到 GitHub

### 如果是第一次推送（使用 main 分支）：

```bash
git branch -M main
git push -u origin main
```

### 如果已经推送过，后续更新：

```bash
git push
```

## 完整示例

假设你的 GitHub 用户名是 `yourusername`，仓库名是 `sherpa-onnx-voice-wake`：

```bash
# 1. 连接到远程仓库
cd /hdd_data/aaod/stt
git remote add origin https://github.com/yourusername/sherpa-onnx-voice-wake.git

# 2. 设置主分支为 main
git branch -M main

# 3. 推送代码到 GitHub
git push -u origin main
```

## 常见问题

### 1. 认证问题

如果推送时需要认证，GitHub 现在使用 Personal Access Token (PAT)：

1. 访问 https://github.com/settings/tokens
2. 点击 `Generate new token` -> `Generate new token (classic)`
3. 选择权限：至少需要 `repo` 权限
4. 生成 token 并复制
5. 推送时使用 token 作为密码

### 2. 如果远程仓库已存在

```bash
# 查看现有远程仓库
git remote -v

# 删除现有远程仓库
git remote remove origin

# 添加新的远程仓库
git remote add origin https://github.com/yourusername/your-repo.git
```

### 3. 使用 SSH 而不是 HTTPS

如果你配置了 SSH 密钥：

```bash
git remote add origin git@github.com:yourusername/your-repo.git
```

## 推送后的操作

推送成功后，你可以在 GitHub 上看到你的仓库，包含：

- 所有脚本文件
- 配置文件
- 文档（README.md, USAGE.md）
- Web 版语音识别工具
- 快速启动脚本

## 后续更新

当你修改代码后，使用以下命令推送更新：

```bash
# 查看修改的文件
git status

# 添加修改的文件
git add .

# 提交修改
git commit -m "描述你的修改"

# 推送到 GitHub
git push
```

## 快速命令参考

```bash
# 查看状态
git status

# 查看提交历史
git log

# 查看远程仓库
git remote -v

# 查看分支
git branch

# 创建新分支
git branch new-feature

# 切换分支
git checkout new-feature

# 合并分支
git merge new-feature
```