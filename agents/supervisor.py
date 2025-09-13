from .interviewer import InterviewerAgent
from .evaluator import EvaluatorAgent
from .feedback import FeedbackAgent


class Supervisor:
    def __init__(self, question_bank):
        self.interviewer = InterviewerAgent(question_bank)
        self.evaluator = EvaluatorAgent()
        self.feedback = FeedbackAgent()
        

    def run_interview(self, answers):
        evaluations = []
        for qa in answers:
            ev = self.evaluator.evaluate(qa["question"], qa["answer"])
            evaluations.append(ev)
        summary = self.feedback.summarize(evaluations)
        return evaluations, summary
