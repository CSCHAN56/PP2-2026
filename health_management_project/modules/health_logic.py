
# modules/health_logic.py

from modules.health_db import HealthDB


class HealthManager:

    def __init__(self):
        self.db = HealthDB()

    # 신규 건강정보 등록
    def register(self, name, age, gender, height, weight):

        name = str(name).strip()
        age = int(age)
        height = float(height)
        weight = float(weight)

        if not name:
            raise ValueError("이름을 입력하세요.")

        if age <= 0:
            raise ValueError("나이는 1 이상이어야 합니다.")

        if height <= 0 or weight <= 0:
            raise ValueError("키와 몸무게는 0보다 커야 합니다.")

        # 동일한 건강정보 중복 등록 검사
        for record in self.db.get_all_records():

            if (
                record.name == name
                and record.age == age
                and record.gender == gender
                and record.height == height
                and record.weight == weight
            ):
                raise ValueError("이미 등록된 건강정보입니다.")

        return self.db.add_record(
            name, age, gender, height, weight
        )

    # 전체 건강정보 조회
    def get_all(self):

        return self.db.get_all_records()

    # ID 또는 이름 검색
    def search(self, keyword=""):

        if not keyword:
            return self.get_all()

        return self.db.search_record(keyword)

    # 건강정보 수정
    def update(
        self, record_id, name, age, gender, height, weight
    ):

        name = str(name).strip()
        age = int(age)
        height = float(height)
        weight = float(weight)

        if not name:
            raise ValueError("이름을 입력하세요.")

        if age <= 0:
            raise ValueError("나이는 1 이상이어야 합니다.")

        if height <= 0 or weight <= 0:
            raise ValueError("키와 몸무게는 0보다 커야 합니다.")

        target = self.db.find_by_id(record_id)

        if target is None:
            raise ValueError("수정할 데이터를 찾을 수 없습니다.")

        # 다른 ID에 동일한 건강정보가 있는지 검사
        for record in self.db.get_all_records():

            if record.id == record_id:
                continue

            if (
                record.name == name
                and record.age == age
                and record.gender == gender
                and record.height == height
                and record.weight == weight
            ):
                raise ValueError("동일한 건강정보가 이미 존재합니다.")

        return self.db.update_record(
            record_id,
            name,
            age,
            gender,
            height,
            weight
        )

    # 건강정보 삭제
    def delete(self, record_id):

        if not self.db.delete_record(record_id):
            raise ValueError("삭제할 데이터를 찾을 수 없습니다.")

        return True

    # 통계 계산
    def statistics(self):

        return self.db.get_statistics()

    # 파일 저장
    def save_file(self, filename):

        return self.db.save_file(filename)

    # 파일 불러오기
    def load_file(self, filename):

        return self.db.load_file(filename)

    # 엑셀 데이터 가져오기
    def import_excel(self, filename):

        try:
            from openpyxl import load_workbook

        except ImportError:
            raise ImportError(
                "엑셀 기능을 사용하려면 "
                "pip install openpyxl을 실행하세요."
            )

        workbook = load_workbook(
            filename,
            read_only=True,
            data_only=True
        )

        try:
            sheet = workbook.active

            rows = sheet.iter_rows(values_only=True)
            header = next(rows, None)

            if not header:
                return 0

            columns = {
                str(value).strip().lower(): index
                for index, value in enumerate(header)
                if value is not None
            }

            required = [
                "name",
                "age",
                "gender",
                "height",
                "weight"
            ]

            if not all(key in columns for key in required):
                raise ValueError(
                    "엑셀 첫 번째 행에 다음 항목이 필요합니다: "
                    "name, age, gender, height, weight"
                )

            count = 0

            for row_number, row in enumerate(rows, start=2):

                if not row:
                    continue

                values = []

                for key in required:
                    index = columns[key]

                    value = row[index] if index < len(row) else None

                    values.append(value)

                if not values[0]:
                    continue

                try:
                    self.register(*values)
                    count += 1

                except (ValueError, TypeError):
                    # 잘못된 데이터 및 중복 데이터 건너뛰기
                    continue

            return count

        finally:
            workbook.close()
