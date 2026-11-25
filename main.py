"""무궁이·태범이 퀴즈 게임 - 프로그램 시작점."""


def get_number(prompt, low, high):
    """low~high 사이의 정수를 받을 때까지 다시 묻는다."""
    while True:
        text = input(prompt).strip()
        if text == "":
            print(f"입력이 비어 있습니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        try:
            number = int(text)
        except ValueError:
            print(f"잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        if number < low or number > high:
            print(f"잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        return number


def show_menu():
    print()
    print("========================================")
    print("      🐯 무궁이·태범이 퀴즈 게임 🐯")
    print("========================================")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("========================================")


def main():
    while True:
        show_menu()
        choice = get_number("선택: ", 1, 5)
        if choice == 1:
            print("퀴즈 풀기는 준비 중입니다.")
        elif choice == 2:
            print("퀴즈 추가는 준비 중입니다.")
        elif choice == 3:
            print("퀴즈 목록은 준비 중입니다.")
        elif choice == 4:
            print("점수 확인은 준비 중입니다.")
        else:
            break
    print("게임을 종료합니다.")


if __name__ == "__main__":
    main()
