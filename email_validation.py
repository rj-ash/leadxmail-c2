from zerobouncesdk import ZeroBounce, ZBException, ZBValidateBatchElement, ZBValidateStatus
from typing import Dict, List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def validate_emails_from_dict(leads_data: List[Dict]) -> List[Dict]:
    """
    Validates emails for multiple leads with proper error handling and response mapping.
    """
    if not leads_data:
        return []

    # Initialize ZeroBounce client
    zero_bounce = ZeroBounce(os.getenv("ZEROBOUNCE_API_KEY"))
    
    # Validate lead data structure and create email mapping
    email_to_lead = {}
    flattened_emails = []
    
    for lead in leads_data:
        if not all(key in lead for key in ['lead_id', 'probable_emails']):
            print(f"Skipping invalid lead entry: {lead.get('lead_name', 'Unnamed lead')}")
            continue
            
        for email in lead['probable_emails']:
            if email not in email_to_lead:
                email_to_lead[email] = lead['lead_id']
                flattened_emails.append(email)

    # Initialize result storage
    results = {lead['lead_id']: {
        'lead_name': lead['lead_name'],
        'lead_id': lead['lead_id'],
        'company_website': lead.get('company_website', ''),
        'probable_emails': lead['probable_emails'],
        'valid_emails': set(),
        'catch_all_emails': set()
    } for lead in leads_data if 'lead_id' in lead}

    # Process emails in API-compliant batches
    for i in range(0, len(flattened_emails), 170):
        chunk = flattened_emails[i:i+170]
        print(f"\nProcessing chunk {i//170 + 1} ({len(chunk)} emails)...")

        try:
            response = zero_bounce.validate_batch(
                [ZBValidateBatchElement(email) for email in chunk]
            )
            
            # Process results using actual email addresses from response
            for email_result in response.email_batch:
                email = email_result.address
                lead_id = email_to_lead.get(email)

                if not lead_id:
                    continue  # Skip emails not mapped to any lead

                if email_result.status == ZBValidateStatus.valid:
                    results[lead_id]['valid_emails'].add(email)
                    print(f"Valid: {email}")
                elif email_result.status == ZBValidateStatus.catch_all:
                    results[lead_id]['catch_all_emails'].add(email)
                    print(f"Catch-all: {email}")

        except ZBException as e:
            print(f"API Error: {str(e)}")
            continue

    # Convert sets to sorted lists and add smtp_test field
    final_results = []
    for lead in results.values():
        lead['valid_emails'] = sorted(lead['valid_emails'])
        lead['catch_all_emails'] = sorted(lead['catch_all_emails'])
        lead['smtp_test'] = lead['catch_all_emails'].copy()
        final_results.append(lead)

    return final_results

def catchall_to_valid(input_data: List[Dict]) -> List[Dict]:
    """
    Promotes catch-all emails to valid when no valid emails exist,
    preserving the original email order but limiting to 10 entries.
    """
    for entry in input_data:
        if not entry['valid_emails']:
            # Maintain original order but filter to probable_emails that are in catch-all
            valid_catchalls = [email for email in entry['probable_emails'] 
                             if email in entry['catch_all_emails']][:10]
            entry['valid_emails'] = valid_catchalls
    return input_data


    
    # Validate emails and process results


