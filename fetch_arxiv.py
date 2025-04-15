import arxiv
from datetime import datetime
import os

today_str = datetime.today().strftime("%Y-%m-%d")

query = "(artificial intelligence OR machine learning OR deep learning) AND (organic material OR flexible device OR semiconductor)"

search = arxiv.Search(
    query=query,
    max_results=5,
    sort_by=arxiv.SortCriterion.SubmittedDate,
    sort_order=arxiv.SortOrder.Descending
)

with open("daily_summary.txt", "w", encoding="utf-8") as f:
    for result in search.results():
        f.write(f"📄 제목: {result.title.strip()}\n")
        f.write(f"👨‍🔬 저자: {', '.join(a.name for a in result.authors)}\n")
        f.write(f"📅 날짜: {result.published.date()}\n")
        f.write(f"📄 초록:\n{result.summary.strip()}\n")
        f.write(f"🔗 링크: {result.pdf_url}\n")
