from typing import Any
from lark import Tree
from sipl.ast import ASTNode, Assign, Block, Skip, If, While, BinOp, Num, Var

def generate_semantic_term(node: Any) -> str:
    if isinstance(node, Tree):
        terms = [generate_semantic_term(child) for child in node.children if isinstance(child, (ASTNode, Tree))]
        return " ; ".join([t for t in terms if t]) if terms else "skip"
    
    if isinstance(node, Skip):
        return "skip"
    elif isinstance(node, Assign):
        return f"{node.var} := {expr_to_string(node.expr)}"
    elif isinstance(node, Block):
        terms = [generate_semantic_term(s) for s in node.statements if s is not None]
        return " ; ".join(terms) if terms else "skip"
    elif isinstance(node, If):
        then_t = generate_semantic_term(node.then_stmt) if node.then_stmt else "skip"
        else_t = generate_semantic_term(node.else_stmt) if node.else_stmt else "skip"
        return f"if {expr_to_string(node.cond)} then {{ {then_t} }} else {{ {else_t} }}"
    elif isinstance(node, While):
        body_t = generate_semantic_term(node.body) if node.body else "skip"
        return f"while {expr_to_string(node.cond)} do {{ {body_t} }}"
    return f"/* {type(node).__name__} */"

def expr_to_string(expr: Any) -> str:
    if expr is None:
        return ""
    if isinstance(expr, Num):
        return str(expr.value)
    elif isinstance(expr, Var):
        return expr.name
    elif isinstance(expr, BinOp):
        left_str = expr_to_string(expr.left)
        right_str = expr_to_string(expr.right)
        return f"({left_str} {expr.op} {right_str})"
    return str(expr)