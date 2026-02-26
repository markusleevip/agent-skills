import os
import sys
import json
import asyncio
import base64
import time
import argparse
import subprocess

# Default configuration - matches Go backend (config/tts.go GetBailianURL)
# IMPORTANT: Use /realtime endpoint (OpenAI-compatible), NOT /inference/ (native DashScope)
DEFAULT_URL = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime"
DEFAULT_MODEL = "qwen3-tts-flash-realtime"
DEFAULT_FORMAT = "mp3"
DEFAULT_SAMPLE_RATE = 16000
DEFAULT_VOICE = "Cherry"

# Available Bailian voice IDs (same as Go backend BailianVoicesList)
VOICES = {
    # Female Voices
    "Cherry":   ("芊悦",     "female", "阳光积极（默认）"),
    "Serena":   ("苏瑶",     "female", "温柔小姐姐"),
    "Chelsie":  ("千雪",     "female", "二次元虚拟女友"),
    "Momo":     ("茉兔",     "female", "撒娇搞怪"),
    "Vivian":   ("十三",     "female", "可爱小暴躁"),
    "Maia":     ("四月",     "female", "知性温柔"),
    "Bella":    ("萌宝",     "female", "小萝莉"),
    "Jennifer": ("詹妮弗",   "female", "电影质感（仅部分模型）"),
    "Katerina": ("卡捷琳娜", "female", "御姐音色"),
    "Mia":      ("乖小妹",   "female", "乖巧温顺"),
    "Bellona":  ("燕铮莺",   "female", "字正腔圆"),
    "Bunny":    ("萌小姬",   "female", "萌属性萝莉"),
    "Elias":    ("墨讲师",   "female", "叙事讲解"),
    "Nini":     ("邻家妹妹", "female", "软黏助眠"),
    "Ebona":    ("诡婆婆",   "female", "恐怖悬疑"),
    "Seren":    ("小婉",     "female", "温和舒缓"),
    "Stella":   ("少女阿月", "female", "甜美少女"),
    "Sonrisa":  ("索尼莎",   "female", "拉美大姐"),
    "Sohee":    ("素熙",     "female", "韩国欧尼"),
    "Ono Anna": ("小野杏",   "female", "日语青梅竹马"),
    "Jada":     ("上海-阿珍","female", "沪上阿姐"),
    "Sunny":    ("四川-晴儿","female", "川味甜心"),
    "Kiki":     ("粤语-阿清","female", "港味闺蜜"),

    # Male Voices
    "Ethan":    ("晨煦",     "male",   "阳光温暖（默认）"),
    "Moon":     ("月白",     "male",   "率性帅气"),
    "Kai":      ("凯",       "male",   "磁性抒情"),
    "Nofish":   ("不吃鱼",   "male",   "幽默设计师"),
    "Ryan":     ("甜茶",     "male",   "节奏炸裂"),
    "Aiden":    ("艾登",     "male",   "美语大男孩"),
    "Eldric Sage": ("沧明子", "male", "沉稳睿智"),
    "Mochi":    ("沙小弥",   "male",   "聪明小大人"),
    "Vincent":  ("田叔",     "male",   "沙哑烟嗓"),
    "Neil":     ("阿闻",     "male",   "新闻主播"),
    "Arthur":   ("徐大爷",   "male",   "质朴厚重"),
    "Pip":      ("顽屁小孩", "male",   "调皮童真"),
    "Bodega":   ("博德加",   "male",   "西班牙大叔"),
    "Alek":     ("阿列克",   "male",   "战斗民族"),
    "Dolce":    ("多尔切",   "male",   "意大利大叔"),
    "Lenn":     ("莱恩",     "male",   "德语青年"),
    "Emilien":  ("埃米尔安", "male",   "浪漫法漫"),
    "Andre":    ("安德雷",   "male",   "磁性沉稳"),
    "Radio Gol": ("拉迪奥",   "male",   "体育解说"),
    "Dylan":    ("北京-晓东","male",   "老北京少年"),
    "Li":       ("南京-老李","male",   "耐心讲师"),
    "Marcus":   ("陕西-秦川","male",   "西北豪杰"),
    "Roy":      ("闽南-阿杰","male",   "戏谑台男"),
    "Peter":    ("天津-李彼得","male",  "相声捧哏"),
    "Eric":     ("四川-程川","male",   "川渝市井"),
    "Rocky":    ("粤语-阿强","male",   "风趣港男"),
}
LEGACY_VOICE_MAP = {
    "zh_female_qingxin": "Cherry",
    "zh_male_jingpin":   "Ethan",
}


