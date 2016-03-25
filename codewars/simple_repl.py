# simple_repl.py

from Tester import Test, Tester

import re


def tokenize(expression):
    if expression == "":
        return []

    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]


class Interpreter:

    OPERATOR_PRECEDENCE = {"=": 0, "+": 1, "-": 1, "*": 2, "/": 2, "%": 2}
    OPERATORS = OPERATOR_PRECEDENCE.keys()

    def __init__(self):
        self.vars = {}
        self.functions = {}

    def input(self, expression):
        """
        The algorithm for evaluating any postfix expression is fairly straightforward:

        1 While there are input tokens left
          1.1 Read the next token from input.
          1.2 If the token is a value
              1.2.1 Push it onto the stack.
          1.3 Otherwise, the token is an operator (operator here includes both operators and functions).
              1.3.1 It is already known that the operator takes n arguments.
              1.3.2 If there are fewer than n values on the stack
                    (Error) The user has not input sufficient values in the expression.
              1.3.3 Else, Pop the top n values from the stack.
              1.3.4 Evaluate the operator, with the values as arguments.
              1.3.5 Push the returned results, if any, back onto the stack.
        2 If there is only one value in the stack
          2.1 That value is the result of the calculation.
        3 Otherwise, there are more values in the stack
          (Error) The user input has too many values.
        """
        if not expression.strip():
            return ""
        rpn = self.infix_to_postfix(expression)
        # print "expression = %s\nrpn = %s" % (expression, rpn)
        tokens = tokenize(rpn)
        stack = []
        for token in tokens:
            if token in self.OPERATORS:
                if len(stack) >= 2:
                    v1 = stack.pop()
                    v2 = stack.pop()
                    stack.append(self.binary_operation(token, v2, v1))
                else:
                    raise RuntimeError("INSUFFICIENT VALUES")
            elif token.isdigit():
                stack.append(int(token))
            elif token in self.vars.keys():
                stack.append(self.vars[token])
            else:
                stack.append(token)
        if len(stack) != 1:
            raise RuntimeError("TOO MANY VALUES: %s -> %s = %s" % (expression, rpn, str(stack)))
        elif type(stack[-1]) == str:
            raise RuntimeError("UNKNOWN VARIABLE")
        # print "%s = %s = %s" % (expression, rpn, str(stack[0]))
        return stack.pop()

    def binary_operation(self, op, v1, v2):
        if op == "+":
            return v1 + v2
        elif op == "-":
            return v1 - v2
        elif op == "*":
            return v1 * v2
        elif op == "/":
            return v1 / v2
        elif op == "%":
            return v1 % v2
        elif op == "=":
            self.vars[v1] = v2
            return v2

    def infix_to_postfix(self, infix_expression):
        """
        1 While there are tokens to be read:
          1.1 Read a token.
          1.2 If the token is a number, then add it to the output queue.
          1.3 If the token is a function token, then push it onto the stack.
          1.4 If the token is a function argument separator (e.g., a comma):
              1.4.1 Until the token at the top of the stack is a left parenthesis, pop operators off
                        the stack onto the output queue. If no left parentheses are encountered, either
                        the separator was misplaced or parentheses were mismatched.
          1.5 If the token is an operator, o1, then:
              1.5.1 while there is an operator token o2, at the top of the operator stack and either
                        o1 is left-associative and its precedence is less than or equal to that of o2, or
                        o1 is right associative, and has precedence less than that of o2,
                    1.5.1.1 pop o2 off the operator stack, onto the output queue;
              1.5.2 at the end of iteration push o1 onto the operator stack.
          1.6 If the token is a left parenthesis (i.e. "("), then push it onto the stack.
          1.7 If the token is a right parenthesis (i.e. ")"):
              1.7.1 Until the token at the top of the stack is a left parenthesis, pop operators off the stack onto the output queue.
              1.7.2 Pop the left parenthesis from the stack, but not onto the output queue.
              1.7.3 If the token at the top of the stack is a function token, pop it onto the output queue.
              1.7.4 If the stack runs out without finding a left parenthesis, then there are mismatched parentheses.
        2 When there are no more tokens to read:
          2.1 While there are still operator tokens in the stack:
              2.1.1 If the operator token on the top of the stack is a parenthesis, then there are mismatched parentheses.
              2.1.2 Pop the operator onto the output queue.
        3 Exit.
        """
        tokens = tokenize(infix_expression)
        queue = []
        stack = []
        while tokens:
            # 1.1
            token = tokens[0]
            tokens = tokens[1:]
            if not (token in self.OPERATORS or token == "(" or token == ")"):
                queue.append(token)
            # 1.5
            elif token in self.OPERATORS:
                # 1.5.1
                while stack and stack[-1] in self.OPERATORS and (self.OPERATOR_PRECEDENCE[token] <= self.OPERATOR_PRECEDENCE[stack[-1]]):
                    queue.append(stack.pop())
                stack.append(token)
            elif token == "(":
                stack.append(token)
            elif token == ")":
                while stack and stack[-1] != "(":
                    queue.append(stack.pop())
                if stack and stack[-1] == "(":
                    stack.pop()
                else:
                    raise RuntimeError("PAREN MISMATCH")
        while stack and len(stack) > 0:
            if stack[-1] == "(":
                raise RuntimeError("PAREN MISMATCH")
            else:
                queue.append(stack.pop())
        return " ".join(queue)

test = Tester()

interpreter = Interpreter();

# Basic arithmetic
test.assert_equals(interpreter.input("1 + 1"), 2, "1 + 1")
test.assert_equals(interpreter.input("2 - 1"), 1, "2 - 1")
test.assert_equals(interpreter.input("2 * 3"), 6, "2 * 3")
test.assert_equals(interpreter.input("8 / 4"), 2, "8 / 4")
test.assert_equals(interpreter.input("7 % 4"), 3, "7 % 4")

# Variables
test.assert_equals(interpreter.input("x = 1"), 1, "x = 1")
test.assert_equals(interpreter.input("x"), 1, "x")
test.assert_equals(interpreter.input("x + 3"), 4, "x + 3")
test.expect_error("input: 'y'", lambda: interpreter.input("y"))