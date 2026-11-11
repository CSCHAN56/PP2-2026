
from pathlib import Path

# 다른 파일에 작성한 코드 가져오기
from modules.health_db import (
    HealthRecord,
    HealthRecordManager,
    save_json,
    load_json,
    save_csv,
    load_csv,
    save_txt,
    load_txt,
    save_pickle,
    load_pickle
)


def main():

    # 데이터 저장 폴더 경로
    data_dir = Path(__file__).resolve().parent / "data"
    data_dir.mkdir(exist_ok=True)

    # 파일 경로 설정
    json_path = data_dir / "health_data.json"
    csv_path = data_dir / "health_data.csv"
    txt_path = data_dir / "health_data.txt"
    pickle_path = data_dir / "health_data.pkl"

    # =================================
    # 1. 건강정보 데이터 생성
    # =================================

    manager = HealthRecordManager()

    manager.add_record(HealthRecord("홍길동", 1.75, 70))
    manager.add_record(HealthRecord("김철수", 1.65, 55))
    manager.add_record(HealthRecord("이영희", 1.60, 75))
    manager.add_record(HealthRecord("박민수", 1.80, 90))
    manager.add_record(HealthRecord("최유진", 1.70, 48))

    print("===== 원본 건강정보 =====")
    manager.display_all()

    # =================================
    # 2. 네 가지 파일로 저장
    # =================================

    print("\n===== 파일 저장 =====")

    save_json(manager, json_path)
    print("JSON 저장 완료")

    save_csv(manager, csv_path)
    print("CSV 저장 완료")

    save_txt(manager, txt_path)
    print("TXT 저장 완료")

    save_pickle(manager, pickle_path)
    print("PICKLE 저장 완료")

    # =================================
    # 3. 저장된 파일 다시 읽기
    # =================================

    print("\n===== 파일 읽기 =====")

    json_manager = load_json(json_path)
    csv_manager = load_csv(csv_path)
    txt_manager = load_txt(txt_path)
    pickle_manager = load_pickle(pickle_path)

    # =================================
    # 4. 원본과 데이터 비교
    # =================================

    original = manager.to_list()

    loaded_data = {
        "JSON": json_manager.to_list(),
        "CSV": csv_manager.to_list(),
        "TXT": txt_manager.to_list(),
        "PICKLE": pickle_manager.to_list()
    }

    print("\n===== 데이터 일치 여부 확인 =====")

    for file_type, data in loaded_data.items():

        if original == data:
            print(f"{file_type}: 원본 데이터와 일치합니다.")
        else:
            print(f"{file_type}: 원본 데이터와 일치하지 않습니다.")

    # =================================
    # 5. 읽어온 데이터 출력
    # =================================

    print("\n===== JSON 데이터 출력 =====")
    json_manager.display_all()

    print("\n===== CSV 데이터 출력 =====")
    csv_manager.display_all()

    print("\n===== TXT 데이터 출력 =====")
    txt_manager.display_all()

    print("\n===== PICKLE 데이터 출력 =====")
    pickle_manager.display_all()


# 프로그램 실행
if __name__ == "__main__":
    main()