def map_voice(voice_id: str) -> str:
    if not voice_id:
        return "Cherry"
    if voice_id in VOICES:
        return voice_id
    mapped = LEGACY_VOICE_MAP.get(voice_id)
    if mapped:
        return mapped
    print(f"[WARN] Unknown voice '{voice_id}', defaulting to Cherry")
    return "Cherry"


class BailianRealtimeTTS:
    """
    Aliyun Bailian Realtime TTS using OpenAI-compatible WebSocket protocol.
    Endpoint: wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=<model>
    Protocol: session.update -> input_text_buffer.append -> session.finish
    Matches Go backend implementation in tts_bailian.go
    """

    def __init__(self, api_key, model=None, voice=None, fmt=None, sample_rate=None, url=None):
        self.api_key = api_key
        self.model = model or DEFAULT_MODEL
        self.voice = map_voice(voice or DEFAULT_VOICE)
        self.format = fmt or DEFAULT_FORMAT
        self.sample_rate = sample_rate or DEFAULT_SAMPLE_RATE
        # Build URL with model query param (same as Go's GetBailianURL)
        base = url or DEFAULT_URL
        self.url = f"{base}?model={self.model}" if "model=" not in base else base
        self.audio_data = bytearray()
        self._session_ready = asyncio.Event()

    async def synthesize(self, text: str, output_file: str):
        try:
            import websockets
        except ImportError:
            return False, "Run --install-deps first."

        headers = {"Authorization": f"Bearer {self.api_key}"}
        ts = lambda: f"event_{int(time.time() * 1000)}"

        try:
            async with websockets.connect(self.url, additional_headers=headers, compression=None) as ws:
                # Start background receiver (like Go's goroutine)
                recv_task = asyncio.create_task(self._recv_loop(ws))

                # 1. Wait 100ms for connection (matches Go: time.Sleep(100ms))
                await asyncio.sleep(0.1)

                # 2. Send session.update
                await ws.send(json.dumps({
                    "type": "session.update",
                    "event_id": ts(),
                    "session": {
                        "voice": self.voice,
                        "response_format": self.format,
                        "sample_rate": self.sample_rate,
                        "mode": "server_commit",
                    },
                }))
                print(f"[INFO] session.update sent  voice={self.voice}  format={self.format}")

                # 3. Wait for session.created or session.updated (CRITICAL - matches Go's sessionReady chan)
                try:
                    await asyncio.wait_for(self._session_ready.wait(), timeout=5.0)
                    print("[INFO] Session ready")
                except asyncio.TimeoutError:
                    print("[WARN] Timeout waiting for session ready, proceeding anyway")

                # 4. Send text (matches Go: AppendText)
                await ws.send(json.dumps({
                    "type": "input_text_buffer.append",
                    "event_id": ts(),
                    "text": text,
                }))
                print(f"[INFO] Text sent ({len(text)} chars)")

                # 5. Wait 300ms (matches Go: time.Sleep(300ms))
                await asyncio.sleep(0.3)

                # 6. Finish (matches Go: Finish)
                await ws.send(json.dumps({
                    "type": "session.finish",
                    "event_id": ts(),
                }))
                print("[INFO] session.finish sent, awaiting audio...")

                # 7. Wait for recv_task to complete (response.done)
                try:
                    await asyncio.wait_for(recv_task, timeout=30.0)
                except asyncio.TimeoutError:
                    recv_task.cancel()
                    return False, "Timeout waiting for audio"

        except Exception as e:
            return False, f"Connection error: {e}"

        if not self.audio_data:
            return False, "No audio data received"

        out_dir = os.path.dirname(os.path.abspath(output_file))
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(output_file, "wb") as f:
            f.write(self.audio_data)
        return True, f"✅ Saved to {output_file}  ({len(self.audio_data):,} bytes)"

    async def _recv_loop(self, ws):
        """Matches Go's handleEvent / ReceiveMessages logic"""
        try:
            async for raw in ws:
                if isinstance(raw, bytes):
                    self.audio_data.extend(raw)
                    continue
                try:
                    ev = json.loads(raw)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    print(f"[WARN] Unparseable message: {repr(raw)[:120]}")
                    continue

                t = ev.get("type", "")

                if t in ("session.created", "session.updated"):
                    print(f"[INFO] {t} ✓")
                    self._session_ready.set()

                elif t == "response.audio.delta":
                    delta = ev.get("delta", "")
                    if delta:
                        self.audio_data.extend(base64.b64decode(delta))

                elif t == "response.done":
                    print(f"[INFO] response.done — total audio {len(self.audio_data):,} bytes")
                    break

                elif t == "error":
                    err = ev.get("error", ev)
                    print(f"[ERROR] Server error: {json.dumps(err, ensure_ascii=False)}")
                    break

                elif t in ("response.audio.done", "response.created", "session.finished",
                           "response.output_item.added", "response.output_item.done",
                           "response.content_part.added", "response.content_part.done"):
                    print(f"[INFO] {t}")

                else:
                    print(f"[DEBUG] unknown event type='{t}'  msg={json.dumps(ev, ensure_ascii=False)[:200]}")
        except Exception as e:
            print(f"[WARN] recv_loop exited: {e}")


