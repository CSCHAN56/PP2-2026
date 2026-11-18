
# main.py

from modules.health_logic import HealthManager


def print_records(records):

    if not records:
        print("\n등록된 건강정보가 없습니다.")
        return

    print("\n" + "=" * 100)
    print(
        f"{'ID':<12}{'이름':<12}{'나이':<8}"
        f"{'성별':<8}{'키':<12}{'몸무게':<12}"
        f"{'BMI':<10}{'비만도':<12}"
    )
    print("=" * 100)

    for r in records:

        print(
            f"{r.id:<12}{r.name:<12}{r.age:<8}"
            f"{r.gender:<8}{r.height:<12}"
            f"{r.weight:<12}{r.bmi:<10}{r.obesity:<12}"
        )

    print("=" * 100)


def main():

    manager = HealthManager()

    while True:

        print("\n========== 건강정보 관리 프로그램 ==========")
        print("1. 건강정보 등록")
        print("2. 전체 건강정보 조회")
        print("3. 건강정보 검색")
        print("4. 건강정보 수정")
        print("5. 건강정보 삭제")
        print("6. 건강정보 통계")
        print("7. 파일 저장")
        print("8. 파일 불러오기")
        print("9. 엑셀 파일 가져오기")
        print("0. 프로그램 종료")
        print("============================================")

        choice = input("메뉴 선택: ").strip()

        try:

            # 1. 신규 등록
            if choice == "1":

                print("\n[건강정보 등록]")

                name = input("이름: ")
                age = input("나이: ")
                gender = input("성별(남성/여성): ")
                height = input("키(cm): ")
                weight = input("몸무게(kg): ")

                record = manager.register(
                    name, age, gender, height, weight
                )

                print("\n등록이 완료되었습니다.")
                print("발급 ID:", record.id)
                print("BMI:", record.bmi)
                print("비만도:", record.obesity)

            # 2. 전체 조회
            elif choice == "2":

                print("\n[전체 건강정보 조회]")
                print_records(manager.get_all())

            # 3. 검색
            elif choice == "3":

                keyword = input(
                    "\n검색할 이름 또는 ID: "
                )

                results = manager.search(keyword)

                print_records(results)

            # 4. 수정
            elif choice == "4":

                print("\n[건강정보 수정]")

                record_id = input("수정할 ID: ")

                record = manager.db.find_by_id(record_id)

                if record is None:
                    print("해당 ID의 데이터가 없습니다.")
                    continue

                print("현재 정보:")
                print_records([record])

                name = input("새 이름: ")
                age = input("새 나이: ")
                gender = input("새 성별: ")
                height = input("새 키(cm): ")
                weight = input("새 몸무게(kg): ")

                manager.update(
                    record_id,
                    name,
                    age,
                    gender,
                    height,
                    weight
                )

                print("건강정보 수정 완료!")
                print("BMI와 비만도가 자동으로 재계산되었습니다.")

            # 5. 삭제
            elif choice == "5":

                print("\n[건강정보 삭제]")

                record_id = input("삭제할 ID: ")

                confirm = input(
                    "정말 삭제하시겠습니까? (y/n): "
                )

                if confirm.lower() == "y":

                    manager.delete(record_id)

                    print("삭제가 완료되었습니다.")

                else:
                    print("삭제를 취소했습니다.")

            # 6. 통계
            elif choice == "6":

                print("\n[건강정보 통계]")

                stats = manager.statistics()

                if stats is None:
                    print("등록된 데이터가 없습니다.")

                else:
                    print("전체 인원:", stats["count"], "명")
                    print("평균 키:", stats["avg_height"], "cm")
                    print("평균 몸무게:", stats["avg_weight"], "kg")
                    print("평균 BMI:", stats["avg_bmi"])

            # 7. 파일 저장
            elif choice == "7":

                print("\n[파일 저장]")
                print("지원 형식: json, csv, txt, pkl")

                filename = input(
                    "저장 경로 (예: data/health_data.json): "
                )

                manager.save_file(filename)

                print("파일 저장 완료!")

            # 8. 파일 불러오기
            elif choice == "8":

                print("\n[파일 불러오기]")

                filename = input(
                    "불러올 파일 경로: "
                )

                count = manager.load_file(filename)

                print(f"{count}건의 데이터가 추가되었습니다.")

            # 9. 엑셀 가져오기
            elif choice == "9":

                print("\n[엑셀 파일 가져오기]")

                filename = input(
                    "엑셀 파일 경로 (.xlsx): "
                )

                count = manager.import_excel(filename)

                print(f"{count}건의 데이터를 가져왔습니다.")

            # 0. 종료
            elif choice == "0":

                print("프로그램을 종료합니다.")
                break

            else:

                print("올바른 메뉴 번호를 입력하세요.")

        except (ValueError, TypeError, OSError, ImportError) as e:

            print("\n오류:", e)

        except Exception as e:

            print("\n예상하지 못한 오류:", e)


if __name__ == "__main__":
    main()
