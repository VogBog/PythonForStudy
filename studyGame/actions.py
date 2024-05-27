class Action:
    def __init__(self):
        self.arr = []

    def add(self, func: callable):
        self.arr.append(func)

    def remove(self, func: callable):
        if func in self.arr:
            self.arr.remove(func)

    def clear(self):
        self.arr.clear()

    def invoke(self):
        for func in self.arr:
            func()

    def is_empty(self) -> bool:
        return len(self.arr) > 0