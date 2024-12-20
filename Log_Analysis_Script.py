
import re
import csv
from collections import Counter
from tabulate import tabulate

# Configurable parameters
LOG_FILE = "/content/sample.log"  # Path to the log file
FAILED_LOGIN_INDICATOR = "401"
FAILED_LOGIN_THRESHOLD = 3  # Threshold for suspicious login attempts
OUTPUT_CSV = "log_analysis_results.csv"

def parse_log_file(file_path):
    """Parses the log file and extracts required information."""
    ip_requests = Counter()
    endpoint_requests = Counter()
    failed_logins = Counter()

    # Regular expression for log parsing
    log_pattern = re.compile(
        r'(?P<ip>[\d\.]+) - - \[.*\] "(?P<method>\S+) (?P<endpoint>\S+) .*" (?P<status>\d+) .*'
    )

    with open(file_path, "r") as file:
        for line in file:
            match = log_pattern.match(line)
            if match:
                ip = match.group("ip")
                endpoint = match.group("endpoint")
                status = match.group("status")

                # Count IP requests
                ip_requests[ip] += 1

                # Count endpoint requests
                endpoint_requests[endpoint] += 1

                # Track failed login attempts
                if status == FAILED_LOGIN_INDICATOR and endpoint == "/login":
                    failed_logins[ip] += 1

    return ip_requests, endpoint_requests, failed_logins

def write_to_csv(ip_requests_sorted, most_accessed_endpoint, failed_logins, output_file):
    """Writes the results to a CSV file."""
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Write IP requests
        writer.writerow(["Requests per IP Address"])
        writer.writerow(["IP Address", "Request Count"])
        for ip, count in ip_requests_sorted:  # Loop through sorted list
            writer.writerow([ip, count])

        writer.writerow([])

        # Write most accessed endpoint
        writer.writerow(["Most Frequently Accessed Endpoint"])
        writer.writerow(["Endpoint", "Access Count"])
        writer.writerow([most_accessed_endpoint[0], most_accessed_endpoint[1]])

        writer.writerow([])

        # Write suspicious activity
        writer.writerow(["Suspicious Activity Detected"])
        writer.writerow(["IP Address", "Failed Login Attempts"])
        for ip, count in failed_logins.items():
            if count > FAILED_LOGIN_THRESHOLD:
                writer.writerow([ip, count])

def main():
    # Parse the log file
    try:
        ip_requests, endpoint_requests, failed_logins = parse_log_file(LOG_FILE)

        # Sort IP requests by count
        sorted_ip_requests = sorted(ip_requests.items(), key=lambda x: x[1], reverse=True)

        # Find the most accessed endpoint
        most_accessed_endpoint = endpoint_requests.most_common(1)[0]

        # Detect suspicious activity
        suspicious_ips = {ip: count for ip, count in failed_logins.items() if count > FAILED_LOGIN_THRESHOLD}

        # Display results as tables
        print("\nRequests per IP Address:")
        print(tabulate(sorted_ip_requests, headers=["IP Address", "Request Count"], tablefmt="grid"))

        print("\nMost Frequently Accessed Endpoint:")
        print(tabulate([most_accessed_endpoint], headers=["Endpoint", "Access Count"], tablefmt="grid"))

        print("\nSuspicious Activity Detected:")
        print(tabulate(
            suspicious_ips.items(),
            headers=["IP Address", "Failed Login Attempts"],
            tablefmt="grid",
        ))

        # Write results to CSV
        write_to_csv(sorted_ip_requests, most_accessed_endpoint, suspicious_ips, OUTPUT_CSV)
        print(f"\nResults have been saved to {OUTPUT_CSV}")

    except FileNotFoundError:
        print(f"Error: File '{LOG_FILE}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

