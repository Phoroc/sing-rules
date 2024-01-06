import math
import re
import requests
import json
import os

lists_hagezi = [
    ["hagezi-light", "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/light-onlydomains.txt"],
    ["hagezi-normal", "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/multi-onlydomains.txt"],
    ["hagezi-pro", "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/pro-onlydomains.txt"],
    ["hagezi-proplus", "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/pro.plus-onlydomains.txt"],
    ["hagezi-ultimate", "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/ultimate-onlydomains.txt"],
    ["hagezi-tif", "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/tif-onlydomains.txt"]
]

lists_1hosts = [
    ["1hosts-mini", "https://raw.githubusercontent.com/badmojr/1Hosts/master/mini/domains.wildcards"],
    ["1hosts-lite", "https://raw.githubusercontent.com/badmojr/1Hosts/master/Lite/domains.wildcards"],
    ["1hosts-pro", "https://raw.githubusercontent.com/badmojr/1Hosts/master/Pro/domains.wildcards"],
    ["1hosts-xtra", "https://raw.githubusercontent.com/badmojr/1Hosts/master/Xtra/domains.wildcards"]
]

output_dir = "./rule-set"


def convert_domains(list_info: list) -> str:
    r = requests.get(list_info[1])
    domain_list = []
    if r.status_code == 200:
        lines = r.text.splitlines()
        for line in lines:
            if not line.startswith("#") and line.strip():
                domain_list.append(line)
    result = {
        "version": 1,
        "rules": [
            {
                "domain_suffix": []
            }
        ]
    }
    result["rules"][0]["domain_suffix"] = domain_list
    filepath = os.path.join(output_dir, list_info[0] + ".json")
    with open(filepath, "w") as f:
        f.write(json.dumps(result, indent=2))
    return filepath


def main():
    files = []
    os.mkdir(output_dir)
    for ls in lists_hagezi:
        filepath = convert_domains(ls)
        files.append(filepath)
    for ls in lists_1hosts:
        filepath = convert_domains(ls)
        files.append(filepath)
    print("rule-set source generated:")
    for filepath in files:
        print(filepath)
    for filepath in files:
        srs_path = filepath.replace(".json", ".srs")
        os.system("sing-box rule-set compile --output " +
                  srs_path + " " + filepath)


if __name__ == "__main__":
    main()
