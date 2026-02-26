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

### 女声音色（22 种）

| ID | 中文名 | 风格描述 | 适用场景 |
|----|--------|----------|----------|
| `Cherry` | 芊悦 | 阳光积极、亲切自然小姐姐 | 旁白、对话、通用（默认） |
| `Serena` | 苏瑶 | 温柔小姐姐 | 旁白、抒情内容 |
| `Chelsie` | 千雪 | 二次元虚拟女友 | 动漫、游戏内容 |
| `Momo` | 茉兔 | 撒娇搞怪，逗你开心 | 儿童内容、轻松场景 |
| `Vivian` | 十三 | 拽拽的、可爱的小暴躁 | 年轻角色、个性对话 |
| `Maia` | 四月 | 知性与温柔的碰撞 | 知识讲解、教育 |
| `Bella` | 萌宝 | 喝酒不打醉拳的小萝莉 | 儿童内容 |
| `Jennifer` | 詹妮弗 | 品牌级、电影质感般美语女声 | 广告、高端内容 |
| `Katerina` | 卡捷琳娜 | 御姐音色，韵律回味十足 | 成熟女性角色 |
| `Mia` | 乖小妹 | 温顺如春水，乖巧如初雪 | 温柔场景 |
| `Bellona` | 燕铮莺 | 声音洪亮，字正腔圆，千面人声 | 有声书、广播剧 |
| `Bunny` | 萌小姬 | "萌属性"爆棚的小萝莉 | 儿童内容、动漫 |
| `Elias` | 墨讲师 | 知识讲解，叙事技巧强 | 教育、知识类 |
| `Nini` | 邻家妹妹 | 糯米糍一样又软又黏 | 亲密场景、助眠 |
| `Ebona` | 诡婆婆 | 低语如钥匙，开启内心幽暗 | 恐怖、悬疑内容 |
| `Seren` | 小婉 | 温和舒缓，助你入眠 | 助眠、疗愈 |
| `Stella` | 少女阿月 | 甜美少女音，正义感满满 | 动漫、少女角色 |
| `Sonrisa` | 索尼莎 | 热情开朗的拉美大姐 | 西班牙语内容 |
| `Sohee` | 素熙 | 温柔开朗的韩国欧尼 | 韩语内容 |
| `Ono Anna` | 小野杏 | 鬼灵精怪的青梅竹马 | 日语内容、动漫 |
| `Jada` | 上海 - 阿珍 | 风风火火的沪上阿姐 | 上海话内容 |
| `Sunny` | 四川 - 晴儿 | 甜到你心里的川妹子 | 四川话内容 |
| `Kiki` | 粤语 - 阿清 | 甜美的港妹闺蜜 | 粤语内容 |

### 男声音色（22 种）

