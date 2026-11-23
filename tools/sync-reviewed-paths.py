"""Compare reviewed rulebook corrections. Write the report outside the site."""

import argparse
from collections import Counter
import json
from pathlib import Path
import re


BASE_CHAPTERS = {
    17: 4, 18: 4, 19: 5, 20: 5, 21: None, 22: 7, 23: 8, 24: 9,
    25: 9, 26: 10, 27: 11, 28: 9, 29: 12, 30: 13, 31: 14, 32: 15, 33: 16,
}
EDITORIAL = re.compile(r"примечани[ея]|переводчик|оригинал|уточн|спорн|ведущ", re.I)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def file_and_chapter(value):
    path, separator, chapter = value.rpartition("=")
    if not separator or not path or not chapter.isdecimal() or not 1 <= int(chapter) <= 22:
        raise argparse.ArgumentTypeError("expected a review path and chapter number, e.g. v34.json=17")
    return Path(path), int(chapter)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--rulings", type=Path, required=True)
    parser.add_argument("--approved", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, help="directory containing the latest reviewed chapters")
    parser.add_argument("--reviewed-rulings", type=Path, help="separately approved exceptions")
    parser.add_argument("--extra-review", action="append", default=[], type=file_and_chapter,
                        metavar="JSON=CHAPTER", help="review file and its chapter number, e.g. v34.json=17")
    parser.add_argument("--apply", action="store_true")
    return parser.parse_args()


def compare_correction(current, final, correction, approved, blocked, apply):
    paragraph = correction["paragraph"]
    before, after = correction["before"], correction["after"]
    if paragraph in blocked:
        return current, "check source ambiguity and Foundry-specific ruling"
    if EDITORIAL.search(after):
        return current, "check editorial wording and whether it belongs on site"
    if after not in final:
        return current, "compare with later source: superseded or absent"

    if current.count(before) == 1:
        if paragraph not in approved:
            return current, "check meaning and current site terminology"
        return current.replace(before, after, 1), "applied" if apply else "candidate"

    line = correction.get("line", 0)
    if paragraph in approved and line > 0:
        lines = current.splitlines(keepends=True)
        final_lines = final.splitlines()
        if line <= min(len(lines), len(final_lines)):
            if lines[line - 1].count(before) == 1 and after in final_lines[line - 1]:
                lines[line - 1] = lines[line - 1].replace(before, after, 1)
                status = "applied at verified line" if apply else "candidate at verified line"
                return "".join(lines), status
    if after in current:
        return current, "already present; verify if repeated elsewhere"
    return current, "locate original with surrounding context"


def main():
    args = parse_args()
    site = Path(__file__).resolve().parents[1] / "docs"
    book = site / "book"
    if args.report.resolve().is_relative_to(site):
        raise SystemExit("Write the report outside docs.")
    snapshot = args.snapshot or args.source / "book-v33-path-sources-20261123"
    approved = set(read_json(args.approved))
    reviewed_rulings = set(read_json(args.reviewed_rulings)) if args.reviewed_rulings else set()
    rulings = args.rulings.read_text(encoding="utf-8")
    blocked = {int(value) for value in re.findall(r"(?<!\d)\d{3,5}(?!\d)", rulings)} | {11404}
    blocked -= reviewed_rulings
    review_files = [
        (path, chapter) for version, chapter in BASE_CHAPTERS.items()
        for path in sorted(args.source.glob(f"book-v{version}-*review-20261123.json"))
    ]
    review_files.extend(args.extra_review)
    contents = {}
    results = []
    for review, chapter in review_files:
        if chapter is None:
            chapter = int(re.search(r"path-(\d+)", review.name).group(1))
        name = f"chapter-10-{chapter:02}.md"
        if name not in contents:
            contents[name] = (book / name).read_text(encoding="utf-8")
        current = contents[name]
        final = (snapshot / name).read_text(encoding="utf-8")
        for correction in read_json(review)["corrections"]:
            current, status = compare_correction(current, final, correction, approved, blocked, args.apply)
            results.append({
                "review": review.name,
                "chapter": name,
                "paragraph": correction["paragraph"],
                "status": status,
                "before": correction["before"],
                "after": correction["after"],
            })
        contents[name] = current

    args.report.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.apply:
        for name, text in contents.items():
            path = book / name
            raw = path.read_bytes()
            if text != raw.decode("utf-8").replace("\r\n", "\n"):
                newline = "\r\n" if b"\r\n" in raw else "\n"
                path.write_bytes(text.replace("\n", newline).encode("utf-8"))
    print(Counter(entry["status"] for entry in results))


if __name__ == "__main__":
    main()
