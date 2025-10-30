import json
import os
from datetime import datetime
from deepdiff import DeepDiff  # pip install deepdiff

# -------------------------------
# 기본 설정
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

old_name = input("이전 파일 이름 입력: ").strip()
new_name = input("최신 파일 이름 입력: ").strip()

old_file = old_name if os.path.isabs(old_name) else os.path.join(BASE_DIR, old_name)
new_file = new_name if os.path.isabs(new_name) else os.path.join(BASE_DIR, new_name)

# -------------------------------
# JSON 로드 함수
# -------------------------------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# -------------------------------
# 비교 함수
# -------------------------------
def compare_rules(old_data, new_data):
    old_rules = {r.get("학칙명", f"unknown_old_{i}"): r for i, r in enumerate(old_data.get("내용", []))}
    new_rules = {r.get("학칙명", f"unknown_new_{i}"): r for i, r in enumerate(new_data.get("내용", []))}

    added = [new_rules[k] for k in new_rules if k not in old_rules]
    removed = [old_rules[k] for k in old_rules if k not in new_rules]

    modified = []
    for name in new_rules:
        if name in old_rules and new_rules[name] != old_rules[name]:
            diff = DeepDiff(old_rules[name], new_rules[name], ignore_order=True).to_dict()
            modified.append({
                "학칙명": name,
                "변경사항": diff
            })

    return added, removed, modified

# -------------------------------
# 실행
# -------------------------------
if __name__ == "__main__":
    print("\n[INFO] JSON 비교 시작...\n")

    old_data = load_json(old_file)
    new_data = load_json(new_file)

    added, removed, modified = compare_rules(old_data, new_data)

    # 결과 요약
    result_summary = {
        "비교일": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "비교대상": {
            "이전파일": os.path.basename(old_file),
            "최신파일": os.path.basename(new_file)
        },
        "통계": {
            "추가된 항목": len(added),
            "삭제된 항목": len(removed),
            "수정된 항목": len(modified)
        },
        "결과": {
            "추가": added,
            "삭제": removed,
            "수정": modified
        }
    }

    # 결과 파일 이름
    output_file = os.path.join(
        BASE_DIR,
        f"compare_result_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result_summary, f, ensure_ascii=False, indent=2)

    print(f"✅ 비교 완료. 결과 저장됨 → {output_file}")
