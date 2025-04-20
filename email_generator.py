import warnings
import time
import re
from typing import List, Dict

warnings.filterwarnings("ignore", category=UserWarning)


def clean_name(full_name):

    full_name = re.sub(r"\s*\(.*?\)\s*", " ", full_name)
    if not full_name.strip():
        return []

    titles = [
    "",

    # General honorifics
    "mr", "mister", "mrs", "miss", "ms", "mx", "sir", "madam", "ma'am", "dame", "lady", "lord",

    # Academic and educational
    "dr", "doctor", "prof", "professor", "phd", "msc", "bsc", "ba", "ma", "bcom", "mcom",
    "mtech", "btech", "mphil", "bca", "mca", "bba", "mba", "pgdm", "pgdba",
    "bfa", "mfa", "bed", "med", "dphil",

    # Medical and healthcare
    "md", "dds", "dmd", "do", "mbbs", "bds", "bpt", "dpt", "bpharm", "dpharm",
    "dmlt", "rph", "dch", "ayur", "bams", "bhms", "nurse", "dcn",

    # Legal and judiciary
    "jd", "esq", "esquire", "llb", "llm", "adv", "advocate", "barrister", "solicitor",
    "justice", "judge", "magistrate",

    # Engineering and technical
    "eng", "engineer", "pe", "ce", "me", "eee", "ece", "cs", "cse", "it",
    "software engineer", "developer", "dev", "qa", "tester", "architect",
    "ml engineer", "ai engineer", "ai specialist", "data scientist", "data analyst",

    # Religious titles
    "rev", "reverend", "fr", "father", "sr", "sister", "br", "brother",

    # Military and defense
    "capt", "captain", "lt", "lieutenant", "col", "colonel", "gen", "general",
    "cmdr", "commander", "maj", "major", "sgt", "sergeant", "adm", "admiral",
    "air cmde", "air commodore", "marshal",

    # Government and honorary
    "hon", "honourable", "mp", "mla", "governor", "minister", "councilor",
    "ambassador", "secretary", "president", "vp", "chancellor", "mayor", "commissioner",

    # Business, management, and leadership
    "ceo", "cto", "coo", "cfo", "founder", "cofounder", "partner", "director",
    "avp", "manager", "lead", "consultant", "advisor", "analyst",
    "associate", "intern", "trainee", "executive", "team lead", "product manager", "project manager",

    # Finance, accounting, and compliance
    "cfa", "cfp", "cpa", "ca", "chartered accountant", "cs", "icwa", "icwai",
    "cost accountant", "actuary", "risk manager", "compliance officer",

    # Miscellaneous
    "jr", "junior", "sr", "senior", "i", "ii", "iii", "iv",
    "coach", "trainer", "mentor", "freelancer", "creator", "influencer", "strategist", "specialist"
]

    name_parts = full_name.lower().split()
    # name_parts = [s for s in name_parts if "." not in s]
    name_parts = [part.replace(",", "").replace(".", "") for part in name_parts]
    cleaned = [part for part in name_parts if part not in titles]
    return cleaned


def probable_mail_gen_for_1_lead(lead_detail):
    name = clean_name(lead_detail['name'])  

    first, last = "", ""
    if not name:
        return []
    if len(name) == 1:
        first = name[0]
    elif len(name) == 2:
        first, last = name[0], name[1]
    else:
        first, last = name[0], name[-1]

    domain = "@" + lead_detail['curr_company_url'].split("//")[-1].split("/")[0].replace("www.", "")
    
    # Generate valid combinations upfront
    local_part = set()
    for fn in [first, first[0] if first else "", ""]:
        for ln in [last, last[0] if last else "", ""]:
            for sep in [".", "_", ""]:
                if fn or ln:  # Skip empty combinations
                    local_part.add(f"{fn}{sep}{ln}")
                    local_part.add(f"{ln}{sep}{fn}")
    
    # Filter invalid patterns
    emails = []
    for lp in local_part:
        if not lp.startswith((".", "_")) and not lp.endswith((".", "_")) and len(lp) > 1:
            emails.append(lp + domain)
    
    return emails






