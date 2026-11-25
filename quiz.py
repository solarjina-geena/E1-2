"""퀴즈 문제 하나를 나타내는 Quiz 클래스."""


class Quiz:
    def __init__(self, question, choices, answer, hint=""):
        self.question = question  # 문제 문장 (str)
        self.choices = choices    # 선택지 4개 (list[str])
        self.answer = answer      # 정답 번호 1~4 (int)
        self.hint = hint          # 힌트 문장 (str, 없으면 "")

    def display(self, number=None):
        """문제와 선택지를 출력한다. number가 있으면 문제 앞에 번호를 붙인다."""
        title = f"[문제 {number}] " if number is not None else ""
        print(f"\n{title}{self.question}")
        for index, choice in enumerate(self.choices, start=1):
            print(f"  {index}. {choice}")

    def has_hint(self):
        return self.hint != ""

    def is_correct(self, number):
        return number == self.answer

    def to_dict(self):
        """JSON 저장용 dict로 바꾼다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data):
        """저장된 dict에서 Quiz 객체를 다시 만든다. 형태가 틀리면 ValueError."""
        question = data["question"]
        choices = data["choices"]
        answer = data["answer"]
        # hint는 보너스로 나중에 생긴 키라, 예전 파일에 없으면 빈 힌트로 둔다.
        hint = data.get("hint", "")
        if not isinstance(question, str) or not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("퀴즈 형식이 올바르지 않습니다.")
        if not isinstance(answer, int) or not 1 <= answer <= 4:
            raise ValueError("정답 번호가 올바르지 않습니다.")
        if not isinstance(hint, str):
            raise ValueError("힌트 형식이 올바르지 않습니다.")
        return cls(question, choices, answer, hint)
