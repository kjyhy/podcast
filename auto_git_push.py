import subprocess
import os
from datetime import datetime

# Git 커밋 메시지 자동 생성
now = datetime.now().strftime("%Y-%m-%d %H:%M")
commit_msg = f"🌀 자동 RSS 갱신: {now}"

try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("✅ Git 자동 push 완료!")
except subprocess.CalledProcessError as e:
    print(f"❌ Git 명령어 실패: {e}")
