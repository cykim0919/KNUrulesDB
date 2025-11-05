import os
import json
from datetime import datetime
from deepdiff import DeepDiff  # pip install deepdiff


# -------------------------------
# 🔧 JSON 로드 함수
# -------------------------------
def load_json(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ 파일을 찾을 수 없습니다: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# -------------------------------
# 🔧 파일명 기준 비교 함수 (첨부파일 dict/str 모두 처리)
# -------------------------------
def detect_updates_file_based(old_json, new_json):
    old_items = old_json.get("내용", [])
    new_items = new_json.get("내용", [])

    def safe_filename(item):
        """첨부파일이 dict 또는 str일 때 모두 안전하게 파일명 추출"""
        attach = item.get("첨부파일", {})
        if isinstance(attach, dict):
            return attach.get("파일명", "").strip()
        elif isinstance(attach, str):
            return attach.strip()
        return ""

    # 🔹 파일명 기준 dict 생성
    old_dict = {safe_filename(item): item for item in old_items if safe_filename(item)}
    new_dict = {safe_filename(item): item for item in new_items if safe_filename(item)}

    added, changed = [], []

    # 🔹 신규 파일
    for fname, new_item in new_dict.items():
        if fname not in old_dict:
            added.append(new_item)
        else:
            # 🔹 기존 파일과 비교하여 변경사항 감지
            old_item = old_dict[fname]
            diff = DeepDiff(old_item, new_item, ignore_order=True)
            if diff:
                changed.append({
                    "파일명": fname,
                    "이전값": old_item,
                    "변경후": new_item,
                    "변경세부": diff.to_dict()
                })

    return added, changed


# -------------------------------
# ✅ 결과 저장 함수
# -------------------------------
def save_result(added, changed):
    date = datetime.now().strftime("%Y-%m-%d")
    output_name = f"rules_update_filebased_{date}.json"
    output_path = os.path.join(os.path.dirname(__file__), output_name)

    result = {
        "비교일": date,
        "신규 항목 수": len(added),
        "변경 항목 수": len(changed),
        "신규 항목": added,
        "변경 항목": changed
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n✅ [완료] 신규 {len(added)}개 / 변경 {len(changed)}개 저장됨")
    print(f"📁 결과 파일: {output_path}")


# -------------------------------
# 🚀 실행부
# -------------------------------
if __name__ == "__main__":
    old_file = input("이전 JSON 파일 이름 입력: ").strip()
    new_file = input("최신 JSON 파일 이름 입력: ").strip()

    print("\n[INFO] 파일명 기준 JSON 비교 중...")

    try:
        old_json = load_json(old_file)
        new_json = load_json(new_file)
    except Exception as e:
        print(f"[ERROR] 파일 로드 실패: {e}")
        exit(1)

    added, changed = detect_updates_file_based(old_json, new_json)
    save_result(added, changed)
