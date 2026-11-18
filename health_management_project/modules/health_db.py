
# modules/health_db.py

import os
import json
import csv
import pickle
import uuid

from dataclasses import dataclass, asdict


# 건강정보 데이터 구조
@dataclass
class HealthRecord:
    id: str
    name: str
    age: int
    gender: str
    height: float
    weight: float
    bmi: float
    obesity: str


class HealthDB:

    def __init__(self):
        self.records = []

    # BMI 계산
    def calculate_bmi(self, height, weight):
        height = float(height)
        weight = float(weight)

        if height <= 0 or weight <= 0:
            raise ValueError("키와 몸무게는 0보다 커야 합니다.")

        bmi = weight / ((height / 100) ** 2)

        return round(bmi, 2)

    # 비만도 판정
    def get_obesity(self, bmi):

        if bmi < 18.5:
            return "저체중"
        elif bmi < 23:
            return "정상"
        elif bmi < 25:
            return "과체중"
        elif bmi < 30:
            return "비만"
        else:
            return "고도비만"

    # 건강정보 신규 등록
    def add_record(self, name, age, gender, height, weight):

        if not str(name).strip():
            raise ValueError("이름을 입력해야 합니다.")

        age = int(age)
        height = float(height)
        weight = float(weight)

        if age <= 0:
            raise ValueError("나이는 1 이상이어야 합니다.")

        bmi = self.calculate_bmi(height, weight)

        record = HealthRecord(
            id=str(uuid.uuid4())[:8],
            name=str(name).strip(),
            age=age,
            gender=str(gender),
            height=height,
            weight=weight,
            bmi=bmi,
            obesity=self.get_obesity(bmi)
        )

        self.records.append(record)

        return record

    # ID로 건강정보 조회
    def find_by_id(self, record_id):

        for record in self.records:
            if record.id == record_id:
                return record

        return None

    # ID 중복 확인
    def check_duplicate(self, record_id):

        return self.find_by_id(record_id) is not None

    # 건강정보 수정
    def update_record(
        self, record_id, name, age, gender, height, weight
    ):

        record = self.find_by_id(record_id)

        if record is None:
            return False

        age = int(age)
        height = float(height)
        weight = float(weight)

        if not str(name).strip():
            raise ValueError("이름을 입력해야 합니다.")

        if age <= 0:
            raise ValueError("나이는 1 이상이어야 합니다.")

        bmi = self.calculate_bmi(height, weight)

        record.name = str(name).strip()
        record.age = age
        record.gender = str(gender)
        record.height = height
        record.weight = weight

        # 키와 몸무게 변경 시 BMI 자동 재계산
        record.bmi = bmi
        record.obesity = self.get_obesity(bmi)

        return True

    # 건강정보 삭제
    def delete_record(self, record_id):

        record = self.find_by_id(record_id)

        if record is None:
            return False

        self.records.remove(record)

        return True

    # 전체 건강정보 조회
    def get_all_records(self):

        return self.records

    # 이름 또는 ID 검색
    def search_record(self, keyword):

        keyword = str(keyword).lower()

        return [
            record for record in self.records
            if keyword in record.name.lower()
            or keyword in record.id.lower()
        ]

    # 파일 저장
    def save_file(self, filename):

        os.makedirs(
            os.path.dirname(filename) or ".",
            exist_ok=True
        )

        extension = os.path.splitext(filename)[1].lower()

        data = [
            asdict(record)
            for record in self.records
        ]

        if extension == ".json":

            with open(filename, "w", encoding="utf-8") as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

        elif extension == ".csv":

            with open(
                filename,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                if data:
                    writer = csv.DictWriter(
                        file,
                        fieldnames=data[0].keys()
                    )

                    writer.writeheader()
                    writer.writerows(data)

        elif extension == ".txt":

            with open(filename, "w", encoding="utf-8") as file:

                for record in data:
                    file.write(
                        json.dumps(record, ensure_ascii=False) + "\n"
                    )

        elif extension == ".pkl":

            with open(filename, "wb") as file:
                pickle.dump(data, file)

        else:
            raise ValueError("지원하지 않는 파일 형식입니다.")

        return True

    # 파일 불러오기
    def load_file(self, filename):

        extension = os.path.splitext(filename)[1].lower()

        if extension == ".json":

            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

        elif extension == ".csv":

            with open(
                filename,
                "r",
                encoding="utf-8-sig"
            ) as file:

                data = list(csv.DictReader(file))

        elif extension == ".txt":

            with open(filename, "r", encoding="utf-8") as file:

                data = [
                    json.loads(line)
                    for line in file
                    if line.strip()
                ]

        elif extension == ".pkl":

            with open(filename, "rb") as file:
                data = pickle.load(file)

        else:
            raise ValueError("지원하지 않는 파일 형식입니다.")

        if not isinstance(data, list):
            raise ValueError("파일 데이터 형식이 올바르지 않습니다.")

        loaded_records = []

        for item in data:

            record_id = str(item["id"])

            if any(
                r.id == record_id for r in loaded_records
            ):
                continue

            bmi = self.calculate_bmi(
                item["height"],
                item["weight"]
            )

            record = HealthRecord(
                id=record_id,
                name=str(item["name"]),
                age=int(item["age"]),
                gender=str(item["gender"]),
                height=float(item["height"]),
                weight=float(item["weight"]),
                bmi=bmi,
                obesity=self.get_obesity(bmi)
            )

            loaded_records.append(record)

        # 기존 데이터와 ID 중복 확인
        existing_ids = {
            record.id for record in self.records
        }

        added_count = 0

        for record in loaded_records:

            if record.id not in existing_ids:
                self.records.append(record)
                existing_ids.add(record.id)
                added_count += 1

        return added_count

    # 통계 계산
    def get_statistics(self):

        if not self.records:
            return None

        count = len(self.records)

        return {
            "count": count,
            "avg_height": round(
                sum(r.height for r in self.records) / count, 2
            ),
            "avg_weight": round(
                sum(r.weight for r in self.records) / count, 2
            ),
            "avg_bmi": round(
                sum(r.bmi for r in self.records) / count, 2
            )
        }
