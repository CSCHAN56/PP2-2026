def say_happy_birthday(name:str) -> None:
    print("안녕하세요")
    print(name + "님의 생일을 축하합니다")
    return None

def test_happy_birthday():
    say_happy_birthday("찬승")
    say_happy_birthday("강민")
    say_happy_birthday("승균")
    say_happy_birthday("권우")

def test_happy_birthday2():
    names = ["찬승", "강민", "승균", "권우"]
    for name in names:
        say_happy_birthday(name)

def test_happy_birthday3():
    #say_happy_birthday(3.14)
    #say_happy_birthday(100)
    say_happy_birthday([1,2,3])
 
if __name__ == "__main__":
    #test_happy_birthday2()
    test_happy_birthday3()