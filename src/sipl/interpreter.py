from typing import Dict, Any, List
from sipl.ast import ASTNode, Assign, Block, Skip, If, While, BinOp, Num, Var

class InterpreterError(Exception):
    pass

class SIPLInterpreter:
    def __init__(self, max_steps: int = 10000):
        self.max_steps = max_steps
        self.steps_count = 0
        self.trace_log: List[Dict[str, Any]] = []

    def eval_expr(self, expr: Any, state: Dict[str, int]) -> int:
        if isinstance(expr, Num):
            return expr.value
        elif isinstance(expr, Var):
            if expr.name not in state:
                state[expr.name] = 0
            return state[expr.name]
        elif isinstance(expr, BinOp):
            left = self.eval_expr(expr.left, state)
            right = self.eval_expr(expr.right, state)
            if expr.op == "+": return left + right
            if expr.op == "-": return left - right
            if expr.op == "*": return left * right
            if expr.op == ">": return int(left > right)
            if expr.op == "<": return int(left < right)
            if expr.op == "=": return int(left == right)
        return int(expr)

    def execute(self, node: ASTNode, state: Dict[str, int]) -> None:
        self.steps_count += 1
        if self.steps_count > self.max_steps:
            raise InterpreterError("Execution step limit exceeded (possible infinite loop).")

        self.trace_log.append({
            "step": self.steps_count,
            "node": type(node).__name__,
            "state": dict(state)
        })

        if isinstance(node, Assign):
            val = self.eval_expr(node.expr, state)
            state[node.var] = val
        elif isinstance(node, Block):
            for stmt in node.statements:
                self.execute(stmt, state)
        elif isinstance(node, Skip):
            pass
        elif isinstance(node, If):
            if self.eval_expr(node.cond, state):
                self.execute(node.then_stmt, state)
            else:
                self.execute(node.else_stmt, state)
        elif isinstance(node, While):
            while self.eval_expr(node.cond, state):
                self.execute(node.body, state)