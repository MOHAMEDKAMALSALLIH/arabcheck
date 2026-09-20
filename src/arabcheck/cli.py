"""واجهة سطر الأوامر."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from . import __version__
from .core import ArabCheck


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


def main(argv=None) -> int:
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
