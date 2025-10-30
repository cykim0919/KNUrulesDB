import os
import json
import time
import requests
import win32com.client
from datetime import datetime

# -------------------------------
# 경로 설정
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json_files")
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
PDF_DIR = os.path.join(BASE_DIR, "pdfs")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

SECURITY_MODULE_PATH = r"C:\Users\ch901\OneDrive\바탕 화면\보안모듈(Automation)\FilePathCheckerModuleExample.dll"

# -------------------------------
# 1️⃣ 변화 감지 함수
# -------------------------------
def detect_updates(old_json, new_json):
    with open(old_json, "r", encoding="utf-8") as f:
        old_data = json.load(f)
    with open(new_json, "r", encoding="utf-8") as f:
        new_data = json.load(f)

    old_rules = {d["학칙명"]: d for d in old_data["내용"]}
    new_rules = {d["학칙명"]: d for d in new_data["내용"]}

    updated = []

    for name, new_item in new_rules.items():
        old_item = old_rules.get(name)
        if not old_item:
            updated.append(new_item)
            continue

        changed = False

        # ✅ 날짜 변경 확인
        if old_item.get("공포일자") != new_item.get("공포일자"):
            changed = True
        if old_item.get("관리부서") != new_item.get("관리부서"):
            changed = True
        # ✅ 첨부파일 구조 안정화
        old_attach = old_item.get("첨부파일", {})
        new_attach = new_item.get("첨부파일", {})
        if isinstance(old_attach, str):
            old_attach = {}
        if isinstance(new_attach, str):
            new_attach = {}

        if old_attach.get("파일명") != new_attach.get("파일명"):
            changed = True

        # ✅ 내용 변경 확인
        if old_item.get("내용") != new_item.get("내용"):
            changed = True

        if changed:
            updated.append(new_item)

    return updated


# -------------------------------
# 2️⃣ 파일 다운로드 함수
# -------------------------------
def download_file(url, save_path):
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(r.content)
        print(f"[OK] 다운로드 완료: {os.path.basename(save_path)}")
        return True
    except Exception as e:
        print(f"[ERR] 다운로드 실패: {url} ({e})")
        return False


# -------------------------------
# 3️⃣ HWP → PDF 변환 함수
# -------------------------------
def hwp_to_pdf(hwp_path, pdf_path):
    try:
        hwp = win32com.client.gencache.EnsureDispatch("HWPFrame.HwpObject")
        hwp.RegisterModule("FilePathCheckDLL", SECURITY_MODULE_PATH)
        hwp.Open(hwp_path)
        hwp.SaveAs(pdf_path, "PDF")
        hwp.Quit()
        print(f"[OK] PDF 변환 완료: {os.path.basename(pdf_path)}")
    except Exception as e:
        print(f"[ERR] PDF 변환 실패: {e}")


# -------------------------------
# 4️⃣ 전체 파이프라인 실행
# -------------------------------
def run_update_pipeline(old_json, new_json):
    start = time.time()

    print("[INFO] 변화 감지 중...")
    updated_rules = detect_updates(old_json, new_json)
    print(f"[INFO] 변경된 학칙 수: {len(updated_rules)}")

    if not updated_rules:
        print("[DONE] 변경된 학칙이 없습니다.")
        return

    for rule in updated_rules:
        name = rule["학칙명"].replace("/", "_").replace(" ", "_")
        attach = rule.get("첨부파일", {})
        url = attach.get("다운로드링크")

        if not url:
            continue

        hwp_path = os.path.join(DOWNLOAD_DIR, f"{name}.hwp")
        pdf_path = os.path.join(PDF_DIR, f"{name}.pdf")

        # ① 파일 다운로드
        if download_file(url, hwp_path):
            # ② PDF 변환
            hwp_to_pdf(hwp_path, pdf_path)

    elapsed = round(time.time() - start, 2)
    print(f"\n✅ 전체 프로세스 완료 (소요시간: {elapsed}s)")


# -------------------------------
#  실행
# -------------------------------
if __name__ == "__main__":
    old_file = input("이전 JSON 파일 이름 입력: ").strip()
    new_file = input("최신 JSON 파일 이름 입력: ").strip()
    run_update_pipeline(old_file, new_file)