async def main():
    parser = argparse.ArgumentParser(description="Aliyun Bailian Realtime TTS")
    parser.add_argument("--text",        type=str, help="Text to synthesize (required)")
    parser.add_argument("--output",      type=str, default="output.mp3",   help="Output file (default: output.mp3)")
    parser.add_argument("--api_key",     type=str, help="DashScope API Key")
    parser.add_argument("--model",       type=str, default=DEFAULT_MODEL,  help=f"Model (default: {DEFAULT_MODEL})")
    parser.add_argument("--voice",       type=str, default=DEFAULT_VOICE,  help="Voice: Cherry Serena Ethan Ryan Kai ...")
    parser.add_argument("--format",      type=str, default=DEFAULT_FORMAT, help="Format: mp3 pcm opus (default: mp3)")
    parser.add_argument("--sample_rate", type=int, default=DEFAULT_SAMPLE_RATE)
    parser.add_argument("--url",         type=str, default=DEFAULT_URL,    help="WebSocket base URL")
    parser.add_argument("--install-deps", action="store_true", help="Install websockets")
    parser.add_argument("--list-voices", action="store_true")
    args = parser.parse_args()

    if args.install_deps:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets"])
        print("✅ websockets installed")
        return

    if args.list_voices:
        print(f"{'ID':<15} {'Name':<14} {'Gender':<8} Description")
        print("-" * 58)
        for vid, (name, gender, desc) in VOICES.items():
            print(f"{vid:<15} {name:<14} {gender:<8} {desc}")
        return

    if not args.text:
        parser.print_help()
        return

    api_key = args.api_key or os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("Error: provide --api_key or set DASHSCOPE_API_KEY")
        sys.exit(1)

    client = BailianRealtimeTTS(
        api_key=api_key,
        model=args.model,
        voice=args.voice,
        fmt=args.format,
        sample_rate=args.sample_rate,
        url=args.url,
    )
    print(f"[INFO] Synthesizing: '{args.text}'")
    print(f"[INFO] URL: {client.url}")
    success, msg = await client.synthesize(args.text, args.output)
    print(msg)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
