from DS.stack import Stack

_nav_stack = Stack()

def open_view(view):
    _nav_stack.push(view)
    print("STACK PUSH →", _nav_stack.items)

def go_back():
    _nav_stack.pop()
    print("STACK POP →", _nav_stack.items)
    return _nav_stack.peek()

def current_view():
    return _nav_stack.peek()