| ID | 中文名 | 风格描述 | 适用场景 |
|----|--------|----------|----------|
| `Ethan` | 晨煦 | 标准普通话，阳光温暖活力 | 旁白、通用 |
| `Moon` | 月白 | 率性帅气 | 年轻男性角色 |
| `Kai` | 凯 | 耳朵的一场 SPA | 旁白、抒情 |
| `Nofish` | 不吃鱼 | 不会翘舌音的设计师 | 轻松、幽默场景 |
| `Ryan` | 甜茶 | 节奏拉满，戏感炸裂 | 广告、戏剧性内容 |
| `Aiden` | 艾登 | 精通厨艺的美语大男孩 | 英语内容、生活类 |
| `Eldric Sage` | 沧明子 | 沉稳睿智的老者 | 新闻、严肃内容 |
| `Mochi` | 沙小弥 | 聪明伶俐的小大人 | 儿童内容 |
| `Vincent` | 田叔 | 沙哑烟嗓，千军万马与江湖豪情 | 有声书、历史内容 |
| `Neil` | 阿闻 | 专业新闻主持人 | 新闻播报 |
| `Arthur` | 徐大爷 | 质朴嗓音，岁月沉淀 | 故事讲述、乡村内容 |
| `Pip` | 顽屁小孩 | 调皮捣蛋却充满童真 | 儿童内容 |
| `Bodega` | 博德加 | 热情的西班牙大叔 | 西班牙语内容 |
| `Alek` | 阿列克 | 战斗民族的冷与暖 | 俄语内容 |
| `Dolce` | 多尔切 | 慵懒的意大利大叔 | 意大利语内容 |
| `Lenn` | 莱恩 | 理性叛逆的德国青年 | 德语内容 |
| `Emilien` | 埃米尔安 | 浪漫的法国大哥哥 | 法语内容 |
| `Andre` | 安德雷 | 磁性沉稳男生 | 通用旁白 |
| `Radio Gol` | 拉迪奥·戈尔 | 足球诗人解说 | 体育内容 |
| `Dylan` | 北京 - 晓东 | 北京胡同里长大的少年 | 北京话内容 |
| `Li` | 南京 - 老李 | 耐心的瑜伽老师 | 南京话、教学 |
| `Marcus` | 陕西 - 秦川 | 面宽话短，心实声沉 | 陕西话内容 |
| `Roy` | 闽南 - 阿杰 | 诙谐直爽的台湾哥仔 | 闽南语内容 |
| `Peter` | 天津 - 李彼得 | 天津相声专业捧哏 | 天津话、喜剧 |
| `Eric` | 四川 - 程川 | 跳脱市井的四川成都男子 | 四川话内容 |
| `Rocky` | 粤语 - 阿强 | 幽默风趣的阿强 | 粤语内容 |

### 推荐音色配置

| 场景类型 | 推荐女声 | 推荐男声 |
|----------|----------|----------|
| **旁白/通用（中文）** | Cherry | Ethan |
| **旁白/通用（英语）** | Maia | Aiden |
| **新闻播报** | Eldric Sage | Neil |
| **有声书/广播剧** | Bellona | Vincent |
| **教育/知识讲解** | Maia | Elias |
| **儿童内容** | Bella/Bunny | Mochi/Pip |
| **广告/营销** | Cherry/Ryan | Ryan |
| **助眠/疗愈** | Seren/Nini | Kai |
| **动漫/游戏** | Chelsie/Stella | Moon |
| **四川话内容** | Sunny | Eric |
| **粤语内容** | Kiki | Rocky |
| **北京话内容** | - | Dylan |
| **上海话内容** | Jada | - |

> **提示**：
> - **中文内容默认**：女声 Cherry（芊悦），男声 Ethan（晨煦）
> - **英语内容默认**：女声 Maia（四月），男声 Aiden（艾登）
> - Jennifer（詹妮弗）音色仅在 `qwen3-tts-flash` 模型中支持，在 `qwen3-tts-flash-realtime` 模型中不可用


### 使用示例

```bash
# 温柔女声旁白
python scripts/aliyun_tts.py --text "欢迎来到海洋世界" --voice Serena --output narration.mp3

# 新闻播报男声
python scripts/aliyun_tts.py --text "现在是北京时间上午十点" --voice Neil --output news.mp3

# 儿童故事
python scripts/aliyun_tts.py --text "从前有座山" --voice Bella --output story.mp3

# 四川话配音
python scripts/aliyun_tts.py --text "你好，吃了吗" --voice Sunny --output sichuan.mp3

# 粤语配音
python scripts/aliyun_tts.py --text "你好，食咗饭未啊" --voice Kiki --output cantonese.mp3

# 有声书（女声）
python scripts/aliyun_tts.py --text "话说天下大势" --voice Bellona --output audiobook.mp3

# 体育解说
python scripts/aliyun_tts.py --text "球进了！" --voice Radio Gol --output sports.mp3
```

## 注意事项

1. 使用项目中的 `bailian-api-key`（`config.yaml` → `tts.bailian-api-key`）
2. 输出格式推荐 `mp3`（浏览器兼容性最好）
3. 网络需能访问 `dashscope.aliyuncs.com`
