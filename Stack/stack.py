# pilha
# princípio L.I.F.O - Last In First Out

class Node:
    def __init__(self, data):
        self.data = data
        self.above = None

    def __str__(self):
        return f'{self.data}'


class Stack:
    def __init__(self):
        self.total = 0
        self.stack = None

    def __str__(self):
        if self.total == 0:
            return '[]'
        stack = '['
        current_element = self.stack
        while current_element.above:
            stack += f'{current_element}, '
            current_element = current_element.above
        stack += f'{current_element}]'
        return stack

    def __len__(self):
        return self.total

    def __push(self, stack, node):
        if not stack:
            return node
        stack.above = self.__push(stack.above, node)
        return stack

    def push(self, data):
        node = Node(data)
        self.stack = self.__push(self.stack, node)
        self.total += 1

    def __pop(self, current_element, above_element):
        if not above_element.above:
            current_element.above = None
        if above_element.above:
            self.__pop(current_element.above, current_element.above.above)

    def pop(self):
        if self.total > 1:
            current_element = self.stack
            above_element = current_element.above
            self.__pop(current_element, above_element)
        else:
            self.stack = None
        self.total -= 1


stack = Stack()
stack.push(10)
stack.push(53)
stack.push(23)
stack.push(9)
stack.push(60)

print(stack)

stack.pop()
stack.pop()
stack.pop()
stack.pop()
stack.pop()
print(stack)
