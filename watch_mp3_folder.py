import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

# 감시할 폴더
WATCH_FOLDER = "mp3"
EXTENSION = ".mp3"

class MP3Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(EXTENSION):
            print(f"🎧 새 mp3 파일 감지됨: {event.src_path}")
            print("🌀 rss_generator.py 실행 중...")
            subprocess.run(["python", "rss_generator.py"])
            print("✅ feed.xml 자동 갱신 완료!\n")

if __name__ == "__main__":
    print(f"📡 '{WATCH_FOLDER}/' 폴더 감시 시작 (Ctrl+C로 종료)")
    observer = Observer()
    observer.schedule(MP3Handler(), path=WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("🛑 감시 종료됨")
    observer.join()
