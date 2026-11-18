import json
from typing import Any
from sipl.ast import ASTNode, Assign, Num, Var, BinOp

def ast_to_dict(node: Any) -> Any:
    if isinstance(node, ASTNode):
        res = {"kind": type(node).__name__}
        for k, v in node.__dict__.items():
            if k != "span":
                res[k] = ast_to_dict(v)
        return res
    elif isinstance(node, list):
        return [ast_to_dict(i) for i in node]
    return node

def export_json(node: ASTNode) -> str:
    return json.dumps(ast_to_dict(node), indent=2, ensure_ascii=False)

def export_dot(node: ASTNode) -> str:
    dot_lines = ["digraph AST {", '  node [shape=box, fontname="Arial"];']
    counter = [0]

    def traverse(n: Any) -> int:
        curr_id = counter[0]
        counter[0] += 1
        label = type(n).__name__
        if isinstance(n, Assign): label += f"\\n({n.var})"
        elif isinstance(n, Num): label += f"\\n({n.value})"
        elif isinstance(n, Var): label += f"\\n({n.name})"
        elif isinstance(n, BinOp): label += f"\\n({n.op})"

        dot_lines.append(f'  node{curr_id} [label="{label}"];')

        for k, v in n.__dict__.items():
            if k == "span": continue
            if isinstance(v, ASTNode):
                child_id = traverse(v)
                dot_lines.append(f'  node{curr_id} -> node{child_id} [label="{k}"];')
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, ASTNode):
                        child_id = traverse(item)
                        dot_lines.append(f'  node{curr_id} -> node{child_id} [label="{k}[]"];')
        return curr_id

    if isinstance(node, ASTNode):
        traverse(node)
    dot_lines.append("}")
    return "\n".join(dot_lines)