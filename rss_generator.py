from feedgen.feed import FeedGenerator
from datetime import datetime
from pathlib import Path
from html import escape
import os
import subprocess

# === 설정 ===
SITE_URL = "https://kjyhy.github.io/podcast"
FEED_FILE = "feed.xml"
MP3_FOLDER = "mp3"
TTS_FOLDER = "daily_briefing"

# === 피드 생성 ===
fg = FeedGenerator()
fg.load_extension('podcast')

fg.title("AI 논문 요약 팟캐스트")
fg.link(href=SITE_URL, rel='alternate')
fg.description("최신 인공지능 논문을 요약하고 음성으로 제공합니다.")
fg.language("ko")
fg.generator("python-feedgen")
fg.docs("http://www.rssboard.org/rss-specification")
fg.podcast.itunes_category('Technology')
fg.podcast.itunes_author("Jane Kang")
fg.podcast.itunes_summary("매일 업데이트되는 AI 논문 오디오 요약")
fg.podcast.itunes_explicit("no")
fg.podcast.itunes_image(f"{SITE_URL}/cover.jpg")
fg.atom_link(href=f"{SITE_URL}/feed.xml", rel="self")

# === mp3 파일 순회 ===
mp3_files = sorted(Path(MP3_FOLDER).glob("*.mp3"))

for mp3_path in mp3_files:
    date_str = mp3_path.stem  # e.g., "2025-04-25"
    mp3_url = f"{SITE_URL}/{MP3_FOLDER}/{mp3_path.name}"
    mp3_size = os.path.getsize(mp3_path)

    # 해당 날짜의 텍스트 설명 파일
    txt_path = Path(TTS_FOLDER) / f"tts_script_{date_str}.txt"
    if not txt_path.exists():
        print(f"⚠️ {txt_path.name} 없음. 건너뜁니다.")
        continue

    with open(txt_path, encoding='utf-8') as f:
        summary_text = f.read()

    # XML-safe 이스케이프
    escaped_description = escape(summary_text)

    # 날짜 포맷
    pub_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%a, %d %b %Y 07:00:00 +0000")

    fg.add_item(
        title=f"{date_str} 논문 요약",
        description=escaped_description,
        link=SITE_URL,
        guid=date_str,
        pubDate=pub_date,
        enclosure={
            "url": mp3_url,
            "length": str(mp3_size),
            "type": "audio/mpeg"
        }
    )

# === XML 저장 ===
fg.rss_file(FEED_FILE)
print(f"✅ {FEED_FILE} 생성 완료")

# === Git 자동 푸시 ===
try:
    subprocess.run(["git", "add", FEED_FILE], check=True)
    subprocess.run(["git", "commit", "-m", f"🔄 RSS feed 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("🚀 GitHub에 자동 push 완료")
except subprocess.CalledProcessError as e:
    print(f"⚠️ Git 자동화 실패: {e}")