input = [{'lead_name': 'Akshat Singh', 'lead_id': 'LLD03', 'company_website': 'https://www.panscience.xyz/', 'probable_emails': ['s.a@panscience.xyz', 's_a@panscience.xyz', 'a_s@panscience.xyz', 'singha@panscience.xyz', 'akshat_s@panscience.xyz', 'singh_akshat@panscience.xyz', 's_akshat@panscience.xyz', 'akshats@panscience.xyz', 'akshat_singh@panscience.xyz', 'singh_a@panscience.xyz', 'akshat.s@panscience.xyz', 'sa@panscience.xyz', 'singh.akshat@panscience.xyz', 'singh.a@panscience.xyz', 's.akshat@panscience.xyz', 'sakshat@panscience.xyz', 'akshat.singh@panscience.xyz', 'asingh@panscience.xyz', 'a.singh@panscience.xyz', 'a.s@panscience.xyz', 'akshat@panscience.xyz', 'as@panscience.xyz', 'singh@panscience.xyz', 'singhakshat@panscience.xyz', 'a_singh@panscience.xyz', 'akshatsingh@panscience.xyz']}, {'lead_name': 'Anshul V. Pandey, PhD', 'lead_id': 'LLD04', 'company_website': 'https://www.panscience.xyz/', 'probable_emails': ['anshul@panscience.xyz', 'pandey.a@panscience.xyz', 'a_pandey@panscience.xyz', 'anshul.pandey@panscience.xyz', 'p_a@panscience.xyz', 'pa@panscience.xyz', 'pandeyanshul@panscience.xyz', 'panshul@panscience.xyz', 'pandey@panscience.xyz', 'anshul_pandey@panscience.xyz', 'anshul.p@panscience.xyz', 'anshul_p@panscience.xyz', 'p.a@panscience.xyz', 'anshulp@panscience.xyz', 'p.anshul@panscience.xyz', 'anshulpandey@panscience.xyz', 'apandey@panscience.xyz', 'pandeya@panscience.xyz', 'p_anshul@panscience.xyz', 'a_p@panscience.xyz', 'a.p@panscience.xyz', 'pandey_anshul@panscience.xyz', 'ap@panscience.xyz', 'a.pandey@panscience.xyz', 'pandey_a@panscience.xyz', 'pandey.anshul@panscience.xyz']}, {'lead_name': 'Tanisha Singh, PhD', 'lead_id': 'LLD05', 'company_website': 'https://www.panscience.xyz/', 'probable_emails': ['singh.tanisha@panscience.xyz', 'tanisha.singh@panscience.xyz', 's.tanisha@panscience.xyz', 'tanishas@panscience.xyz', 't.singh@panscience.xyz', 'stanisha@panscience.xyz', 'singht@panscience.xyz', 'tanishasingh@panscience.xyz', 'tsingh@panscience.xyz', 'singh_t@panscience.xyz', 'tanisha.s@panscience.xyz', 'singh.t@panscience.xyz', 't_s@panscience.xyz', 'singhtanisha@panscience.xyz', 'singh_tanisha@panscience.xyz', 'tanisha_s@panscience.xyz', 'ts@panscience.xyz', 'tanisha@panscience.xyz', 't_singh@panscience.xyz', 'tanisha_singh@panscience.xyz', 's_t@panscience.xyz', 's_tanisha@panscience.xyz', 'st@panscience.xyz', 's.t@panscience.xyz', 'singh@panscience.xyz', 't.s@panscience.xyz']}]

