---
name: "aliyun-tts"
description: "调用阿里云百炼（DashScope）文字转语音API，将文本转换为语音。支持多种高质量模型如 qwen3-tts-flash-realtime。"
---

# 阿里云百炼 TTS (文字转语音) Skill

## 概述

调用阿里云百炼 Realtime TTS API（OpenAI 兼容 WebSocket 协议），将文本生成高质量语音文件。

> **重要**：使用 `/api-ws/v1/realtime` endpoint（非 `/inference/`），这是 OpenAI 兼容接口。

## 配置凭据

```powershell
# 方式一：环境变量
$env:DASHSCOPE_API_KEY = "sk-xxxx"

# 方式二：命令行参数
--api_key "sk-xxxx"
```

## 安装依赖

```bash
python scripts/aliyun_tts.py --install-deps
```

## 基本使用

```bash
# 基本（默认 Cherry 音色，mp3 格式）
python scripts/aliyun_tts.py --api_key "sk-xxx" --text "你好世界" --output hello.mp3

# 指定音色
python scripts/aliyun_tts.py --text "你好" --voice Serena --output hello.mp3

# 查看所有音色
python scripts/aliyun_tts.py --list-voices
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--text` | 要转换的文本（必须） | - |
| `--output` | 输出文件路径 | output.mp3 |
| `--voice` | 音色 ID（见下表） | Cherry |
| `--format` | 音频格式：mp3 / pcm / opus | mp3 |
| `--model` | 模型名称 | qwen3-tts-flash-realtime |
| `--api_key` | API Key | 环境变量 |

## 常用音色

| ID | 中文名 | 性别 | 风格 |
|----|--------|------|------|
| `Cherry` | 芊悦 | 女 | 阳光积极（默认） |
| `Serena` | 苏瑶 | 女 | 温柔 |
| `Chelsie` | 千雪 | 女 | 二次元 |
| `Ethan` | 晨煦 | 男 | 阳光温暖 |
| `Ryan` | 甜茶 | 男 | 节奏感 |
| `Kai` | 凯 | 男 | 磁性 |

更多音色：`python scripts/aliyun_tts.py --list-voices`

## 注意事项

1. 使用项目中的 `bailian-api-key`（`config.yaml` → `tts.bailian-api-key`）
2. 输出格式推荐 `mp3`（浏览器兼容性最好）
3. 网络需能访问 `dashscope.aliyuncs.com`
