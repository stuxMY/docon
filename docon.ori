#!/usr/bin/env python3

import requests
import re
import subprocess
from prompt_toolkit import prompt

def get_domains(base_domain):
    url = f"https://crt.sh/?q=%25.{base_domain}&output=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        domains = {entry['name_value'] for entry in data if 'name_value' in entry}

        valid_domains = sorted([domain for domain in domains if re.match(r"^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$", domain)])

        with open("domain.txt", "w") as file:
            for domain in valid_domains:
                file.write(f"{domain}\n")

        print(f"Saved {len(valid_domains)} domains and subdomains for {base_domain} in domain.txt.")
        return valid_domains

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def run_nuclei_scan():
    try:
        subprocess.run(["nuclei", "-l", "domain.txt", "-o", "nuclei_results.txt"], check=True)
        print("Nuclei scan completed. Results saved in nuclei_results.txt.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Nuclei: {e}")

if __name__ == "__main__":
    # Use prompt() from prompt_toolkit to capture domain name
    base_domain = prompt("Domain : >  ").strip()
    get_domains(base_domain)
    run_nuclei_scan()

