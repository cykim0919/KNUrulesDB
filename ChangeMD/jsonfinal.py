import json
import os
from datetime import datetime

def build_rule_json(meta, md_file, embedded_chunks_file, collected_at=None):
    """
    meta: dict - 규정 메타데이터
    md_file: str - markdown 파일 경로
    embedded_chunks_file: str - chunks_embedded.json 경로
    collected_at: str - 수집일 (없으면 오늘 날짜)
    """
    # 1. original 읽기 (개행 → \n 변환)
    with open(md_file, "r", encoding="utf-8") as f:
        original_text = f.read().replace("\n", "\\n")

    # 2. embedded_chunks 읽기
    with open(embedded_chunks_file, "r", encoding="utf-8") as f:
        embedded_chunks = json.load(f)

    # 3. 규정 JSON 구성
    rule_json = {
        "title": meta.get("title", ""),
        "category": meta.get("category", ""),
        "url": meta.get("url", ""),
        "department": meta.get("department", ""),
        "revision": meta.get("revision", ""),
        "number": meta.get("number", ""),
        "date": meta.get("date", ""),
        "attachment": meta.get("attachment", []),
        "attachment_content": [
            {
                "original": original_text,
                "imbed": embedded_chunks
            }
        ]
    }

    # 수집일 없으면 오늘 날짜
    if collected_at is None:
        collected_at = datetime.today().strftime("%Y-%m-%d")

    # attachment에 수집일 채워주기
    for att in rule_json["attachment"]:
        if "collected_at" not in att or not att["collected_at"]:
            att["collected_at"] = collected_at

    return rule_json


