import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://wwwk.kangwon.ac.kr"
LIST_URL = f"{BASE_URL}/www/selectRegltnList.do"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
SAVE_DIR = "data/hwp_files_fast"
os.makedirs(SAVE_DIR, exist_ok=True)

def clean_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", name).strip()

def get_list_page(page_index: int) -> str:
    params = {"key": "2289", "pageUnit": "10", "searchCnd": "all", "searchSeCode": "", "pageIndex": page_index}
    r = requests.get(LIST_URL, params=params, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.text

def parse_list_page(html: str):
    soup = BeautifulSoup(html, "html.parser")
    results = []

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if "downloadCmmAtchmnfl.do" in href:
            file_url = urljoin(BASE_URL, href)

            # 같은 행(tr) 안의 제목 찾기
            tr = a.find_parent("tr")
            title_tag = tr.find("a", href=True) if tr else None
            title = clean_filename(title_tag.text.strip() if title_tag else "무제")

            results.append((title, file_url))

    print(f"[DEBUG] {len(results)}개의 다운로드 링크 추출 완료")
    return results

def download_file(url: str, save_path: str):
    try:
        r = requests.get(url, headers=HEADERS, stream=True, timeout=20)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        print(f"[SAVE] {os.path.basename(save_path)}")
    except Exception as e:
        print(f"[ERROR] 다운로드 실패: {url} ({e})")

def crawl_all(max_pages=60):
    total_downloads = 0

    for page in range(1, max_pages + 1):
        print(f"\n[INFO] {page} 페이지 처리 중...")
        html = get_list_page(page)
        files = parse_list_page(html)

        if not files:
            print("[INFO] 더 이상 데이터가 없습니다. 종료.")
            break

        for title, file_url in files:
            save_path = os.path.join(SAVE_DIR, f"{title}.hwp")
            if os.path.exists(save_path):
                print(f"[SKIP] 이미 존재: {title}")
                continue
            download_file(file_url, save_path)
            total_downloads += 1
            time.sleep(0.3)

    print(f"\n[DONE] 총 {total_downloads}개 파일 다운로드 완료.")
    print(f"[DIR] 저장 경로: {os.path.abspath(SAVE_DIR)}")

if __name__ == "__main__":
    crawl_all(max_pages=60)
