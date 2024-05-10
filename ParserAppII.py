class Node:
    def __init__(self, symbol, left=None, right=None):
        self.symbol = symbol
        self.leftChild = left
        self.rightChild = right

    def __str__(self):
        return self.symbol

import sys


error = False
next_token = '%'
input_stream = []

def lex():
    global next_token
    while input_stream and input_stream[0] in ' \n\t':
        input_stream.pop(0)
    if input_stream:
        next_token = input_stream.pop(0)
    else:
        next_token = '$'

def printTree(tree):
    if tree:
        printTree(tree.leftChild)
        printTree(tree.rightChild)
        print(tree.symbol, end=' ')

def evaluate(tree):
    if tree is None:
        return 0
    if tree.symbol.isdigit():
        return int(tree.symbol)
    elif tree.symbol == '+':
        return evaluate(tree.leftChild) + evaluate(tree.rightChild)
    elif tree.symbol == '-':
        return evaluate(tree.leftChild) - evaluate(tree.rightChild)
    elif tree.symbol == '*':
        return evaluate(tree.leftChild) * evaluate(tree.rightChild)
    elif tree.symbol == '/':
        return evaluate(tree.leftChild) / evaluate(tree.rightChild)
    elif tree.symbol == 'a':
        return 10
    elif tree.symbol == 'b':
        return 20
    elif tree.symbol == 'c':
        return 30
    elif tree.symbol == 'd':
        return 40

def unconsumed_input():
    return ''.join(input_stream)

def G():
    global error
    lex()
    print("G -> E")
    tree = E()
    if next_token == '$' and not error:
        print("success")
        return tree
    else:
        print("failure: unconsumed input=", unconsumed_input())
        return None

def E():
    global error
    if error:
        return None
    print("E -> T R")
    temp = T()
    return R(temp)

def R(tree):
    global error
    if error:
        return None
    if next_token == '+':
        print("R -> + T R")
        lex()
        temp1 = T()
        temp2 = R(temp1)
        return Node('+', tree, temp2)
    elif next_token == '-':
        print("R -> - T R")
        lex()
        temp1 = T()
        temp2 = R(temp1)
        return Node('-', tree, temp2)
    else:
        print("R -> e")
        return tree

def T():
    global error
    if error:
        return None
    print("T -> F S")
    temp = F()
    return S(temp)

def S(tree):
    global error
    if error:
        return None
    if next_token == '*':
        print("S -> * F S")
        lex()
        temp1 = F()
        temp2 = S(temp1)
        return Node('*', tree, temp2)
    elif next_token == '/':
        print("S -> / F S")
        lex()
        temp1 = F()
        temp2 = S(temp1)
        return Node('/', tree, temp2)
    else:
        print("S -> e")
        return tree

def F():
    global error
    if error:
        return None
    if next_token == '(':
        print("F -> ( E )")
        lex()
        temp = E()
        if next_token == ')':
            lex()
            return temp
        else:
            error = True
            print("error: unexpected token", next_token)
            print("unconsumed input", unconsumed_input())
            return None
    elif next_token in 'abcd':
        return M()
    elif next_token in '0123':
        return N()
    else:
        error = True
        print("error: unexpected token", next_token)
        print("unconsumed input", unconsumed_input())
        return None

def M():
    global error
    if error:
        return None
    symbol = next_token
    lex()
    return Node(symbol)

def N():
    global error
    if error:
        return None
    symbol = next_token
    lex()
    return Node(symbol)

def main():
    global input_stream
    with open('expression.txt', 'r') as file:
        input_stream = list(file.read().strip())
    theTree = G()
    if not error:
        print("\nPostfix notation of the tree:")
        printTree(theTree)
        print("\nThe evaluated value is:", evaluate(theTree))
    else:
        print("Input not parsed correctly")

if __name__ == "__main__":
    main()
