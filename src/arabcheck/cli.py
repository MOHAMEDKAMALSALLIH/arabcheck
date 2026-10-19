"""واجهة سطر الأوامر."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from . import __version__
from .core import ArabCheck
from .scanner import Scanner


def read_input(args, parser):
    if args.file:
        try:
            return args.file.read_text(encoding="utf-8")
        except FileNotFoundError:
            parser.error(f"الملف غير موجود: {args.file}")
    if args.text:
        return args.text
    if not sys.stdin.isatty():
        return sys.stdin.read()
    parser.error("لازم تمرّر نصاً، أو --file، أو stdin.")
    return ""


def build_parser():
    p = argparse.ArgumentParser(prog="arabcheck", description="ArabCheck — تنظيف وفحص النصوص العربية.")
    p.add_argument("text", nargs="?", help="النص")
    p.add_argument("-f", "--file", type=Path, help="قراءة من ملف")
    p.add_argument("-c", "--clean", action="store_true")
    p.add_argument("-n", "--normalize", action="store_true")
    p.add_argument("-a", "--audit", action="store_true")
    p.add_argument("-j", "--json", action="store_true")
    p.add_argument("-q", "--quiet", action="store_true")
    p.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    return p


def run_scan(argv) -> int:
    """Run the modular scanner without changing legacy CLI parsing."""
    parser = argparse.ArgumentParser(
        prog="arabcheck scan",
        description="فحص النصوص باستخدام قواعد ArabCheck.",
    )
    parser.add_argument("text", nargs="?", help="النص المراد فحصه")
    parser.add_argument("-f", "--file", type=Path, help="قراءة من ملف")
    parser.add_argument(
        "--rules",
        help="أسماء القواعد مفصولة بفواصل، مثل hamzat_qat",
    )
    parser.add_argument("-j", "--json", action="store_true")
    parser.add_argument("-q", "--quiet", action="store_true")

    args = parser.parse_args(argv)
    text = read_input(args, parser)
    scanner = Scanner()
    rule_names = (
        [name.strip() for name in args.rules.split(",") if name.strip()]
        if args.rules else None
    )

    try:
        issues = scanner.scan(text, rule_names=rule_names)
    except ValueError as exc:
        parser.error(str(exc))

    if args.json:
        print(json.dumps({
            "input": text,
            "issues": issues,
            "meta": {
                "rules": rule_names or scanner.available_rules(),
                "version": __version__,
            },
        }, ensure_ascii=False, indent=2))
    else:
        if not args.quiet:
            print(text)
        for issue in issues:
            print(f"⚠️  {issue['message']}", file=sys.stderr)

    return 1 if issues else 0


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    if argv and argv[0] == "scan":
        return run_scan(argv[1:])

    parser = build_parser()
    args = parser.parse_args(argv)
    text = read_input(args, parser)
    checker = ArabCheck()
    result = checker.process(text, clean=args.clean, normalize=args.normalize, audit=args.audit)
    if args.json:
        payload = {**result, "meta": {
            "cleaned": args.clean, "normalized": args.normalize,
            "audited": args.audit, "version": __version__,
        }}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if not args.quiet:
            print(result["result"])
        for issue in result["issues"]:
            print(f"⚠️  {issue['message']}", file=sys.stderr)
    return 1 if result["issues"] else 0


if __name__ == "__main__":
    sys.exit(main())
