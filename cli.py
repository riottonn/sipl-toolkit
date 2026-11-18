import argparse
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from sipl.parser import parse_sipl
from sipl.interpreter import SIPLInterpreter
from sipl.semantics import generate_semantic_term
from sipl.visualization import export_json, export_dot

def main():
    parser = argparse.ArgumentParser(description="SIPL Language Toolkit CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_parse = subparsers.add_parser("parse", help="Parse file to JSON AST")
    p_parse.add_argument("file", type=Path)

    p_dot = subparsers.add_parser("dot", help="Export AST to Graphviz DOT format")
    p_dot.add_argument("file", type=Path)

    p_check = subparsers.add_parser("check", help="Checking for syntactic correctness")
    p_check.add_argument("file", type=Path)

    p_run = subparsers.add_parser("run", help="Program execution with an initial state")
    p_run.add_argument("file", type=Path)
    p_run.add_argument("--state", type=str, default="{}", help="JSON with state")

    p_trace = subparsers.add_parser("trace", help="Outputting a step-by-step execution trace")
    p_trace.add_argument("file", type=Path)
    p_trace.add_argument("--state", type=str, default="{}", help="JSON with state")

    p_sem = subparsers.add_parser("term", help="Semantic term generation")
    p_sem.add_argument("file", type=Path)

    args = parser.parse_args()
    code = args.file.read_text(encoding="utf-8")

    try:
        if args.command == "check":
            parse_sipl(code)
            print("OK: The syntax is correct.")
        elif args.command == "parse":
            ast = parse_sipl(code)
            print(export_json(ast))
        elif args.command == "dot":
            ast = parse_sipl(code)
            print(export_dot(ast))
        elif args.command == "run":
            ast = parse_sipl(code)
            state = json.loads(args.state)
            interpreter = SIPLInterpreter()
            interpreter.execute(ast, state)
            print(json.dumps(state, indent=2, ensure_ascii=False))
        elif args.command == "trace":
            ast = parse_sipl(code)
            state = json.loads(args.state)
            interpreter = SIPLInterpreter()
            interpreter.execute(ast, state)
            print(json.dumps(interpreter.trace_log, indent=2, ensure_ascii=False))
        elif args.command == "term":
            ast = parse_sipl(code)
            print(generate_semantic_term(ast))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()