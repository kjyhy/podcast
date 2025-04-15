import arxiv
from datetime import datetime
import os

# ✅ TTS 스크립트 생성 함수
def wrap_for_tts(title, abstract, link):
    return (
        f"📢 오늘 소개할 논문은 '{title}'입니다.\n\n"
        f"🔗 논문 링크는 {link} 이고요,\n\n"
        f"{abstract}\n\n"
        f"이상으로 오늘의 논문 요약을 마칩니다. 감사합니다.\n"
    )

# ✅ arXiv 검색 설정
query = "(organic semiconductor OR OLED) AND (machine learning OR artificial intelligence) AND (device OR devices)"
today = datetime.today().strftime("%Y-%m-%d")
briefing_file = f"daily_briefing/daily_briefing_{today}.txt"
tts_file = f"daily_briefing/tts_script_{today}.txt"

search = arxiv.Search(
    query=query,
    max_results=3,
    sort_by=arxiv.SortCriterion.SubmittedDate,
    sort_order=arxiv.SortOrder.Descending,
)

client = arxiv.Client()
os.makedirs("daily_briefing", exist_ok=True)

# ✅ 요약 파일 생성
with open(briefing_file, "w", encoding="utf-8") as bf, open(tts_file, "w", encoding="utf-8") as tf:
    for result in client.results(search):
        title = result.title.strip()
        abstract = result.summary.strip()
        link = result.pdf_url

        bf.write(f"📄 Title: {title}\n")
        bf.write(f"🔗 Link: {link}\n\n")
        bf.write(f"🧠 Abstract:\n{abstract}\n")
        bf.write("=" * 60 + "\n\n")

        # ✅ TTS용 변환 및 저장
        tts_script = wrap_for_tts(title, abstract, link)
        tf.write(tts_script + "\n\n")

print(f"✅ 영어 요약 저장 완료 → {briefing_file}")
print(f"✅ TTS 스크립트 저장 완료 → {tts_file}")
