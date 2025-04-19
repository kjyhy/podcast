from feedgen.feed import FeedGenerator
from datetime import datetime
import os
import subprocess  # ✅ 이 줄 추가해야 에러 안 남

SITE_URL = "https://kjyhy.github.io/podcast/"
MP3_FOLDER = "mp3"
TXT_FOLDER = "daily_briefing"
AUTHOR_NAME = "Jane Kang"
COVER_IMAGE_URL = SITE_URL + "cover.jpg"

def generate_rss():
    fg = FeedGenerator()
    fg.load_extension('podcast')

    fg.title("AI 논문 요약 팟캐스트")
    fg.link(href=SITE_URL, rel='alternate')
    fg.description("최신 인공지능 논문을 요약하고 음성으로 제공합니다.")
    fg.language("ko")
    fg.podcast.itunes_author(AUTHOR_NAME)
    fg.podcast.itunes_image(COVER_IMAGE_URL)
    fg.podcast.itunes_summary("매일 업데이트되는 AI 논문 오디오 요약")
    fg.podcast.itunes_explicit("no")
    fg.podcast.itunes_category("Technology")

    for filename in sorted(os.listdir(MP3_FOLDER), reverse=True):
        if filename.endswith(".mp3"):
            date_str = filename.replace(".mp3", "")
            pub_date = datetime.strptime(date_str, "%Y-%m-%d")

            txt_path = os.path.join(TXT_FOLDER, f"tts_script_{date_str}.txt")
            if os.path.exists(txt_path):
                with open(txt_path, "r", encoding="utf-8") as f:
                    description = f.read().strip()
            else:
                description = f"{date_str} 논문 요약입니다."

            mp3_path = os.path.join(MP3_FOLDER, filename)
            length = os.path.getsize(mp3_path)

            fe = fg.add_entry()
            fe.title(f"{date_str} 논문 요약")
            fe.description(description)
            fe.guid(date_str)
            fe.pubDate(pub_date.strftime("%a, %d %b %Y 07:00:00 +0000"))
            fe.enclosure(f"{SITE_URL}mp3/{filename}", str(length), "audio/mpeg")

    fg.rss_file("feed.xml")
    print("✅ feed.xml 생성 완료!")

if __name__ == "__main__":
    generate_rss()
    try:
        subprocess.run(["python", "auto_git_push.py"])
    except Exception as e:
        print(f"❌ Git 자동 push 실패: {e}")
