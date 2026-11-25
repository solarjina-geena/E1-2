"""게임 전체(퀴즈 목록, 점수, 메뉴)를 관리하는 QuizGame 클래스."""

import json
import random
from pathlib import Path

from quiz import Quiz

STATE_FILE = Path(__file__).parent / "state.json"  # 어디서 실행해도 프로젝트 루트


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


class QuizGame:
    def __init__(self):
        self.quizzes = []       # Quiz 객체 리스트
        self.best_score = None  # 최고 기록의 맞힌 문제 수 (None = 아직 안 풀었음)
        self.best_total = None  # 최고 기록 때 푼 전체 문제 수
        self.reset_to_default()

    def reset_to_default(self):
        self.quizzes = make_default_quizzes()
        self.best_score = None
        self.best_total = None

    # ---------- 저장 / 불러오기 ----------

    def load(self):
        """state.json을 읽는다. 없으면 기본 퀴즈로, 손상되었으면 복구한다."""
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(q) for q in data["quizzes"]]
            self.best_score = data["best_score"]
            self.best_total = data["best_total"]
        except FileNotFoundError:                  # 첫 실행
            self.reset_to_default()
            self.save()
        except (ValueError, KeyError, TypeError):  # 손상된 파일
            print("저장 파일이 손상되어 기본 퀴즈로 복구합니다.")
            self.reset_to_default()
            self.save()
        except OSError:                            # 권한 등 읽기 오류
            print("저장 파일을 읽을 수 없어 기본 퀴즈로 시작합니다.")
            self.reset_to_default()

    def save(self):
        """퀴즈와 최고 점수를 state.json에 UTF-8로 저장한다."""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
            "best_total": self.best_total,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except OSError:
            print("저장에 실패했습니다.")

    # ---------- 입력 ----------

    def get_number(self, prompt, low, high):
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

    def get_text(self, prompt):
        """비어 있지 않은 문자열을 받을 때까지 다시 묻는다."""
        while True:
            text = input(prompt).strip()
            if text == "":
                print("입력이 비어 있습니다. 내용을 입력하세요.")
                continue
            return text

    # ---------- 메뉴 ----------

    def show_menu(self):
        print()
        print("========================================")
        print("      🐯 무궁이·태범이 퀴즈 게임 🐯")
        print("========================================")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 퀴즈 삭제")
        print("5. 점수 확인")
        print("6. 종료")
        print("========================================")

    def run(self):
        self.load()
        try:
            while True:
                self.show_menu()
                choice = self.get_number("선택: ", 1, 6)
                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.delete_quiz()
                elif choice == 5:
                    self.show_score()
                else:
                    break
        except (KeyboardInterrupt, EOFError):  # Ctrl+C 또는 입력 끝(Ctrl+Z/Ctrl+D)
            print("\n입력이 중단되어 저장 후 종료합니다.")
        self.save()
        print("게임을 종료합니다.")

    # ---------- 기능 ----------

    def play(self):
        """퀴즈를 무작위 순서로 출제하고 결과에 따라 최고 점수를 갱신한다."""
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        count = self.get_number(f"몇 문제를 풀까요? (1-{len(self.quizzes)}): ", 1, len(self.quizzes))
        # random.sample은 섞인 '복사본'을 만들므로 self.quizzes(목록 순서)는 그대로 남는다.
        selected = random.sample(self.quizzes, count)
        print(f"\n퀴즈를 시작합니다! (총 {len(selected)}문제, 무작위 순서)")
        correct = 0
        for number, quiz in enumerate(selected, start=1):
            quiz.display(number)
            choice = self.get_number("정답 번호: ", 1, 4)
            if quiz.is_correct(choice):
                print("정답입니다! 🎉")
                correct += 1
            else:
                print(f"아쉬워요. 정답은 {quiz.answer}번 '{quiz.choices[quiz.answer - 1]}'입니다.")

        total = len(selected)
        print("\n========================================")
        print(f"결과: {total}문제 중 {correct}문제 정답!")
        print("========================================")
        self.update_best_score(correct, total)

    def update_best_score(self, correct, total):
        """맞힌 문제 수가 더 많을 때만 최고 점수를 바꾼다."""
        if self.best_score is None or correct > self.best_score:
            self.best_score = correct
            self.best_total = total
            self.save()
            print("🎊 최고 점수를 갱신했습니다!")

    def add_quiz(self):
        """문제, 선택지 4개, 정답 번호를 입력받아 퀴즈를 추가한다."""
        print("\n새 퀴즈를 추가합니다.")
        question = self.get_text("문제: ")
        choices = [self.get_text(f"선택지 {i}: ") for i in range(1, 5)]
        answer = self.get_number("정답 번호 (1-4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        self.save()
        print(f"퀴즈가 추가되었습니다. (현재 {len(self.quizzes)}문제)")

    def list_quizzes(self):
        """등록된 퀴즈를 번호와 함께 보여 준다."""
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return
        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}문제)")
        print("----------------------------------------")
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"{number}. {quiz.question}")

    def delete_quiz(self):
        """목록을 보여 주고 고른 번호의 퀴즈를 삭제한다. 0을 고르면 취소."""
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return
        self.list_quizzes()
        number = self.get_number(f"삭제할 번호 (1-{len(self.quizzes)}, 0: 취소): ", 0, len(self.quizzes))
        if number == 0:
            print("삭제를 취소했습니다.")
            return
        removed = self.quizzes.pop(number - 1)
        self.save()
        print(f"'{removed.question}' 퀴즈를 삭제했습니다. (현재 {len(self.quizzes)}문제)")

    def show_score(self):
        """최고 점수를 보여 준다. 한 번도 풀지 않았으면 안내만 한다."""
        if self.best_score is None:
            print("아직 푼 기록이 없습니다. 먼저 퀴즈를 풀어 보세요.")
            return
        print(f"\n🏆 최고 점수: {self.best_total}문제 중 {self.best_score}문제 정답")
