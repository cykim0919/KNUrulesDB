import os
import json
import time
from bs4 import BeautifulSoup
from datetime import datetime

# -------------------------------
# 🔧 경로 설정
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_DIR = os.path.join(BASE_DIR, "..", "crawler", "data", "html_requests")

# 📅 수집일(파일명에 포함)
today_str = datetime.now().strftime("%Y-%m-%d")
OUTPUT_JSON = os.path.join(BASE_DIR, f"rules_parsed_structured_{today_str}.json")

# -------------------------------
# 🔧 추출 키워드 및 필터 단어
# -------------------------------
KEYWORDS = ["구분", "관리부서", "제·개정", "호수", "공포일자", "내용", "첨부파일"]
FILTER_WORDS = ["다운로드", "보기", "첨부", "파일"]

# -------------------------------
# ✅ HTML 파일에서 표 데이터 추출
# -------------------------------
def extract_text_data(html_path):
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
    except UnicodeDecodeError:
        import chardet
        with open(html_path, "rb") as f:
            raw = f.read()
        enc = chardet.detect(raw)["encoding"]
        html = raw.decode(enc, errors="ignore")

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text("\n", strip=True)
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    data = {}
    current_key = None

    for i, line in enumerate(lines):
        for key in KEYWORDS:
            if key in line:
                current_key = key
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if any(bad in next_line for bad in FILTER_WORDS):
                        continue
                    if not any(k in next_line for k in KEYWORDS):
                        data[key] = next_line
                else:
                    data[key] = ""
                break

    attach_tag = soup.select_one("a[href*='downloadCmmAtchmnfl']")
    if attach_tag:
        href = attach_tag.get("href", "")
        if not href.startswith("http"):
            href = "https://wwwk.kangwon.ac.kr" + href
        filename = attach_tag.get_text(strip=True)
        data["첨부파일"] = {
            "파일명": filename,
            "다운로드링크": href
        }

    if "내용" in data and data["내용"]:
        data["학칙명"] = data["내용"]
    else:
        data["학칙명"] = os.path.splitext(os.path.basename(html_path))[0]

    return data if len(data) > 1 else None

# -------------------------------
# ✅ 전체 HTML 순회 + 구조화 JSON 생성
# -------------------------------
def parse_all_html_structured():
    start_time = time.time()
    files = [f for f in os.listdir(HTML_DIR) if f.endswith(".html")]
    all_data = []

    for idx, file in enumerate(sorted(files), 1):
        path = os.path.join(HTML_DIR, file)
        parsed = extract_text_data(path)
        if parsed:
            if parsed["학칙명"].startswith("regltn_"):
                parsed["학칙명"] = parsed.get("내용", "")
            all_data.append(parsed)
            print(f"[{idx}/{len(files)}] {file} → ✅ ({parsed.get('학칙명')})")
        else:
            print(f"[{idx}/{len(files)}] {file} → ⚠️ SKIP")

    elapsed_time = round(time.time() - start_time, 2)

    output_data = {
        "수집일": today_str,
        "수집 대상": "강원대학교 학칙/규정",
        "수집 설명": "강원대학교 학칙 크롤링",
        "수집시간": f"{elapsed_time}초",
        "내용": all_data
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ [완료] {len(all_data)}개 문서 JSON 저장 완료: {OUTPUT_JSON}")
    print(f"⏱️ 처리시간: {elapsed_time}s")

# -------------------------------
# 실행
# -------------------------------
if __name__ == "__main__":
    parse_all_html_structured()
