# md 파일 읽기 예제
def read_md(md_path):
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
        print("[완료] MD 파일 읽기 성공")
        return content
    except UnicodeDecodeError:
        # 혹시 UTF-8 아닌 경우 대비
        with open(md_path, "r", encoding="cp949", errors="ignore") as f:
            content = f.read()
        print("[경고] UTF-8 아님 → CP949로 강제 변환")
        return content


if __name__ == "__main__":
    md_file = r"C:\Users\ch901\PycharmProjects\ChangeMD\강원대학교 학칙_utf8.md"   # 실제 md 파일 경로 입력
    text = read_md(md_file)
    print("=== 파일 내용 미리보기 ===")
    print(text[:1000])
