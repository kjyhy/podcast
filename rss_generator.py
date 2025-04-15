from feedgen.feed import FeedGenerator
from datetime import datetime
import subprocess
import os

# 설정
SITE_URL = "https://kjyhy.github.io/podcast/"
MP3_FOLDER = "mp3"
AUTHOR_NAME = "Jane Kang"
COVER_IMAGE_URL = SITE_URL + "cover.jpg"  # cover.jpg는 저장소 루트에 업로드

def generate_rss():
    fg = FeedGenerator()
    fg.load_extension('podcast')

    fg.title("AI 논문 요약 팟캐스트")
    fg.link(href=SITE_URL, rel='alternate')
    fg.description("최신 인공지능/머신러닝 논문을 요약하고 음성으로 전달합니다.")
    fg.language("ko")
    fg.podcast.itunes_author(AUTHOR_NAME)
    fg.podcast.itunes_image(COVER_IMAGE_URL)
    fg.podcast.itunes_summary("매주 업데이트되는 AI 논문 오디오 요약")
    fg.podcast.itunes_explicit("no")
    fg.podcast.itunes_category("Technology")

    for filename in sorted(os.listdir(MP3_FOLDER), reverse=True):
        if filename.endswith(".mp3"):
            date_str = filename.replace(".mp3", "")
            try:
                pub_date = datetime.strptime(date_str, "%Y-%m-%d")
            except:
                continue  # 날짜 형식이 잘못된 파일은 무시

            fe = fg.add_entry()
            fe.title(f"{date_str} 논문 요약")
            fe.guid(date_str)
            fe.pubDate(pub_date)
            fe.description(f"{date_str} 논문 오디오 요약입니다.")
            fe.enclosure(f"{SITE_URL}mp3/{filename}", 0, "audio/mpeg")

    fg.rss_file("feed.xml")
    print("✅ RSS feed.xml 생성 완료!")

if __name__ == "__main__":
    generate_rss()
    subprocess.run(["python", "auto_git_push.py"])

