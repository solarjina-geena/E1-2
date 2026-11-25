"""무궁이·태범이 퀴즈 게임 - 프로그램 시작점."""

from quiz import Quiz


def make_default_quizzes():
    """처음 실행하거나 저장 파일이 손상되었을 때 쓰는 기본 퀴즈 6문제."""
    places = ["에버랜드", "서울대공원", "국립백두대간수목원", "대전 오월드"]
    return [
        Quiz("무궁이와 태범이의 관계는?", ["부부", "남매", "모자", "사촌"], 2),
        Quiz("무궁이와 태범이의 부모 이름은?", ["태호와 건곤", "한과 도", "한청과 우리", "아름과 다운"], 1),
        Quiz("무궁이와 태범이가 지금 사는 곳은?", list(places), 3),
        Quiz("무궁이와 태범이가 태어난 곳은?", list(places), 1),
        Quiz("2026년 현재 무궁이와 태범이의 동생은 몇 마리인가?", ["2마리", "3마리", "4마리", "5마리"], 3),
        Quiz("무궁이와 태범이 중 누가 첫째인가?", ["무궁", "태범", "동시에 태어났다", "알려지지 않았다"], 2),
    ]


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


def play(quizzes):
    """모든 퀴즈를 차례로 출제하고 맞힌 문제 수를 돌려준다."""
    if not quizzes:
        print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
        return None

    print(f"\n퀴즈를 시작합니다! (총 {len(quizzes)}문제)")
    correct = 0
    for number, quiz in enumerate(quizzes, start=1):
        quiz.display(number)
        choice = get_number("정답 번호: ", 1, 4)
        if quiz.is_correct(choice):
            print("정답입니다! 🎉")
            correct += 1
        else:
            print(f"아쉬워요. 정답은 {quiz.answer}번 '{quiz.choices[quiz.answer - 1]}'입니다.")

    print("\n========================================")
    print(f"결과: {len(quizzes)}문제 중 {correct}문제 정답!")
    print("========================================")
    return correct


def main():
    quizzes = make_default_quizzes()
    while True:
        show_menu()
        choice = get_number("선택: ", 1, 5)
        if choice == 1:
            play(quizzes)
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
