import ast
import operator

ops = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
       ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg}  # только арифм.


def _ev(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in ops:
        return ops[type(node.op)](_ev(node.left), _ev(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in ops:
        return ops[type(node.op)](_ev(node.operand))
    raise ValueError("bad expr")


def calc(expr):
    # счет без eval, чужой код не вып.
    try:
        return _ev(ast.parse(expr, mode="eval").body)
    except Exception:
        return None
