from feedgen.feed import FeedGenerator
from datetime import datetime
import os

def generate_rss():
    fg = FeedGenerator()
    fg.title("AI 논문 요약 팟캐스트")
    
    #fg.link(href="http://yourdomain.com/rss", rel="self")
    fg.link(href="https://github.com/kjyhy/podcast.git", rel="self")
    fg.description("AI 및 소재/디바이스 논문을 요약하여 팟캐스트로 전달합니다.")
    fg.language("ko")

    mp3_dir = "mp3"
    for filename in sorted(os.listdir(mp3_dir), reverse=True):
        if filename.endswith(".mp3"):
            date = filename.replace(".mp3", "")
            fe = fg.add_entry()
            fe.title(f"{date} 논문 요약")
            fe.pubDate(datetime.strptime(date, "%Y-%m-%d"))
            fe.enclosure(f"http://yourdomain.com/mp3/{filename}", 0, "audio/mpeg")
            fe.description(f"{date} 논문 요약 음성입니다.")

    fg.rss_file("feed.xml")
    print("✅ feed.xml 생성 완료!")

generate_rss()
