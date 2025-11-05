import os

def md_to_single_line(md_path, output_path=None):
    # md 파일 읽기
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # JSON 안전하게 만들기
    # 개행 → \n 치환
    single_line = content.replace("\n", "\\n")
    # 큰따옴표 → \" 치환
    single_line = single_line.replace('"', '\\"')

    # 결과 저장
    if not output_path:
        base, ext = os.path.splitext(md_path)
        output_path = base + "_oneline.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(single_line)

    print(f"[완료] 변환된 파일: {output_path}")
    return single_line  # 함수 실행 후 문자열도 리턴


if __name__ == "__main__":
    md_file = r"C:\Users\ideadesignlab\PycharmProjects\PythonProject\KNUrulesDB\ChangeMD\강원대학교 대학원 학사운영규정_utf8.md"
    md_to_single_line(md_file)
