import re
import json
import os
import logging
from typing import List, Set

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def identify_stocks(subtitles: List[str]) -> List[str]:
    """
    Identify stock mentions within the extracted subtitles.

    Args:
    subtitles (List[str]): List of subtitle strings.

    Returns:
    List[str]: List of identified stock symbols or company names.
    """
    # Ensure all items in subtitles are strings
    subtitles = [str(item) if not isinstance(item, str) else item for item in subtitles]

    # Get the absolute path to the project root directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Construct the path to the JSON file
    json_path = os.path.join(project_root, 'data', 'top_1000_companies.json')

    try:
        # Load the extended list of stock symbols and company names from the JSON file
        with open(json_path, 'r') as f:
            companies = json.load(f)
    except FileNotFoundError:
        logging.error(f"Could not find the file {json_path}")
        return []
    except json.JSONDecodeError:
        logging.error(f"Could not parse the JSON file {json_path}")
        return []

    stock_symbols = [company['symbol'] for company in companies]
    company_names = [company['name'] for company in companies]

    # Combine stock symbols and company names into a single list
    stock_mentions = stock_symbols + company_names

    # Create a set to store identified stock mentions
    identified_stocks: Set[str] = set()

    # Define a regular expression pattern to match stock symbols and company names
    pattern = re.compile(r'\b(' + '|'.join(re.escape(symbol) for symbol in stock_mentions) + r')\b', re.IGNORECASE)

    # Search through the subtitles to identify stock mentions
    for text in subtitles:
        matches = pattern.findall(text)
        identified_stocks.update(match.upper() for match in matches)

    return list(identified_stocks)

# Example usage
if __name__ == '__main__':
    # Read subtitles from the subtitles.json file
    try:
        with open('subtitles.json', 'r') as file:
            subtitles = json.load(file)
    except FileNotFoundError:
        logging.error("Could not find the subtitles.json file")
        exit(1)
    except json.JSONDecodeError:
        logging.error("Could not parse the subtitles.json file")
        exit(1)

    # Ensure subtitles are in the correct format (list of strings)
    if isinstance(subtitles, list) and all(isinstance(item, str) for item in subtitles):
        identified_stocks = identify_stocks(subtitles)
    else:
        # If subtitles are not in the correct format, try to extract text from each item
        subtitles_text = [item.get('text', '') if isinstance(item, dict) else str(item) for item in subtitles]
        identified_stocks = identify_stocks(subtitles_text)

    print(json.dumps(identified_stocks))
