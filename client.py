import requests
import time
import json
from typing import Dict, List
import argparse

def process_emails(api_url: str, leads: List[Dict]) -> Dict:
    """
    Process emails and wait for results
    
    Args:
        api_url: Base URL of the API
        leads: List of leads to process
    
    Returns:
        Dictionary containing the processing results
    """
    # Make the initial request
    response = requests.post(
        f"{api_url}/process-emails",
        json=leads,
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    data = response.json()
    
    # Get the request ID
    request_id = data["request_id"]
    print(f"Processing started. Request ID: {request_id}")
    print("Waiting for results...")
    
    # Poll for results
    while True:
        status_response = requests.get(f"{api_url}/status/{request_id}")
        status_response.raise_for_status()
        status_data = status_response.json()
        
        if status_data["status"] == "completed":
            print("\nProcessing completed!")
            return status_data["results"]
        elif status_data["status"] == "error":
            print(f"\nError: {status_data['error']}")
            return None
        else:
            print(".", end="", flush=True)
            time.sleep(2)  # Wait 2 seconds before polling again

def main():
    parser = argparse.ArgumentParser(description="Email Processing Client")
    parser.add_argument("--url", default="https://your-project.vercel.app", help="API URL")
    parser.add_argument("--file", help="JSON file containing leads")
    args = parser.parse_args()
    
    # Load leads from file or use default
    if args.file:
        with open(args.file, 'r') as f:
            leads = json.load(f)
    else:
        # Default test data
        leads = [
            {
                "lead_name": "Akshat Singh",
                "lead_id": "LLD03",
                "company_website": "https://www.panscience.xyz/"
            }
        ]
    
    try:
        results = process_emails(args.url, leads)
        if results:
            print("\nResults:")
            print(json.dumps(results, indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 