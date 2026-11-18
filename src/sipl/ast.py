from dataclasses import dataclass
from typing import List, Optional, Union

@dataclass
class SourceSpan:
    line: int = 0
    column: int = 0
    end_line: int = 0
    end_column: int = 0

@dataclass
class ASTNode:
    span: Optional[SourceSpan] = None

@dataclass
class BinOp(ASTNode):
    op: str = ""
    left: Optional[Union['BinOp', 'Num', 'Var']] = None
    right: Optional[Union['BinOp', 'Num', 'Var']] = None

@dataclass
class Num(ASTNode):
    value: int = 0

@dataclass
class Var(ASTNode):
    name: str = ""

Expr = Union[BinOp, Num, Var]

@dataclass
class Assign(ASTNode):
    var: str = ""
    expr: Optional[Expr] = None

@dataclass
class If(ASTNode):
    cond: Optional[BinOp] = None
    then_stmt: Optional[ASTNode] = None
    else_stmt: Optional[ASTNode] = None

@dataclass
class While(ASTNode):
    cond: Optional[BinOp] = None
    body: Optional[ASTNode] = None

@dataclass
class Block(ASTNode):
    statements: List[ASTNode] = None

    def __post_init__(self):
        if self.statements is None:
            self.statements = []

@dataclass
class Skip(ASTNode):
    pass