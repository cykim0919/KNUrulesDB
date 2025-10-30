import os
import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://wwwk.kangwon.ac.kr/www/selectRegltnIemList.do?key=2289&regltnNo="
SAVE_DIR = r"C:\Users\ch901\PycharmProjects\KNUrulesDB\src\crawler\data\html_requests"
os.makedirs(SAVE_DIR, exist_ok=True)

# 브라우저처럼 가장하기 위한 헤더
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/130.0.0.0 Safari/537.36"
}

def fetch_html(regltn_no):
    url = f"{BASE_URL}{regltn_no}"
    print(f"[INFO] {regltn_no}번 페이지 요청 중: {url}")

    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()

        html = res.text
        # 혹시 iframe이 있다면 soup로 내부 추출
        soup = BeautifulSoup(html, "html.parser")

        iframe = soup.select_one("iframe#ifrContents")
        if iframe and iframe.get("src"):
            iframe_src = "https://wwwk.kangwon.ac.kr" + iframe["src"]
            res_iframe = requests.get(iframe_src, headers=HEADERS)
            res_iframe.raise_for_status()
            html = res_iframe.text  # iframe 내부 페이지 내용으로 교체

        # 파일 저장
        path = os.path.join(SAVE_DIR, f"regltn_{regltn_no}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[OK] {regltn_no}번 저장 완료: {path}")

    except Exception as e:
        print(f"[ERR] {regltn_no}번 실패: {e}")

if __name__ == "__main__":
    for i in range(0, 430):
        fetch_html(i)
        time.sleep(0.3)  # 서버 부하 방지
    print("\n✅ 모든 HTML 다운로드 완료.")
