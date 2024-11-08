#!/usr/bin/env python3

import requests
import re
import subprocess
import json
from prompt_toolkit import prompt

def get_domains_from_crtsh(domain):
    """Fetches subdomains for a given domain from crt.sh."""
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        subdomains = {entry['name_value'] for entry in data if 'name_value' in entry}
        valid_subdomains = sorted([sub for sub in subdomains if re.match(r"^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$", sub)])

        return valid_subdomains

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching subdomains for {domain}: {e}")
        return []

def get_base_domains_from_hackerone():
    """Fetches domains from the HackerOne data JSON."""
    url = "https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/refs/heads/main/data/hackerone_data.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        base_domains = {target['asset_identifier'].lstrip("*.") for program in data for target in program.get('targets', {}).get('in_scope', []) if 'asset_identifier' in target}
        valid_base_domains = sorted([domain for domain in base_domains if re.match(r"^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$", domain)])

        return valid_base_domains

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def gather_all_domains():
    """Combines base domains from HackerOne with subdomains from crt.sh and saves them to domain.txt."""
    all_domains = set()
    
    base_domains = get_base_domains_from_hackerone()
    for domain in base_domains:
        print(f"Fetching subdomains for {domain}...")
        subdomains = get_domains_from_crtsh(domain)
        all_domains.update(subdomains)

    # Write all unique domains to domain.txt
    with open("domain.txt", "w") as file:
        for domain in sorted(all_domains):
            file.write(f"{domain}\n")

    print(f"Saved {len(all_domains)} domains and subdomains in domain.txt.")
    return all_domains

def run_nuclei_scan():
    try:
        subprocess.run(["nuclei", "-l", "domain.txt", "-o", "nuclei_results.txt"], check=True)
        print("Nuclei scan completed. Results saved in nuclei_results.txt.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Nuclei: {e}")

if __name__ == "__main__":
    # Prompt user to choose the source of domains
    choice = prompt("Type 'hackerone' to use HackerOne data and gather subdomains: ").strip().lower()

    if choice == 'hackerone':
        gather_all_domains()
    else:
        print("Invalid option. Exiting.")

    run_nuclei_scan()

