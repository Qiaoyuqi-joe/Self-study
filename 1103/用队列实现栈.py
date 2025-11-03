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
    



    #-----------------------------------------------------------

    #使用一个队列完成 把最后进去的数值留下 其他n-1个数值出队再入队  保证最后一个进来的数值在对头


from collections import deque

class MyStack:
    def __init__(self):
        self.q = deque()
    def push(self,x:int) -> None:
        self.q.append(x)
        for _ in range (len(self.q)-1):
            self.q.append(self.q.popleft())

    def pop(self) -> int:
        return self.q.popleft()  #直接这么写 是因为所有元素在入栈的时候已经经历过了push的调整了 所以直接就可以popleft（）
    #出栈 直接弹出
    def top(self) -> int:
        return self.q[0]#只读取数值 不删除
    def empty(self) -> bool:
        return not self.q