zerobounce_validation = [{'lead_name': 'Akshat Singh', 'lead_id': 'LLD03', 'company_website': 'https://www.panscience.xyz/', 'probable_emails': ['s.a@panscience.xyz', 's_a@panscience.xyz', 'a_s@panscience.xyz', 'singha@panscience.xyz', 'akshat_s@panscience.xyz', 'singh_akshat@panscience.xyz', 's_akshat@panscience.xyz', 'akshats@panscience.xyz', 'akshat_singh@panscience.xyz', 'singh_a@panscience.xyz', 'akshat.s@panscience.xyz', 'sa@panscience.xyz', 'singh.akshat@panscience.xyz', 'singh.a@panscience.xyz', 's.akshat@panscience.xyz', 'sakshat@panscience.xyz', 'akshat.singh@panscience.xyz', 'asingh@panscience.xyz', 'a.singh@panscience.xyz', 'a.s@panscience.xyz', 'akshat@panscience.xyz', 'as@panscience.xyz', 'singh@panscience.xyz', 'singhakshat@panscience.xyz', 'a_singh@panscience.xyz', 'akshatsingh@panscience.xyz'], 'valid_emails': [], 'catch_all_emails': ['a.s@panscience.xyz', 'a.singh@panscience.xyz', 'a_s@panscience.xyz', 'akshat.s@panscience.xyz', 'akshatsingh@panscience.xyz', 'asingh@panscience.xyz', 's.akshat@panscience.xyz', 'sakshat@panscience.xyz', 'singh_a@panscience.xyz'], 'smtp_test': ['a.s@panscience.xyz', 'a.singh@panscience.xyz', 'a_s@panscience.xyz', 'akshat.s@panscience.xyz', 'akshatsingh@panscience.xyz', 'asingh@panscience.xyz', 's.akshat@panscience.xyz', 'sakshat@panscience.xyz', 'singh_a@panscience.xyz']}, {'lead_name': 'Anshul V. Pandey, PhD', 'lead_id': 'LLD04', 'company_website': 'https://www.panscience.xyz/', 'probable_emails': ['anshul@panscience.xyz', 'pandey.a@panscience.xyz', 'a_pandey@panscience.xyz', 'anshul.pandey@panscience.xyz', 'p_a@panscience.xyz', 'pa@panscience.xyz', 'pandeyanshul@panscience.xyz', 'panshul@panscience.xyz', 'pandey@panscience.xyz', 'anshul_pandey@panscience.xyz', 'anshul.p@panscience.xyz', 'anshul_p@panscience.xyz', 'p.a@panscience.xyz', 'anshulp@panscience.xyz', 'p.anshul@panscience.xyz', 'anshulpandey@panscience.xyz', 'apandey@panscience.xyz', 'pandeya@panscience.xyz', 'p_anshul@panscience.xyz', 'a_p@panscience.xyz', 'a.p@panscience.xyz', 'pandey_anshul@panscience.xyz', 'ap@panscience.xyz', 'a.pandey@panscience.xyz', 'pandey_a@panscience.xyz', 'pandey.anshul@panscience.xyz'], 'valid_emails': ['anshul.pandey@panscience.xyz', 'anshul@panscience.xyz'], 'catch_all_emails': ['a.p@panscience.xyz', 'a.pandey@panscience.xyz', 'anshulpandey@panscience.xyz'], 'smtp_test': ['a.p@panscience.xyz', 'a.pandey@panscience.xyz', 'anshulpandey@panscience.xyz']}, {'lead_name': 'Tanisha Singh, PhD', 'lead_id': 'LLD05', 'company_website': 'https://www.panscience.xyz/', 'probable_emails': ['singh.tanisha@panscience.xyz', 'tanisha.singh@panscience.xyz', 's.tanisha@panscience.xyz', 'tanishas@panscience.xyz', 't.singh@panscience.xyz', 'stanisha@panscience.xyz', 'singht@panscience.xyz', 'tanishasingh@panscience.xyz', 'tsingh@panscience.xyz', 'singh_t@panscience.xyz', 'tanisha.s@panscience.xyz', 'singh.t@panscience.xyz', 't_s@panscience.xyz', 'singhtanisha@panscience.xyz', 'singh_tanisha@panscience.xyz', 'tanisha_s@panscience.xyz', 'ts@panscience.xyz', 'tanisha@panscience.xyz', 't_singh@panscience.xyz', 'tanisha_singh@panscience.xyz', 's_t@panscience.xyz', 's_tanisha@panscience.xyz', 'st@panscience.xyz', 's.t@panscience.xyz', 'singh@panscience.xyz', 't.s@panscience.xyz'], 'valid_emails': ['tanisha@panscience.xyz', 'tanisha_s@panscience.xyz'], 'catch_all_emails': ['s_tanisha@panscience.xyz', 'singh.tanisha@panscience.xyz', 't.s@panscience.xyz', 't_s@panscience.xyz', 't_singh@panscience.xyz', 'tanisha_singh@panscience.xyz'], 'smtp_test': ['s_tanisha@panscience.xyz', 'singh.tanisha@panscience.xyz', 't.s@panscience.xyz', 't_s@panscience.xyz', 't_singh@panscience.xyz', 'tanisha_singh@panscience.xyz']}]

filtered_data = catchall_to_valid(zerobounce_validation)
print(filtered_data)


