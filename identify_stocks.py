import re
import sys
import json
import os

def identify_stocks(subtitles):
    """
    Identify stock mentions within the extracted subtitles.

    Args:
    subtitles (list of str): List of subtitle strings.

    Returns:
    list of str: List of identified stock symbols or company names.
    """
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the JSON file
    json_path = os.path.join(current_dir, 'top_1000_companies.json')

    try:
        # Load the extended list of stock symbols and company names from the JSON file
        with open(json_path, 'r') as f:
            companies = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find the file {json_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not parse the JSON file {json_path}")
        return []

    stock_symbols = [company['symbol'] for company in companies]
    company_names = [company['name'] for company in companies]

    # Combine stock symbols and company names into a single list
    stock_mentions = stock_symbols + company_names

    # Print the count of loaded stock symbols and company names
    print(f"Loaded {len(stock_symbols)} stock symbols and {len(company_names)} company names.")

    # Create a set to store identified stock mentions
    identified_stocks = set()

    # Define a regular expression pattern to match stock symbols and company names
    pattern = re.compile(r'\b(' + '|'.join(re.escape(symbol) for symbol in stock_mentions) + r')\b', re.IGNORECASE)

    # Search through the subtitles to identify stock mentions
    for subtitle in subtitles:
        matches = pattern.findall(subtitle)
        for match in matches:
            identified_stocks.add(match.upper())

    # Print identified stock mentions
    print(f"Identified stock mentions: {identified_stocks}")

    return list(identified_stocks)

# Example usage
if __name__ == '__main__':
    # Read subtitles from standard input or command line arguments
    if len(sys.argv) > 1:
        subtitles = json.loads(sys.argv[1])
    else:
        subtitles = json.load(sys.stdin)

    identified_stocks = identify_stocks(subtitles)
    print(json.dumps(identified_stocks))
