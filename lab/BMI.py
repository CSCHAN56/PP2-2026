def BMI(kg: float, cm: float) -> float:
    bmi = kg / (cm / 100) ** 2
    return bmi

def test_get_bmi():
    kg = 78
    cm = 173
    b = BMI(kg,cm)
    print(f"키({cm}), 몸무게({kg})인 사람의 BMI는 {b}입니다.")

test_get_bmi()