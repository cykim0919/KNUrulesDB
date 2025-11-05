import json
from openai import OpenAI
from tqdm import tqdm

# 🔑 API Key 꼭 환경변수 OPENAI_API_KEY로 설정해두세요
client = OpenAI()

def embed_chunks(input_json, output_json, model_name="text-embedding-3-small", batch_size=50):
    # JSON 로드
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    # chunked 텍스트 수집
    texts = [item["chunked"] for item in data if item.get("chunked", "").strip()]
    print(f"[INFO] 총 {len(texts)}개의 청크 벡터화 시작 (모델: {model_name})")

    # 결과 저장할 리스트
    embeddings = []

    # OpenAI는 대량 입력도 처리 가능하지만, 안전하게 batch 단위로 자르기
    for i in tqdm(range(0, len(texts), batch_size), desc="Batches"):
        batch = texts[i:i+batch_size]
        response = client.embeddings.create(
            model=model_name,
            input=batch
        )
        batch_embeddings = [e.embedding for e in response.data]
        embeddings.extend(batch_embeddings)

    # 다시 매핑
    idx = 0
    for item in data:
        if item.get("chunked", "").strip():
            item["vector"] = embeddings[idx]
            idx += 1

    # 저장
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("[완료] 벡터 추가된 JSON 저장:", output_json)


if __name__ == "__main__":
    embed_chunks(
        input_json="강원대학교 대학원 학사운영규정_chunks.json",
        output_json="강원대학교 대학원 학사운영규정_chunks_embedded.json"
    )
