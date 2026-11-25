"""퀴즈 문제 하나를 나타내는 Quiz 클래스."""


class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question  # 문제 문장 (str)
        self.choices = choices    # 선택지 4개 (list[str])
        self.answer = answer      # 정답 번호 1~4 (int)

    def display(self, number=None):
        """문제와 선택지를 출력한다. number가 있으면 문제 앞에 번호를 붙인다."""
        title = f"[문제 {number}] " if number is not None else ""
        print(f"\n{title}{self.question}")
        for index, choice in enumerate(self.choices, start=1):
            print(f"  {index}. {choice}")

    def is_correct(self, number):
        return number == self.answer

    def to_dict(self):
        """JSON 저장용 dict로 바꾼다."""
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    @classmethod
    def from_dict(cls, data):
        """저장된 dict에서 Quiz 객체를 다시 만든다."""
        return cls(data["question"], data["choices"], data["answer"])
