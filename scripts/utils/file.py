import json
import os


def clean_key(key: str) -> str:
    key = key.replace("-", " ").replace("_", " ").replace(".", " ").strip()
    key = " ".join(key.split())
    return key.strip().lower().replace(" ", "_")


def read_file(file_path: str) -> str:
    if not file_path:
        raise ValueError("file_path is required")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"file not found: {file_path}")

    with open(file_path, "r") as file:
        return file.read()


def write_file(file_path: str, data: str):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if not file_path:
        raise ValueError("file_path is required")
    if not data:
        raise ValueError("data is required")

    with open(file_path, "w") as file:
        file.write(data)
    print(f"Data saved to {file_path}")


def parse_file_data(data: str) -> dict:
    if not data:
        raise ValueError("data is required")

    parsed_data = {}
    sections = [d.strip() for d in data.lower().split("***") if d.strip()]
    for s in sections:
        section_name = clean_key(s.split("\n")[0][1:])
        parsed_data[section_name] = {}
        keys = []
        for line in s.split("\n")[1:]:
            line = line.replace("*", "").replace("\t", " ").strip().lower()
            if not line:
                continue

            if "#" in line:
                keys = []
                for v in line.strip().split(" "):
                    key = clean_key(v).replace("#", "")
                    if key and key not in keys:
                        keys.append(key)
                        parsed_data[section_name][key] = []
            elif ":" in line:
                key, val = map(clean_key, line.strip().split(":"))
                val = val.strip().replace("_", " ").split(" ")[0]
                parsed_data[section_name][key] = val
            elif len(keys) > 0:
                parsed_line = [v.strip() for v in line.strip().split(" ") if v.strip()]
                keys = list(parsed_data[section_name].keys())
                for i, val in enumerate(parsed_line):
                    if i == len(keys) - 1 and len(parsed_line) != len(keys):
                        parsed_data[section_name][keys[i]].append(parsed_line[i:])
                        break
                    parsed_data[section_name][keys[i]].append(val)
    return parsed_data


def get_file_data(file_path: str, save: bool = False) -> dict:
    file_data = read_file(file_path)
    data = parse_file_data(file_data)
    if save:
        file_path = os.path.join("data", f"{os.path.basename(file_path)}.json")
        write_file(file_path, json.dumps(data, indent=2))
    return data
