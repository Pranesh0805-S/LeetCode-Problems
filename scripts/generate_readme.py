from pathlib import Path
import re


README_FILE = Path("README.md")

START_MARKER = "<!-- LEETCODE-STATS:START -->"
END_MARKER = "<!-- LEETCODE-STATS:END -->"


def get_problems():
    problems = []

    for directory in Path(".").iterdir():
        if not directory.is_dir():
            continue

        match = re.match(r"^(\d+)-(.+)$", directory.name)

        if not match:
            continue

        problem_number = int(match.group(1))
        problem_name = match.group(2).replace("-", " ")

        cpp_file = directory / "solution.cpp"
        python_file = directory / "solution.py"

        problems.append({
            "number": problem_number,
            "name": problem_name,
            "cpp": cpp_file.exists(),
            "python": python_file.exists(),
        })

    return sorted(problems, key=lambda x: x["number"])


def generate_stats(problems):
    cpp_count = sum(problem["cpp"] for problem in problems)
    python_count = sum(problem["python"] for problem in problems)

    both_count = sum(
        problem["cpp"] and problem["python"]
        for problem in problems
    )

    cpp_only = sum(
        problem["cpp"] and not problem["python"]
        for problem in problems
    )

    python_only = sum(
        problem["python"] and not problem["cpp"]
        for problem in problems
    )

    lines = [
        "### 📈 Progress",
        "",
        "| Language | Solved |",
        "|---|---:|",
        f"| ⚡ C++ | {cpp_count} |",
        f"| 🐍 Python | {python_count} |",
        "",
        f"**Total unique problems:** {len(problems)}",
        "",
        "### 💻 Language Coverage",
        "",
        "| Category | Count |",
        "|---|---:|",
        f"| Both C++ & Python | {both_count} |",
        f"| C++ only | {cpp_only} |",
        f"| Python only | {python_only} |",
        "",
        "### 📚 Solved Problems",
        "",
        "| # | Problem | C++ | Python |",
        "|---:|---|:---:|:---:|",
    ]

    for problem in problems:
        number = problem["number"]
        name = problem["name"]
        folder = f"{number:04d}-{'-'.join(name.split())}"

        cpp = (
            f"[✅](./{folder}/solution.cpp)"
            if problem["cpp"]
            else "—"
        )

        python = (
            f"[✅](./{folder}/solution.py)"
            if problem["python"]
            else "—"
        )

        lines.append(
            f"| {number} | {name} | {cpp} | {python} |"
        )

    return "\n".join(lines)


def update_readme():
    if not README_FILE.exists():
        raise FileNotFoundError("README.md was not found.")

    readme = README_FILE.read_text(encoding="utf-8")

    if START_MARKER not in readme or END_MARKER not in readme:
        raise ValueError(
            "README.md is missing LEETCODE-STATS markers."
        )

    problems = get_problems()

    stats = generate_stats(problems)

    replacement = (
        START_MARKER
        + "\n"
        + stats
        + "\n"
        + END_MARKER
    )

    pattern = re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER)

    updated_readme = re.sub(
        pattern,
        replacement,
        readme,
        flags=re.DOTALL,
    )

    README_FILE.write_text(
        updated_readme,
        encoding="utf-8"
    )

    print(
        f"README updated successfully. "
        f"Found {len(problems)} unique problems."
    )


if __name__ == "__main__":
    update_readme()
