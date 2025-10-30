import os
import time
import win32com.client

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "..", "crawler", "data", "hwp_files_fast")
OUTPUT_DIR = os.path.join(BASE_DIR, "pdf_files")
os.makedirs(OUTPUT_DIR, exist_ok=True)

SECURITY_MODULE_PATH = r"C:\Users\ch901\OneDrive\바탕 화면\보안모듈(Automation)\FilePathCheckerModuleExample.dll"


def safe_create_hwp(max_retry=3):
    """한글 인스턴스를 안정적으로 생성 (RPC 오류 방지)"""
    for attempt in range(max_retry):
        try:
            hwp = win32com.client.Dispatch("HWPFrame.HwpObject")
            time.sleep(0.5)
            return hwp
        except Exception as e:
            print(f"[경고] HWP 연결 실패 ({attempt + 1}/{max_retry}): {e}")
            # RPC 서버 문제일 가능성 → 재시도
            os.system("taskkill /f /im Hwp.exe >nul 2>&1")
            time.sleep(2)
    raise RuntimeError("한글 RPC 서버에 연결할 수 없습니다.")


def hwp_to_pdf(hwp_path, pdf_path):
    try:
        hwp = safe_create_hwp()

        # 보안모듈 등록
        if os.path.exists(SECURITY_MODULE_PATH):
            hwp.RegisterModule("FilePathCheckDLL", SECURITY_MODULE_PATH)
        else:
            print(f"[경고] 보안 모듈 경로가 존재하지 않습니다: {SECURITY_MODULE_PATH}")

        # 파일 열기
        hwp.Open(hwp_path)
        time.sleep(0.3)

        # PDF 저장
        hwp.SaveAs(pdf_path, "PDF")
        print(f"[OK] {os.path.basename(hwp_path)} → PDF 변환 완료")

    except Exception as e:
        print(f"[ERROR] {os.path.basename(hwp_path)} 변환 실패: {e}")

    finally:
        try:
            hwp.Quit()
            time.sleep(0.3)
        except:
            os.system("taskkill /f /im Hwp.exe >nul 2>&1")


def convert_all():
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".hwp")]
    print(f"[INFO] 변환 대상 파일 수: {len(files)}")

    for idx, filename in enumerate(files, 1):
        hwp_path = os.path.join(INPUT_DIR, filename)
        pdf_path = os.path.join(OUTPUT_DIR, os.path.splitext(filename)[0] + ".pdf")

        if os.path.exists(pdf_path):
            print(f"[SKIP] 이미 변환됨: {filename}")
            continue

        print(f"[{idx}/{len(files)}] 변환 중: {filename}")
        hwp_to_pdf(hwp_path, pdf_path)

    print(f"\n[완료] 모든 HWP → PDF 변환이 끝났습니다.\n[DIR] {os.path.abspath(OUTPUT_DIR)}")


if __name__ == "__main__":
    convert_all()