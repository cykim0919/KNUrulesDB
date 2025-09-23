import os

def md_to_single_line(md_path, output_path=None):
    # md 파일 읽기
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 개행(\n)을 문자열 리터럴 "\n"로 치환
    single_line = content.replace("\n", "\\n")

    # 결과 저장
    if not output_path:
        base, ext = os.path.splitext(md_path)
        output_path = base + "_oneline.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(single_line)

    print(f"[완료] 변환된 파일: {output_path}")


if __name__ == "__main__":
    md_file = r"C:\Users\ch901\PycharmProjects\ChangeMD\강원대학교 학칙_utf8.md"
    md_to_single_line(md_file)
