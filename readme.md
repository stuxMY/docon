Docon

Docon is a Python script designed to fetch subdomains of a given domain from crt.sh, validate them, and then run a Nuclei scan to find potential vulnerabilities.
Features

    Fetches subdomains for a specified base domain using crt.sh.
    Validates and filters the retrieved subdomains.
    Saves subdomains in a domain.txt file.
    Runs a Nuclei scan on the list of subdomains and saves the results in nuclei_results.txt.

Prerequisites
1. Python 3

Ensure Python 3 is installed on your system.
2. Required Python Libraries

Install the necessary Python package:

bash

pip install requests

3. Nuclei

Install Nuclei, a vulnerability scanner:

bash

go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

Usage

    Clone this repository: https://github.com/stuxMY/docon.git

git clone https://github.com/stuxMY/docon.git
cd docon

Make the script executable:
chmod +x docon.py

Run the script and provide a domain when prompted:

    ./docon.py

    Enter the domain to analyze (e.g., example.com).

    View Results:
        The subdomains are saved in domain.txt.
        The Nuclei scan results are saved in nuclei_results.txt.

Example

plaintext

Domain : > example.com
Saved 150 domains and subdomains for example.com in domain.txt.
Nuclei scan completed. Results saved in nuclei_results.txt.

Script Overview

    get_domains(base_domain): Fetches subdomains for base_domain from crt.sh, validates them, and saves them to domain.txt.
    run_nuclei_scan(): Runs a Nuclei scan using domain.txt as input and saves results to nuclei_results.txt.
