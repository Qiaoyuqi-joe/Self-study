from collections import deque

class MyStack:
    def __init__(self):
        self.q1 = deque()
        self.q2 = deque()
        #初始化队列 q1为主队列 q2为中转队列
    
    def push(self,x:int) -> None:
        self.q1.append(x)

    def pop(self) -> int:
        if not self.q1:
            return None
        #如果主队列为空 说明栈空

        while len(self.q1) > 1:
            self.q2.append(self.q1.popleft())

        top_val = self.q1.popleft()

        self.q1,self.q2 = self.q2,self.q1

        return top_val
    
    def top(self) -> int:
        top_val = self.pop()

        if top_val is not None:
            self.q1.append(top_val)
        return top_val
    def empty(self) -> bool:
        return not self.q1