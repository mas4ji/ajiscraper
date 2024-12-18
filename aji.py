import requests
from requests.exceptions import RequestException, ConnectionError, Timeout
from urllib3.exceptions import NewConnectionError, MaxRetryError, NameResolutionError
from bs4 import BeautifulSoup
import os
import argparse
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# List of social media platforms
SOCIAL_MEDIA = {
    "facebook": "facebook.com",
    "instagram": "instagram.com",
    "twitter": "twitter.com",
    "linkedin": "linkedin.com",
    "youtube": "youtube.com"
}

def format_url(url):
    """Add http:// if URL doesn't have a protocol."""
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    return url

def print_header():
    ascii_art = r"""
        _     _ _   ____                             
   / \   (_|_) / ___|  ___ _ __ __ _ _ __   ___ 
  / _ \  | | | \___ \ / __| '__/ _` | '_ \ / _ \
 / ___ \ | | |  ___) | (__| | | (_| | |_) |  __/
 /_/   \_\/ |_| |____/ \___|_|  \__,_| .__/ \___|
       |__/                         |_|          
   Aji Scrape - Scrape and Check Social Media Links for Broken Links on Websites
    """
    print(Fore.GREEN + ascii_art)
    print(Fore.YELLOW + "Usage:")
    print("  -d, --domain   Scrape single domain (e.g., example.com or https://example.com)")
    print("  -f, --file     Scrape multiple domains from a file")
    print("  -o, --output   Output file to save results (default: social_links.txt)")
    print("  -p, --proxy    Use a proxy for requests (e.g., http://127.0.0.1:8080)")

def is_user_active(url):
    """Check if the social media account is active or not."""
    try:
        response = requests.get(url, timeout=10)
        
        # Check for HTTP status codes
        if response.status_code == 404:
            return False
        if response.status_code == 403 or response.status_code == 500:
            return False
        if "user not found" in response.text.lower() or "page not found" in response.text.lower():
            return False
        if "Sorry, this page isn't available" in response.text or "User not found" in response.text:
            return False
        
        return True  # The account is active if no issues were found
    except NameResolutionError:
        print(Fore.BLUE + f"[ERROR] Unable to access {url}: DNS Error (Could not resolve hostname).")
        return False
    except MaxRetryError:
        print(Fore.BLUE + f"[ERROR] Unable to access {url}: Max retries exceeded (Temporary DNS failure).")
        return False
    except NewConnectionError:
        print(Fore.BLUE + f"[ERROR] Unable to access {url}: DNS Error (Failed to establish a new connection).")
        return False
    except ConnectionError:
        print(Fore.BLUE + f"[ERROR] Unable to access {url}: Connection error (Server may be down or unreachable).")
        return False
    except Timeout:
        print(Fore.BLUE + f"[ERROR] Unable to access {url}: Timeout error (Server took too long to respond).")
        return False
    except RequestException as e:
        print(Fore.BLUE + f"[ERROR] Unable to access {url}: Website ERROR ({e}).")
        return False

def scrape_social_links(url, result_file, proxy=None):
    try:
        url = format_url(url)

        # Setup proxy if provided
        proxies = {"http": proxy, "https": proxy} if proxy else None
        try:
            response = requests.get(url, timeout=10, proxies=proxies)
            response.raise_for_status()
        except (RequestException, ConnectionError, Timeout, NameResolutionError, MaxRetryError, NewConnectionError):
            print(Fore.BLUE + f"[ERROR] Unable to access {url}: Website ERROR")
            return  # Skip the processing if the website is not accessible
        
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all <a> tags with href
        links = soup.find_all("a", href=True)
        social_links = {}

        for link in links:
            href = link["href"]
            for platform, domain in SOCIAL_MEDIA.items():
                if domain in href:
                    if platform not in social_links:
                        social_links[platform] = []
                    social_links[platform].append(href)
        
        # Write the results to the output file
        with open(result_file, "a") as f:
            f.write(f"{url}\n")  # Domain name at the top
            if social_links:
                print(Fore.GREEN + f"[INFO] Found social media links on {url}:")
                for platform, urls in social_links.items():
                    for social_url in set(urls):  # Remove duplicates
                        # Check if the account is active and provide 'vulnerable' or 'not vulnerable'
                        if platform == "instagram":
                            if is_user_active(social_url):
                                f.write(f"  - {platform.capitalize()}: {social_url} [Potential Vulnerable]\n")
                                print(Fore.YELLOW + f"  - {platform.capitalize()}: {social_url} [Potential Vulnerable]")
                            else:
                                f.write(f"  - {platform.capitalize()}: {social_url} [Vulnerable]\n")
                                print(Fore.RED + f"  - {platform.capitalize()}: {social_url} [Vulnerable]")
                        else:
                            if is_user_active(social_url):
                                f.write(f"  - {platform.capitalize()}: {social_url} [Not Vulnerable]\n")
                                print(Fore.GREEN + f"  - {platform.capitalize()}: {social_url} [Not Vulnerable]")
                            else:
                                f.write(f"  - {platform.capitalize()}: {social_url} [Vulnerable]\n")
                                print(Fore.RED + f"  - {platform.capitalize()}: {social_url} [Vulnerable]")
            else:
                print(Fore.RED + f"[INFO] No social media links found on {url}.")
                f.write("  No social media links found.\n")
            f.write("\n")  # Add an empty line for separation
    except Exception as e:
        print(Fore.BLUE + f"[ERROR] Unknown error occurred while accessing {url}: {e}.")
    
def scrape_from_file(file_path, result_file, proxy=None):
    if not os.path.exists(file_path):
        print(Fore.BLUE + f"[ERROR] File {file_path} not found!")
        return
    
    with open(file_path, "r") as f:
        domains = f.read().splitlines()
        for domain in domains:
            scrape_social_links(domain.strip(), result_file, proxy)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape social media links from websites.")
    parser.add_argument("-d", "--domain", help="Single domain to scrape.")
    parser.add_argument("-f", "--file", help="File containing list of domains (one per line).")
    parser.add_argument("-o", "--output", help="Output file for saving results.", default="social_links.txt")
    parser.add_argument("-p", "--proxy", help="Use a proxy for requests (e.g., http://127.0.0.1:8080).", default=None)
    args = parser.parse_args()

    # Show the header if no valid arguments are provided
    if not (args.domain or args.file):
        print_header()
    else:
        # Delete the output file if it already exists (so we always start fresh)
        if os.path.exists(args.output):
            os.remove(args.output)

        if args.domain:
            scrape_social_links(args.domain, args.output, args.proxy)
        elif args.file:
            scrape_from_file(args.file, args.output, args.proxy)