if __name__ == "__main__":
    # ✅ 규정별 메타데이터 + 파일 경로를 리스트로 준비
    rules_meta = [
        {
            "meta": {
                "title": "강원대학교 학칙",
                "category": "학칙",
                "url": "https://wwwk.kangwon.ac.kr/www/selectRegltnIemList.do?key=2289&regltnNo=328",
                "department": "총무과",
                "revision": "개정",
                "number": "제 2061호",
                "date": "2025-09-01",
                "attachment": [
                    {
                        "filename": "강원대학교 학칙.hwp",
                        "url": "https://wwwk.kangwon.ac.kr/cmm/downloadCmmAtchmnfl.do?fileNo=29899",
                        "ext": "hwp"
                    }
                ]
            },
            "md_file": "강원대학교 학칙_utf8.md",
            "chunks_file": "강원대학교 학칙_chunks_embedded.json"
        },
        {
            "meta": {
                "title": "강원대학교 교수 업적평가 규정",
                "category": "교무행정",
                "url": "",
                "department": "윤채원",
                "revision": "",
                "number": "",
                "date": "2017-04-20",
                "attachment": [
      {
        "filename": "강원대학교 교수 업적평가 규정.hwp",
        "url": "https://wwwk.kangwon.ac.kr/cmm/downloadCmmAtchmnfl.do?fileNo=12930&fileId=917b20024c68ac9339f41d2ac5ad812e82c971499879ad23d80d0567340fef53eb422ddfc2216c95be6ae738e891634962149f104e7e6b19b86b501fbad140688fa4ee472db8ace9",
        "ext": "hwp",
        "collected_date": "2025-09-23"
      }
    ]
            },
            "md_file": "강원대학교 교수 업적평가규정_utf8.md",
            "chunks_file": "강원대학교 교수 업적평가규정_chunks_embedded.json"
        },
        {
            "meta": {
                "title": "전임교원 업적평가 시행지침",
                "category": "교무행정",
                "url": "",
                "department": "교무과",
                "revision": "개정",
                "number": "",
                "date": "2025-03-01",
                "attachment": [
      {
        "filename": "강원대학교 전임교원 업적평가 시행지침.hwp",
        "url": "https://wwwk.kangwon.ac.kr/cmm/downloadCmmAtchmnfl.do?fileNo=28322&fileId=917b20024c68ac9339f41d2ac5ad812e82c971499879ad23d80d0567340fef53eb7c96747c3c634b0f8a18b1f3f69a93b8e930461ded213741cc07ac3dc9e2620e714684e6d80b3e",
        "ext": "hwp",
        "collected_date": "2025-09-23"
      }
    ]
            },
            "md_file": "강원대학교 전임교원 업적평가 시행지침_utf8.md",
            "chunks_file": "강원대학교 전임교원 업적평가 시행지침_chunks_embedded.json"
        },
        {
            "meta": {
                "title": "전임교원 국외파견 및 연구년에 관한 규정",
                "category": "교무행정",
                "url": "",
                "department": "교무과",
                "revision": "",
                "number": "",
                "date": "2020-07-10",
                "attachment": [
      {
        "filename": "강원대학교 전임교원 국외파견 및 연구년 운영 지침.hwp",
        "url": "https://wwwk.kangwon.ac.kr/cmm/downloadCmmAtchmnfl.do?fileNo=13127&fileId=917b20024c68ac9339f41d2ac5ad812e82c971499879ad23d80d0567340fef53eb4229299734fc2abeae3dd2fb05e03c746243477d796abf91950cc0ac4e13c921b89e6c936e1546",
        "ext": "hwp",
        "collected_date": "2025-09-23"
      }
    ],
            },
            "md_file": "강원대학교 전임교원 국외파견 및 연구년 운영 지침_utf8.md",
            "chunks_file": "강원대학교 전임교원 국외파견 및 연구년 운영 지침_chunks_embedded.json"
        },
        {
            "meta": {
                "title": "전임교원 공무국외출장 / 국내여비 등에 관한 규정",
                "category": "교무행정",
                "url": "",
                "department": "총무과",
                "revision": "개정",
                "number": "제 1979호",
                "date": "2023-12-12",
                "attachment": [
      {
        "filename": "강원대학교 교육공무원 공무국외출장 등에 관한 규정.hwp",
        "url": "https://wwwk.kangwon.ac.kr/cmm/downloadCmmAtchmnfl.do?fileNo=23564&fileId=917b20024c68ac9339f41d2ac5ad812e82c971499879ad23d80d0567340fef53eb7cbc030e2e74190b7d8ef341ca6a182fc5b0efdf62febf86f192ebb9f820bacefde98dc65428ab",
        "ext": "hwp",
        "collected_date": "2025-09-23"
      }
    ]
            },
            "md_file": "강원대학교 교육공무원 공무국외출장 등에 관한 규정_utf8.md",
            "chunks_file": "강원대학교 교육공무원 공무국외출장 등에 관한 규정_chunks_embedded.json"
        },
        {
            "meta": {
                "title": "강원대학교 교수회 규정",
                "category": "교무행정",
                "url": "",
                "department": "총무과",
                "revision": "",
                "number": "제 1747호",
                "date": "2019-11-27",
                "attachment": [
      {
        "filename": "강원대학교 교수회 규정.hwp",
        "url": "https://wwwk.kangwon.ac.kr/cmm/downloadCmmAtchmnfl.do?fileNo=13057&fileId=917b20024c68ac9339f41d2ac5ad812e82c971499879ad23d80d0567340fef53eb42292680903949a80466b949450f850690ba2fbc688a73eced05ca2316721bb782282e0125a09f",
        "ext": "hwp",
        "collected_date": "2025-09-23"
      }
    ]
            },
            "md_file": "강원대학교 교수회 규정_utf8.md",
            "chunks_file": "강원대학교 교수회 규정_chunks_embedded.json"
        },
        {
            "meta": {
                "title": "전임교원 성과급적 연봉제 운영지침",
                "category": "교무행정",
                "url": "",
                "department": "교무과",
                "revision": "개정",
                "number": "제 6457호",
                "date": "2025-04-07",
                "attachment": [
      {
        "filename": "강원대학교 전임교원 성과급적 연봉제 운영 지침.hwp",
        "url": "https://wwwk.kangwon.ac.kr/cmm/downloadCmmAtchmnfl.do?fileNo=28540&fileId=917b20024c68ac9339f41d2ac5ad812e82c971499879ad23d80d0567340fef53eb7c963f0508643c1f720430744f5d1326c4b7bfb059d50befcab471d51a86fe45bfd9d352d15723",
        "ext": "hwp",
        "collected_date": "2025-09-23"
      }
    ]
            },
            "md_file": "강원대학교 전임교원 성과급적 연봉제 운영 지침_utf8.md",
            "chunks_file": "강원대학교 전임교원 성과급적 연봉제 운영 지침_chunks_embedded.json"
        },
        {
            "meta": {
                "title": "강원대학교 연구비 관리 규정",
                "category": "교무행정",
                "url": "",
                "department": "총무과",
                "revision": "",
                "number": "제 1856호",
                "date": "2021-08-04",
                "attachment": [
      {
        "filename": "강원대학교 연구비 관리 규정.hwp",
        "url": "https://wwwk.kangwon.ac.kr/cmm/downloadCmmAtchmnfl.do?fileNo=13265&fileId=917b20024c68ac9339f41d2ac5ad812e82c971499879ad23d80d0567340fef53eb4229283023bb36f2fe7519da3a3ca23da763b43d97f90bd0dfecc22f8b42508468a0994c023594",
        "ext": "hwp",
        "collected_date": "2025-09-23"
      }
    ]
            },
            "md_file": "강원대학교 연구비 관리 규정_utf8.md",
            "chunks_file": "강원대학교 연구비 관리 규정_chunks_embedded.json"
        },
        {
            "meta": {
                "title": "강원대학교 학사운영 규정",
                "category": "학사운영규정",
                "url": "",
                "department": "총무과",
                "revision": "개정",
                "number": "제 2050호",
                "date": "2025-08-01",
                "attachment": [
      {
        "filename": "강원대학교 학사운영 규정.hwp",
        "url": "https://wwwk.kangwon.ac.kr/cmm/downloadCmmAtchmnfl.do?fileNo=29858&fileId=917b20024c68ac9339f41d2ac5ad812e82c971499879ad23d80d0567340fef53eb7c9a5a9ec255ec4b3b04e13752978766eab2261f29cdaeca2727f4d3a58b0af8ce76953c721a0e",
        "ext": "hwp",
        "collected_date": "2025-09-23"
      }
    ]
            },
            "md_file": "강원대학교 학사운영 규정_utf8.md",
            "chunks_file": "강원대학교 학사운영 규정_chunks_embedded.json"
        },
        {
            "meta": {
                "title": "강원대학교 대학원 학사운영 규정",
                "category": "학사운영",
                "url": "",
                "department": "총무과",
                "revision": "개정",
                "number": "제 2029호",
                "date": "2025-03-01",
                "attachment": [
      {
        "filename": "강원대학교 대학원 학사운영규정.hwp",
        "url": "https://wwwk.kangwon.ac.kr/cmm/downloadCmmAtchmnfl.do?fileNo=28332&fileId=917b20024c68ac9339f41d2ac5ad812e82c971499879ad23d80d0567340fef53eb7c96747c2c8d7373d5735d2823074c2c49a2ebf2c14f9649b8e5667ac77736d5d0ae2a9bf8bc86",
        "ext": "hwp",
        "collected_date": "2025-09-23"
      }
    ]
            },
            "md_file": "강원대학교 대학원 학사운영규정_utf8.md",
            "chunks_file": "강원대학교 대학원 학사운영규정_chunks_embedded.json"
        }
    ]

    # 전체 결과 담을 리스트
    all_rules = []

    for rule in rules_meta:
        result = build_rule_json(rule["meta"], rule["md_file"], rule["chunks_file"])
        all_rules.append(result)

    # JSON 배열로 저장
    with open("rules_final.json", "w", encoding="utf-8") as f:
        json.dump(all_rules, f, ensure_ascii=False, indent=2)

    print("[완료] 전체 JSON 생성됨: rules_final.json")
