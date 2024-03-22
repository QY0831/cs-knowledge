"""
命令模式的目的是解耦调用操作的对象（调用者）和提供实现的对象（接收者）。
这个模式的做法是，在二者之间放一个 Command 对象，让它实现只有一个方法（execute）的接口，调用接收者中的方法执行所需的操作。
"""
from __future__ import annotations
from abc import ABC, abstractmethod

class Receiver: # 接受者：执行具体操作
    """Receiver：定义各种方法以便执行不同的操作"""
    def action1(self):
        print('Execute action1...')

    def action2(self):
        print('Execute action2...')


class Command(ABC): # 命令对象，对特定的操作进行封装，用于创建不同的命令。
    """
    The Command interface declares a method for executing a command.
    """

    @abstractmethod
    def execute(self) -> None:
        pass
    

class Action1(Command):
    
    def __init__(self, receiver):
        self.receiver = receiver
    
    def execute(self):
        self.receiver.action1()
        
         
class Action2(Command):
    
    def __init__(self, receiver):
        self.receiver = receiver
    
    def execute(self):
        self.receiver.action2()


class Invoker: # 调用命令的对象: 请求者
    """创建命令队列，调用并执行队列中的命令"""
    def __init__(self):
        self.actions = []

    def append_action(self, action):
        self.actions.append(action)

    def execute_actions(self):
        for action in self.actions:
            action.execute()
            
            
if __name__ == '__main__':
    receiver = Receiver()
    action1 = Action1(receiver)
    action2 = Action2(receiver)

    invoker = Invoker()
    invoker.append_action(action1)
    invoker.append_action(action2)
    invoker.execute_actions()