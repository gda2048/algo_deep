import json
import sys
import io
import time
from wrapt_timeout_decorator import *
from contextlib import redirect_stdout



class Checker:
    def __init__(self, questions, answers, user_answers):
        self.questions = questions['questions']
        self.answers = answers["answers"]
        self.user_answers = user_answers["answers"]


    @property
    def res(self):
        rs = []
        for el in range(len(self.questions)):
            rs += [sum(self.check(el))]
        return rs

    def print(self):
        for el in range(len(self.questions)):
            print("type: ", self.questions[el]["type"])
            print("task: ", self.questions[el]["task"])
            print("possible answers: ", self.questions[el]["answer"])
            print("user answer:\n", self.user_answers[el]['answer'], sep="")
            print("right answer:", self.answers[el]['answer'])
            print("This answer is counted as", self.check(el))
            print()

    def check(self, el):
        if self.questions[el]["type"] == "checkbox":
            return self.checkbox(el)
        elif self.questions[el]["type"] == "radio":
            return self.radio(el)
        elif self.questions[el]["type"] == "text":
            return self.text(el)
        elif self.questions[el]["type"] == "code":
            return self.code(el)

    def checkbox(self, el):
        return [int(self.answers[el]["score"]) if sorted(self.answers[el]["answer"]) == sorted(self.user_answers[el]["answer"]) else 0]

    def radio(self, el):
        return [int(self.answers[el]["score"]) if self.answers[el]["answer"] == self.user_answers[el]["answer"] else 0]

    def text(self, el):
        return [int(self.answers[el]["score"]) if self.user_answers[el]["answer"][0].lower().strip(' ') in self.answers[el]["answer"] else 0]


    @timeout(2)
    def code(self, el):
        test_list = []
        try:
            for item in range(len(self.answers[el]["answer"])):
                sys.stdin = io.StringIO(self.answers[el]["answer"][item]["input"])
                f = io.StringIO()
                with redirect_stdout(f):
                    exec(self.user_answers[el]["answer"][0])
                test_list.append(int(self.answers[el]["score"]) if f.getvalue().strip() == self.answers[el]["answer"][item]["output"] else 0)
                sys.stdin = sys.__stdin__
        except Exception:
            test_list = [-1]  # "TL"
        return test_list

    @staticmethod
    def get_questions(file):
        return json.load(file)

    @staticmethod
    def get_answers(file):
        return json.load(file)

    @staticmethod
    def get_user_answers(file):
        return json.load(file)
