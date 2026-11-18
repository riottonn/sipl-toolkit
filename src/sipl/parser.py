from pathlib import Path
from lark import Lark, Transformer
from sipl.ast import Assign, If, While, Block, Skip, BinOp, Num, Var, SourceSpan

class SIPLTransformer(Transformer):
    def num(self, items):
        return Num(value=int(items[0]), span=SourceSpan(0, 0, 0, 0))

    def var(self, items):
        return Var(name=str(items[0]), span=SourceSpan(0, 0, 0, 0))

    def add(self, items):
        return BinOp(op="+", left=items[0], right=items[1], span=SourceSpan(0, 0, 0, 0))

    def sub(self, items):
        return BinOp(op="-", left=items[0], right=items[1], span=SourceSpan(0, 0, 0, 0))

    def mul(self, items):
        return BinOp(op="*", left=items[0], right=items[1], span=SourceSpan(0, 0, 0, 0))

    def gt(self, items):
        return BinOp(op=">", left=items[0], right=items[1], span=SourceSpan(0, 0, 0, 0))

    def lt(self, items):
        return BinOp(op="<", left=items[0], right=items[1], span=SourceSpan(0, 0, 0, 0))

    def eq(self, items):
        return BinOp(op="=", left=items[0], right=items[1], span=SourceSpan(0, 0, 0, 0))

    def assignment(self, items):
        return Assign(var=str(items[0]), expr=items[1], span=SourceSpan(0, 0, 0, 0))

    def conditional(self, items):
        return If(cond=items[0], then_stmt=items[1], else_stmt=items[2], span=SourceSpan(0, 0, 0, 0))

    def while_loop(self, items):
        return While(cond=items[0], body=items[1], span=SourceSpan(0, 0, 0, 0))

    def skip_stmt(self, items):
        return Skip(span=SourceSpan(0, 0, 0, 0))

    def block(self, items):
        return Block(statements=[i for i in items if i is not None], span=SourceSpan(0, 0, 0, 0))

    def start(self, items):
        return items[0]

def parse_sipl(code: str) -> Block:
    grammar_path = Path(__file__).resolve().parents[2] / "grammar" / "sipl.lark"
    parser = Lark(
        grammar_path.read_text(encoding="utf-8"),
        parser="lalr",
    )
    tree = parser.parse(code)
    return SIPLTransformer().transform(tree)