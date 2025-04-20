from email_validation import validate_emails_from_dict, catchall_to_valid
from email_generator import generate_email_addresses_from_data
from typing import Dict, List

def process_email_pipeline(leads_data: List[Dict]) -> List[Dict]:
    """
    Complete pipeline for email processing:
    1. Generate email patterns
    2. Validate emails using ZeroBounce
    3. Filter and promote catch-all emails
    
    Args:
        leads_data (List[Dict]): List of dictionaries containing lead information:
            {
                'lead_name': str,
                'lead_id': str,
                'company_website': str
            }
    
    Returns:
        List[Dict]: List of dictionaries containing processed lead information:
            {
                'lead_name': str,
                'lead_id': str,
                'company_website': str,
                'probable_emails': List[str],
                'valid_emails': List[str],
                'catch_all_emails': List[str],
                'smtp_test': List[str]
            }
    """
    # Step 1: Generate email patterns
    print("\nStep 1: Generating email patterns...")
    generated_emails = generate_email_addresses_from_data(leads_data)
    
    # Step 2: Validate emails using ZeroBounce
    print("\nStep 2: Validating emails with ZeroBounce...")
    validated_emails = validate_emails_from_dict(generated_emails)
    
    # Step 3: Filter and promote catch-all emails
    print("\nStep 3: Filtering and promoting catch-all emails...")
    final_results = catchall_to_valid(validated_emails)
    
    return final_results

# Example usage
if __name__ == "__main__":
    # Example input
    input_data = [
        {
            'lead_name': 'Akshat Singh',
            'lead_id': 'LLD03',
            'company_website': 'https://www.panscience.xyz/'
        },
        {
            'lead_name': 'Anshul V. Pandey, PhD',
            'lead_id': 'LLD01',
            'company_website': 'https://www.panscience.xyz/'
        },
        {
            'lead_name': 'Dr. Tanisha Singh, PhD',
            'lead_id': 'LLD05',
            'company_website': 'https://www.panscience.xyz/'
        }
    ]
    
    # Process the pipeline
    results = process_email_pipeline(input_data)
    
    # Print results
    print("\nFinal Results:")
    print(results)
