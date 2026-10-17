#!/usr/bin/env python3
"""
Scans LeetCode problem directories, parses solution headers and git commit dates,
and updates README.md between sentinel markers with an interactive dashboard.
"""

from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
import re
import subprocess
import sys

START_MARKER = "<!-- LEETCODE-STATS:START -->"
END_MARKER = "<!-- LEETCODE-STATS:END -->"

FOLDER_PATTERN = re.compile(r"^(\d+)-(.+)$")
DIFFICULTY_PATTERN = re.compile(r"Difficulty:\s*(Easy|Medium|Hard)", re.IGNORECASE)

# IST: UTC + 5:30
IST = timezone(timedelta(hours=5, minutes=30))

# Replace with your public LeetCode handle
LEETCODE_USERNAME = "pranesh0805-s"
MILESTONE_TARGET = 100


def get_first_commit_date(repo_dir: Path, folder_name: str) -> str:
    """Gets the date (YYYY-MM-DD in IST) when the problem folder was first committed."""
    try:
        cmd = ["git", "log", "--reverse", "--format=%ct", "--", folder_name]
        result = subprocess.run(
            cmd, cwd=repo_dir, capture_output=True, text=True, check=True
        )
        timestamps = result.stdout.strip().split()
        if timestamps:
            epoch = int(timestamps[0])
            dt = datetime.fromtimestamp(epoch, tz=IST)
            return dt.strftime("%Y-%m-%d")
    except Exception:
        pass
    return datetime.now(IST).strftime("%Y-%m-%d")


def extract_difficulty(file_paths: list[Path]) -> str:
    """Parses difficulty from comments/docstrings in solution files."""
    for path in file_paths:
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
            match = DIFFICULTY_PATTERN.search(content)
            if match:
                return match.group(1).capitalize()
        except Exception:
            continue
    return "Unrated"


def format_difficulty_badge(difficulty: str) -> str:
    colors = {
        "Easy": "00b8a3",
        "Medium": "ffc01e",
        "Hard": "ff375f",
        "Unrated": "gray"
    }
    color = colors.get(difficulty, "gray")
    return f"![{difficulty}](https://img.shields.io/badge/-{difficulty}-{color}?style=flat-square)"


def parse_repository(root_dir: Path):
    problems = []

    for entry in root_dir.iterdir():
        if not entry.is_dir():
            continue

        match = FOLDER_PATTERN.match(entry.name)
        if not match:
            continue

        prob_num = int(match.group(1))
        slug = match.group(2)
        prob_title = slug.replace("-", " ").strip()
        leetcode_url = f"https://leetcode.com/problems/{slug.lower()}/"

        cpp_files = list(entry.glob("*.cpp")) + list(entry.glob("*.cc"))
        py_files = list(entry.glob("*.py"))

        has_cpp = len(cpp_files) > 0
        has_py = len(py_files) > 0

        if not has_cpp and not has_py:
            continue

        difficulty = extract_difficulty(cpp_files + py_files)
        cpp_rel_path = cpp_files[0].relative_to(root_dir).as_posix() if has_cpp else None
        py_rel_path = py_files[0].relative_to(root_dir).as_posix() if has_py else None
        date_solved = get_first_commit_date(root_dir, entry.name)

        problems.append({
            "number": prob_num,
            "raw_number": match.group(1),
            "title": prob_title,
            "slug": slug,
            "url": leetcode_url,
            "folder": entry.name,
            "difficulty": difficulty,
            "has_cpp": has_cpp,
            "has_py": has_py,
            "cpp_path": cpp_rel_path,
            "py_path": py_rel_path,
            "date_solved": date_solved,
        })

    return problems


