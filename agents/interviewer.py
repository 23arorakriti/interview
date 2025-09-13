import random
from .base import BaseAgent


class InterviewerAgent(BaseAgent):
    def __init__(self, question_bank):
        super().__init__()
        self.question_bank = question_bank

    def get_questions(self, n_basic=1, n_inter=1, n_adv=1):
        picked = []
        picked += random.sample(
            self.question_bank["basic"], min(n_basic, len(self.question_bank["basic"]))
        )
        picked += random.sample(
            self.question_bank["intermediate"],
            min(n_inter, len(self.question_bank["intermediate"])),
        )
        picked += random.sample(
            self.question_bank["advanced"],
            min(n_adv, len(self.question_bank["advanced"])),
        )
        random.shuffle(picked)
        return picked
