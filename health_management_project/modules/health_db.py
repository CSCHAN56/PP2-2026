
import json
import csv
import pickle


# =================================
# 1. 건강정보 클래스
# =================================

class HealthRecord:

    def __init__(self, name, height, weight):
        self.name = name
        self.height = height
        self.weight = weight

    # BMI 계산
    def calculate_bmi(self):
        return round(self.weight / (self.height ** 2), 2)

    # 건강 상태 판정
    def get_status(self):
        bmi = self.calculate_bmi()

        if bmi < 18.5:
            return "저체중"
        elif bmi < 25:
            return "정상"
        elif bmi < 30:
            return "과체중"
        else:
            return "비만"

    # 딕셔너리 변환
    def to_dict(self):
        return {
            "name": self.name,
            "height": self.height,
            "weight": self.weight,
            "bmi": self.calculate_bmi(),
            "status": self.get_status()
        }

    # 건강정보 출력
    def display(self):
        print(
            f"이름: {self.name}, "
            f"키: {self.height}m, "
            f"몸무게: {self.weight}kg, "
            f"BMI: {self.calculate_bmi()}, "
            f"상태: {self.get_status()}"
        )


# =================================
# 2. 건강정보 관리자 클래스
# =================================

class HealthRecordManager:

    def __init__(self):
        self.records = []

    # 건강정보 추가
    def add_record(self, record):
        self.records.append(record)

    # 전체 건강정보 출력
    def display_all(self):
        for record in self.records:
            record.display()

    # 딕셔너리 목록으로 변환
    def to_list(self):
        return [record.to_dict() for record in self.records]

    # 딕셔너리 목록을 객체로 변환
    @classmethod
    def from_list(cls, data):
        manager = cls()

        for item in data:
            record = HealthRecord(
                item["name"],
                item["height"],
                item["weight"]
            )
            manager.add_record(record)

        return manager


# =================================
# 3. JSON 저장 및 읽기
# =================================

def save_json(manager, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            manager.to_list(),
            f,
            ensure_ascii=False,
            indent=4
        )


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return HealthRecordManager.from_list(data)


# =================================
# 4. CSV 저장 및 읽기
# =================================

def save_csv(manager, path):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        fields = ["name", "height", "weight", "bmi", "status"]

        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(manager.to_list())


def load_csv(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data = []

        for row in reader:
            data.append({
                "name": row["name"],
                "height": float(row["height"]),
                "weight": float(row["weight"]),
                "bmi": float(row["bmi"]),
                "status": row["status"]
            })

    return HealthRecordManager.from_list(data)


# =================================
# 5. TXT 저장 및 읽기
# =================================

def save_txt(manager, path):
    with open(path, "w", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["name", "height", "weight", "bmi", "status"],
            delimiter="\t"
        )

        writer.writeheader()
        writer.writerows(manager.to_list())


def load_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        data = []

        for row in reader:
            data.append({
                "name": row["name"],
                "height": float(row["height"]),
                "weight": float(row["weight"]),
                "bmi": float(row["bmi"]),
                "status": row["status"]
            })

    return HealthRecordManager.from_list(data)


# =================================
# 6. PICKLE 저장 및 읽기
# =================================

def save_pickle(manager, path):
    with open(path, "wb") as f:
        pickle.dump(manager, f)


def load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)
