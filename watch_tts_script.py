import os
import time
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

MAX_CHAR = 2000
WATCH_FOLDER = "daily_briefing"
SPLIT_FOLDER = os.path.join(WATCH_FOLDER, "split_scripts")
os.makedirs(SPLIT_FOLDER, exist_ok=True)

def split_text_by_sentence(text, max_len=MAX_CHAR):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())  # 문장 기준 분할
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_len:
            current_chunk += sentence + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

class TTSScriptHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and "tts_script" in event.src_path and event.src_path.endswith(".txt"):
            time.sleep(10)
            print(f"📄 감지된 파일: {event.src_path}")

            try:
                with open(event.src_path, "r", encoding="utf-8") as f:
                    text = f.read().strip()

                if not text:
                    print("⚠️ 감지된 파일이 비어 있습니다. 건너뜁니다.")
                    return

                base = os.path.basename(event.src_path).replace(".txt", "")
                chunks = split_text_by_sentence(text)

                for idx, chunk in enumerate(chunks, 1):
                    out_path = os.path.join(SPLIT_FOLDER, f"{base}_part{idx}.txt")
                    with open(out_path, "w", encoding="utf-8") as out_f:
                        out_f.write(chunk)

                print(f"✅ 문장 단위로 {len(chunks)}개로 분할 완료 → {SPLIT_FOLDER}/")

            except Exception as e:
                print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    print(f"📡 '{WATCH_FOLDER}/' 폴더 감시 중... (Ctrl+C로 종료)")
    observer = Observer()
    observer.schedule(TTSScriptHandler(), path=WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("🛑 감시 종료됨")
    observer.join()
