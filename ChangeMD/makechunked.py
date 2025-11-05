import json
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_md_oneline_to_json(md_oneline: str, chunk_size=500, chunk_overlap=100):
    # 텍스트 스플리터 설정
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n", " ", ""],
    )

    # 분할
    chunks = splitter.split_text(md_oneline)

    # JSON 변환
    result = [{"chunked": chunk, "vector": []} for chunk in chunks]
    return result


if __name__ == "__main__":
    # 예: oneline md 파일 읽기
    md_file = r"C:\Users\ideadesignlab\PycharmProjects\PythonProject\KNUrulesDB\ChangeMD\강원대학교 대학원 학사운영규정_utf8_oneline.txt"
    with open(md_file, "r", encoding="utf-8") as f:
        md_oneline = f.read()

    # 분할 후 JSON 변환
    result = split_md_oneline_to_json(md_oneline, chunk_size=500, chunk_overlap=100)

    # 저장
    output_file = r"C:\Users\ideadesignlab\PycharmProjects\PythonProject\KNUrulesDB\ChangeMD\강원대학교 대학원 학사운영규정_chunks.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"[완료] {len(result)}개 청크 생성됨 → {output_file}")
