import pathlib
import sys

MAPPING_FILE = pathlib.Path("cicd-scripts/env-mapping.txt")
DEV_VALUES_FILE = pathlib.Path("cicd-scripts/dev-values.txt")
SCAN_DIRS = ["src", "resources"]
SCAN_SUFFIXES = {".py", ".sql", ".ipynb", ".yml", ".yaml", ".json"}


def read_entries(path):
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            entries.append(line)
    return entries


def main():
    dev_values = read_entries(DEV_VALUES_FILE)
    mapped = {entry.split("=", 1)[0].strip() for entry in read_entries(MAPPING_FILE)}
    problems = []

    for dev in dev_values:
        if dev not in mapped:
            problems.append(f"no mapping line for '{dev}' in env-mapping.txt")

    for folder in SCAN_DIRS:
        for path in pathlib.Path(folder).rglob("*"):
            if not (path.is_file() and path.suffix in SCAN_SUFFIXES):
                continue
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                for dev in dev_values:
                    if dev in line:
                        problems.append(f"{path}:{lineno}: contains '{dev}'")

    if problems:
        print("Environment reference check failed:")
        print("\n".join(problems))
        sys.exit(1)
    print("No dev references found.")


if __name__ == "__main__":
    main()