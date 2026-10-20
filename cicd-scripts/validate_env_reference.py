import pathlib
import sys

MAPPING_FILE = pathlib.Path("cicd-scripts/env-mapping.txt")
SCAN_DIRS = ["src", "resources"]
SCAN_SUFFIXES = {".py", ".sql", ".ipynb", ".yml", ".yaml", ".json"}


def load_dev_values():
    values = []
    for line in MAPPING_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        values.append(line.split("=", 1)[0].strip())
    return values


def main():
    dev_values = load_dev_values()
    failures = []
    for folder in SCAN_DIRS:
        for path in pathlib.Path(folder).rglob("*"):
            if not (path.is_file() and path.suffix in SCAN_SUFFIXES):
                continue
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                for dev in dev_values:
                    if dev in line:
                        failures.append(f"{path}:{lineno}: contains '{dev}'")
    if failures:
        print("Dev references found:")
        print("\n".join(failures))
        sys.exit(1)
    print("No dev references found.")


if __name__ == "__main__":
    main()