def generate_email_addresses_from_data(leads_data: List[Dict]) -> List[Dict]:
    """
    Generate probable email addresses for a list of leads.
    
    Args:
        leads_data (List[Dict]): List of dictionaries containing lead information:
            {
                'lead_name': str,
                'lead_id': str,
                'company_website': str
            }
            
    Returns:
        List[Dict]: List of dictionaries containing lead information and generated emails:
            {
                'lead_name': str,
                'lead_id': str,
                'company_website': str,
                'probable_emails': List[str]
            }
    """
    if not leads_data:
        return []
    
    # Process in batches of 5 leads for better performance
    batch_size = 5
    results = []
    
    for i in range(0, len(leads_data), batch_size):
        batch = leads_data[i:i + batch_size]
        
        # Process each lead in the batch
        for lead in batch:
            try:
                # Prepare lead details for email generation
                lead_detail = {
                    'name': lead['lead_name'],
                    'curr_company_url': lead['company_website']
                }
                
                # Generate emails for this lead
                emails = probable_mail_gen_for_1_lead(lead_detail)
                
                # Create result dictionary
                result = {
                    'lead_name': lead['lead_name'],
                    'lead_id': lead['lead_id'],
                    'company_website': lead['company_website'],
                    'probable_emails': emails
                }
                
                results.append(result)
                
                # Add delay between leads to avoid rate limits
                if i + batch_size < len(leads_data):
                    time.sleep(0.5)
                    
            except Exception as e:
                print(f"Error processing lead {lead.get('lead_name', 'Unknown')}: {str(e)}")
                # Add the lead with empty emails list in case of error
                results.append({
                    'lead_name': lead['lead_name'],
                    'lead_id': lead['lead_id'],
                    'company_website': lead['company_website'],
                    'probable_emails': []
                })
    
    return results










# Test cases

# linkedin_name_test_cases = [
#     {"name": "Dr. Jane Doe (hello world  me  )", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Dr. Firoz M.", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Mr. A. K. (अजीत द्विवेदी) Dwivedi ", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Mr. Raj Malhotra Jr.", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Mary-Jane Watson", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Dr. María Clara Cecilia Rodríguez", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Jean-Luc Picard", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Satoshi Nakamoto", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Lt. Col. David Brown", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Rev. John-Paul II", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Angela Merkel", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "H.E. Dr. Abdul Kalam", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Capt. Jack Sparrow", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Samuel L. Jackson", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Mrs. Olivia de Havilland", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Dr. James K. Polk III", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Elon R. Musk", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Miss Priya Sharma", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Sir Richard Branson", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Judge Judy Sheindlin", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "His Excellency Ban Ki-moon", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Hon. Barack H. Obama", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Ms. Aisha al-Fulan", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Dato' Sri Najib Razak", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Mr. O'Connor", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Fr. John Francis Xavier", "curr_company_url": "https://www.linkedin.com/company/1234567890"  },
#     {"name": "Mr. Li Wei", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Prof. Dr. Wolfgang Schäuble", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "The Rt Hon Theresa May", "curr_company_url": "https://www.linkedin.com/company/1234567890"},
#     {"name": "Dame Maggie Smith", "curr_company_url": "https://www.linkedin.com/company/1234567890"}
# ]

# for name in linkedin_name_test_cases:
#     print(probable_mail_gen_for_1_lead(name))


leads_data = [
    {"lead_name": "Kiran pandey", "lead_id": "LLD01", "company_website": "https://www.panscience.xyz/"},
    {"lead_name": "Happy Singh", "lead_id": "LLD02", "company_website": "https://www.panscience.xyz/"},
    {"lead_name": "Akshat Singh", "lead_id": "LLD03", "company_website": "https://www.panscience.xyz/"},
    {"lead_name": "Anshul V. Pandey, PhD", "lead_id": "LLD04", "company_website": "https://www.panscience.xyz/"},
    {'lead_name': 'Tanisha Singh, PhD', 'lead_id': 'LLD05', 'company_website': 'https://www.panscience.xyz/'}
]

print(generate_email_addresses_from_data(leads_data))