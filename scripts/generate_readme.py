#!/usr/bin/env python3
"""
Scans LeetCode problem directories and updates README.md between sentinel markers.
"""

from pathlib import Path
import re
import sys

START_MARKER = "<!-- LEETCODE-STATS:START -->"
END_MARKER = "<!-- LEETCODE-STATS:END -->"

# Matches patterns like '0001-Two-Sum' or '1021-Remove-Outermost-Parentheses'
FOLDER_PATTERN = re.compile(r"^(\d+)-(.+)$")


def parse_repository(root_dir: Path):
    problems = []

    for entry in root_dir.iterdir():
        if not entry.is_dir():
            continue

        match = FOLDER_PATTERN.match(entry.name)
        if not match:
            continue

        prob_num = int(match.group(1))
        raw_slug = match.group(2)
        prob_title = raw_slug.replace("-", " ").strip()

        # Check solutions (handling standard file names)
        cpp_files = list(entry.glob("*.cpp")) + list(entry.glob("*.cc"))
        py_files = list(entry.glob("*.py"))

        has_cpp = len(cpp_files) > 0
        has_py = len(py_files) > 0

        if not has_cpp and not has_py:
            continue

        cpp_rel_path = cpp_files[0].relative_to(root_dir).as_posix() if has_cpp else None
        py_rel_path = py_files[0].relative_to(root_dir).as_posix() if has_py else None

        problems.append({
            "number": prob_num,
            "raw_number": match.group(1),
            "title": prob_title,
            "folder": entry.name,
            "has_cpp": has_cpp,
            "has_py": has_py,
            "cpp_path": cpp_rel_path,
            "py_path": py_rel_path,
        })

    # Sort numerically by problem ID
    problems.sort(key=lambda x: x["number"])
    return problems


def build_markdown_stats(problems: list) -> str:
    total_solved = len(problems)
    cpp_count = sum(1 for p in problems if p["has_cpp"])
    py_count = sum(1 for p in problems if p["has_py"])
    both_count = sum(1 for p in problems if p["has_cpp"] and p["has_py"])
    cpp_only = sum(1 for p in problems if p["has_cpp"] and not p["has_py"])
    py_only = sum(1 for p in problems if p["has_py"] and not p["has_cpp"])

    lines = [
        START_MARKER,
        "",
        "### 📈 Summary Metrics",
        "",
        "| Metric | Count |",
        "| :--- | :--- |",
        f"| 🎯 **Total Unique Problems Solved** | **{total_solved}** |",
        f"| ⚡ **C++ Solutions** | **{cpp_count}** |",
        f"| 🐍 **Python Solutions** | **{py_count}** |",
        f"| 🔄 **Solved in Both (C++ & Python)** | **{both_count}** |",
        f"| 🔷 **C++ Only** | **{cpp_only}** |",
        f"| 🟨 **Python Only** | **{py_only}** |",
        "",
        "### 📚 Problem Directory",
        "",
        "<details>",
        "<summary><b>Click to expand full solutions list</b></summary>",
        "",
        "| # | Problem Title | Solutions |",
        "| :---: | :--- | :---: |",
    ]

    for p in problems:
        badges = []
        if p["has_cpp"]:
            badges.append(f"[C++]({p['cpp_path']})")
        if p["has_py"]:
            badges.append(f"[Python]({p['py_path']})")

        solution_links = " \\| ".join(badges)
        lines.append(f"| {p['number']} | **{p['title']}** | {solution_links} |")

    lines.extend([
        "",
        "</details>",
        "",
        f"*Last updated automatically: {Path.cwd().name} automated scan.*",
        END_MARKER,
    ])

    return "\n".join(lines)


def update_readme(readme_path: Path, stats_markdown: str):
    if not readme_path.exists():
        print(f"Error: {readme_path} not found.")
        sys.exit(1)

    content = readme_path.read_text(encoding="utf-8")

    if START_MARKER not in content or END_MARKER not in content:
        print(f"Error: Sentinel markers '{START_MARKER}' or '{END_MARKER}' not found in README.")
        sys.exit(1)

    pattern = re.compile(
        f"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}",
        re.DOTALL,
    )

    new_content = pattern.sub(stats_markdown, content)

    if new_content == content:
        print("No changes needed in README.md.")
        return False

    readme_path.write_text(new_content, encoding="utf-8")
    print("README.md updated successfully.")
    return True


def main():
    root = Path(__file__).resolve().parent.parent
    readme_file = root / "README.md"

    problems = parse_repository(root)
    stats_md = build_markdown_stats(problems)
    update_readme(readme_file, stats_md)


if __name__ == "__main__":
    main()
