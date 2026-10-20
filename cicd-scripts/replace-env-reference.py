import pathlib

MAPPING_FILE = pathlib.Path("cicd-scripts/env-mapping.txt")
SCAN_DIRS = ["src", "resources"]  # databricks.yml is excluded on purpose
SCAN_SUFFIXES = {".py", ".sql", ".ipynb", ".yml", ".yaml", ".json"}


def load_mapping():
    pairs = []
    for line in MAPPING_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        dev, prod = line.split("=", 1)
        pairs.append((dev.strip(), prod.strip()))
    return pairs


def files_to_scan():
    for folder in SCAN_DIRS:
        for path in pathlib.Path(folder).rglob("*"):
            if path.is_file() and path.suffix in SCAN_SUFFIXES:
                yield path


def main():
    pairs = load_mapping()
    updated = 0
    for path in files_to_scan():
        text = path.read_text(encoding="utf-8")
        new_text = text
        for dev, prod in pairs:
            new_text = new_text.replace(dev, prod)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print(f"updated {path}")
            updated += 1
    print(f"{updated} file(s) updated")


if __name__ == "__main__":
    main()