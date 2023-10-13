import argparse
import requests
import sys

# Define the Wayback Machine API URL
wayback_api_url = "https://web.archive.org/cdx/search/cdx"

# Custom banner for Paramine
banner = """
 ____                 __  __ _            
|  _ \ __ _ _ __ __ _|  \/  (_)_ __   ___ 
| |_) / _` | '__/ _` | |\/| | | '_ \ / _ \
|  __/ (_| | | | (_| | |  | | | | | |  __/
|_|   \__,_|_|  \__,_|_|  |_|_|_| |_|\___|
	
1.0.0			adrianalvird
"""


# Function to fetch and process data for a subdomain
def fetch_subdomain_data(subdomain, output_file, silent):
    try:
        params = {
            'url': f"{subdomain}/*",
            'output': 'json'
        }

        response = requests.get(wayback_api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            extracted_urls = [entry[2] for entry in data]  # Adjust this index based on the API response structure
            if not silent:
                for url in extracted_urls:
                    print(url)
            if output_file:
                with open(output_file, "a") as file:
                    file.write("\n".join(extracted_urls) + "\n")
        elif not silent:
            print(f"Failed to fetch data for subdomain: {subdomain}")
    except KeyboardInterrupt:
        sys.exit(0)

# Create an argument parser
parser = argparse.ArgumentParser(description="Custom Subdomain URL Extraction Tool")

# Define command-line arguments
parser.add_argument('-u', '--url', help="Specify a single subdomain URL")
parser.add_argument('-f', '--file', help="Specify a file containing a list of subdomains")
parser.add_argument('-p', '--pipe', action="store_true", help="Read subdomains from standard input")
parser.add_argument('-o', '--output', help="Specify an output file for saving extracted URLs")
parser.add_argument('--silent', action="store_true", help="Enable silent mode (no output to the terminal)")

# Parse the command-line arguments
args = parser.parse_args()

# Print the custom banner
print(banner)

# Check and process the selected option
try:
    if args.url:
        fetch_subdomain_data(args.url, args.output, args.silent)
    elif args.file:
        with open(args.file, "r") as subdomains_file:
            subdomains = subdomains_file.read().splitlines()
            for subdomain in subdomains:
                fetch_subdomain_data(subdomain, args.output, args.silent)
    elif args.pipe:
        processed_subdomains = set()
        for line in sys.stdin:
            line = line.strip()
            if line not in processed_subdomains:
                fetch_subdomain_data(line, args.output, args.silent)
                processed_subdomains.add(line)
except KeyboardInterrupt:
    sys.exit(0)

