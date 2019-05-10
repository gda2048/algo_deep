import random


class Elem:
    def __init__(self, data, question, test, answer):
        self.data = data
        self.question = question
        self.test = test
        self.answer = answer

    def check(self, ans):
        return ans == self.answer

    def create_task(self):
        pass


class Sort_el:
    def __init__(self):
        self.list = []
        self.list2 = []
        self.n = random.randint(5, 9)
        self.question_swap = ""
        self.question_check = ""
        self.check = 0
        self.swap = 0
        self.test = []
        for i in range(self.n):
            self.list += [random.randint(i+1, i+9)]
        self.list2 = self.list
        print(self)

    def __repr__(self):
        st = str(self.n)+": "
        for i in self.list:
            st += str(i) + " "
        return st

    def __len__(self):
        return self.n

    def __getitem__(self, item):
        return self.list[item]

    def bubble_sort(self):
        """Сортировка пузырьком"""
        self.swap = 0
        self.check = 0
        copy = self.list.copy()
        for i in range(0, self.n):
            for j in range(1, self.n - i):
                if copy[j] < copy[j - 1]:
                    copy[j], copy[j - 1] = copy[j - 1], copy[j]
                    self.swap += 1
                    # print(copy[j], copy[j - 1], self)
                self.check += 1
        return copy

    def choice_sort(self):
        """Сортировка выбором"""
        self.swap = 0
        self.check = 0
        copy = self.list.copy()
        for i in range(0, self.n):
            for j in range(i + 1, self.n):
                if copy[j] < copy[i]:
                    copy[j], copy[i] = copy[j], copy[i]
                    self.swap += 1
                    # print(copy[j], copy[i], self)
                self.check += 1
        return copy

    def create_test(self, func):
        self.question_swap = "Сколько обменов будет совершено в алгоритме " + func.__doc__ + "?"
        self.question_check = "Сколько проверок между элементами будет совершено в алгоритме " + func.__doc__ + "?"
        func()
        self.test = [self.check, self.swap, self.check - self.swap, random.randint(self.swap, self.check+5)]
        random.shuffle(self.test)
        return Elem(self.list, self.question_swap, self.test, self.swap), \
               Elem(self.list, self.question_check, self.test, self.check)


