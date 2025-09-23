import win32com.client as win32
import os
from markdownify import markdownify as md


def hwp_to_html_utf8(hwp_path, output_dir=None):
    if output_dir is None:
        output_dir = os.path.dirname(hwp_path)

    base_name = os.path.splitext(os.path.basename(hwp_path))[0]
    html_path = os.path.join(output_dir, base_name + ".html")

    # HWP 실행
    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
    hwp.RegisterModule("FilePathCheckDLL", "SecurityModule")

    print(f"[INFO] HWP 열기: {hwp_path}")
    hwp.Open(hwp_path)

    # HTML로 저장
    hwp.SaveAs(html_path, "HTML")
    hwp.Quit()

    print(f"[완료] HWP → HTML 변환: {html_path}")

    # EUC-KR → UTF-8 인코딩 변환
    with open(html_path, "r", encoding="cp949", errors="ignore") as f:
        content = f.read()

    utf8_path = os.path.join(output_dir, base_name + "_utf8.html")
    with open(utf8_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[완료] HTML 인코딩 변환 (UTF-8): {utf8_path}")
    return utf8_path


def html_to_md(html_path, output_dir=None):
    if output_dir is None:
        output_dir = os.path.dirname(html_path)

    base_name = os.path.splitext(os.path.basename(html_path))[0]
    md_path = os.path.join(output_dir, base_name + ".md")

    # HTML → Markdown
    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        html_content = f.read()

    md_content = md(html_content)

    # NBSP 제거
    md_content = md_content.replace("NBSP", " ").replace("\u00A0", " ")

    # UTF-8로 저장 (문제되는 문자는 무시)
    with open(md_path, "w", encoding="utf-8", errors="ignore") as f:
        f.write(md_content)

    print(f"[완료] HTML → Markdown 변환: {md_path}")
    return md_path



if __name__ == "__main__":
    hwp_file = r"C:\Users\ch901\PycharmProjects\ChangeMD\강원대학교 대학원 학사운영규정.hwp"

    # 1. HWP → UTF-8 HTML
    html_utf8 = hwp_to_html_utf8(hwp_file)

    # 2. HTML(UTF-8) → Markdown (NBSP 제거 포함)
    md_file = html_to_md(html_utf8)

    print("[최종완료] 변환된 Markdown 파일:", md_file)