def build_markdown_stats(problems: list) -> str:
    problems_by_number = sorted(problems, key=lambda x: x["number"])

    total_solved = len(problems_by_number)
    cpp_count = sum(1 for p in problems_by_number if p["has_cpp"])
    py_count = sum(1 for p in problems_by_number if p["has_py"])
    both_count = sum(1 for p in problems_by_number if p["has_cpp"] and p["has_py"])

    easy_problems = [p for p in problems_by_number if p["difficulty"] == "Easy"]
    medium_problems = [p for p in problems_by_number if p["difficulty"] == "Medium"]
    hard_problems = [p for p in problems_by_number if p["difficulty"] == "Hard"]

    pct = min(100, int((total_solved / MILESTONE_TARGET) * 100)) if MILESTONE_TARGET else 0

    # Group by commit date
    by_date = defaultdict(list)
    for p in problems:
        by_date[p["date_solved"]].append(p)

    sorted_dates = sorted(by_date.keys(), reverse=True)
    today_ist = datetime.now(IST).strftime("%Y-%m-%d")
    yesterday_ist = (datetime.now(IST) - timedelta(days=1)).strftime("%Y-%m-%d")

    lines = [
        START_MARKER,
        "",
        "### 🎮 Dashboard & Quick Navigation",
        "",
        f'<p align="center">',
        f'  <a href="https://leetcode.com/u/{LEETCODE_USERNAME}/" target="_blank" rel="noopener noreferrer">',
        f'    <img src="https://leetcard.jacoblin.cool/{LEETCODE_USERNAME}?theme=dark&font=baloo&ext=activity" alt="LeetCode Profile Card" width="520" />',
        f'  </a>',
        f'</p>',
        "",
        f"> **Milestone Target ({total_solved}/{MILESTONE_TARGET}):**",
        f'> <progress value="{total_solved}" max="{MILESTONE_TARGET}" style="width: 100%; height: 16px;"></progress> `{pct}% Completed`',
        "",
        "| 🎯 Difficulty Jump | ⚡ Language Views | 📅 Activity & Full Index |",
        "| :---: | :---: | :---: |",
        f"| [🟢 Easy ({len(easy_problems)})](#-easy-problems) • [🟡 Medium ({len(medium_problems)})](#-medium-problems) • [🔴 Hard ({len(hard_problems)})](#-hard-problems) | [🔷 C++ ({cpp_count})](#-c-solutions) • [🟨 Python ({py_count})](#-python-solutions) | [🗓️ Activity Log](#-daily-activity-log) • [📖 Full Index](#-all-solutions-index) |",
        "",
        "### 📊 Breakdown",
        "",
        "| Category | Count | Status Badge |",
        "| :--- | :---: | :--- |",
        f"| **Easy** | `{len(easy_problems)}` | {format_difficulty_badge('Easy')} |",
        f"| **Medium** | `{len(medium_problems)}` | {format_difficulty_badge('Medium')} |",
        f"| **Hard** | `{len(hard_problems)}` | {format_difficulty_badge('Hard')} |",
        f"| **C++ Solutions** | `{cpp_count}` | `⚡ Modern C++` |",
        f"| **Python Solutions** | `{py_count}` | `🐍 Python 3` |",
        f"| **Dual-Language** | `{both_count}` | `🔄 Both Implemented` |",
        "",
        "---",
        "",
        "### 📅 Daily Activity Log",
        "",
    ]

    # Daily Timeline
    for date_str in sorted_dates:
        if date_str == today_ist:
            label = f"🔥 Today ({date_str}) — {len(by_date[date_str])} solved"
            is_open = " open"
        elif date_str == yesterday_ist:
            label = f"⚡ Yesterday ({date_str}) — {len(by_date[date_str])} solved"
            is_open = ""
        else:
            label = f"📌 {date_str} — {len(by_date[date_str])} solved"
            is_open = ""

        lines.extend([
            f"<details{is_open}>",
            f"<summary><b>{label}</b></summary>",
            "",
            "| Problem ID | Name | Difficulty | Solution Link |",
            "| :---: | :--- | :---: | :---: |",
        ])

        for item in by_date[date_str]:
            badges = []
            if item["has_cpp"]:
                badges.append(f"[C++]({item['cpp_path']})")
            if item["has_py"]:
                badges.append(f"[Python]({item['py_path']})")
            links = " \\| ".join(badges)
            diff_badge = format_difficulty_badge(item["difficulty"])
            lines.append(f"| `#{item['number']}` | [{item['title']}]({item['url']}) | {diff_badge} | {links} |")

        lines.extend(["", "</details>", ""])

    # Difficulty Accordions
    for section_title, tag, problem_list in [
        ("🟢 Easy Problems", "easy-problems", easy_problems),
        ("🟡 Medium Problems", "medium-problems", medium_problems),
        ("🔴 Hard Problems", "hard-problems", hard_problems),
    ]:
        lines.extend([
            "---",
            "",
            f"### {section_title}",
            f"<details>",
            f"<summary><b>View {section_title} ({len(problem_list)})</b></summary>",
            "",
            "| # | Title | Language Solutions | Solved Date |",
            "| :---: | :--- | :---: | :---: |",
        ])
        for p in problem_list:
            badges = []
            if p["has_cpp"]:
                badges.append(f"[C++]({p['cpp_path']})")
            if p["has_py"]:
                badges.append(f"[Python]({p['py_path']})")
            links = " \\| ".join(badges)
            lines.append(f"| {p['number']} | [{p['title']}]({p['url']}) | {links} | {p['date_solved']} |")
        lines.extend(["", "</details>", ""])

    # Full Master Index
    lines.extend([
        "---",
        "",
        "### 📖 All Solutions Index",
        "",
        "<details>",
        "<summary><b>Click to expand full repository table</b></summary>",
        "",
        "| # | Problem Title | Difficulty | Available Implementations | First Solved |",
        "| :---: | :--- | :---: | :---: | :---: |",
    ])

    for p in problems_by_number:
        badges = []
        if p["has_cpp"]:
            badges.append(f"[C++]({p['cpp_path']})")
        if p["has_py"]:
            badges.append(f"[Python]({p['py_path']})")
        solution_links = " \\| ".join(badges)
        diff_badge = format_difficulty_badge(p["difficulty"])
        lines.append(f"| {p['number']} | [{p['title']}]({p['url']}) | {diff_badge} | {solution_links} | {p['date_solved']} |")

    lines.extend([
        "",
        "</details>",
        "",
        f"*Synced automatically (Scheduled daily at 06:00 AM IST & on code push).* ",
        END_MARKER,
    ])

    return "\n".join(lines)


def update_readme(readme_path: Path, stats_markdown: str):
    if not readme_path.exists():
        print(f"Error: {readme_path} not found.")
        sys.exit(1)

    content = readme_path.read_text(encoding="utf-8")

    if START_MARKER not in content or END_MARKER not in content:
        print(f"Error: Sentinel markers '{START_MARKER}' or '{END_MARKER}' not found.")
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
    print("README.md updated successfully with interactive metrics.")
    return True


def main():
    root = Path(__file__).resolve().parent.parent
    readme_file = root / "README.md"

    problems = parse_repository(root)
    stats_md = build_markdown_stats(problems)
    update_readme(readme_file, stats_md)


if __name__ == "__main__":
    main()
