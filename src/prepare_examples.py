import json


def prepare_examples():
    try:
        # Read sentiment analysis results from JSON file
        with open("sentiment_analysis_results.json", "r") as f:
            sentiment_results = json.load(f)
    except FileNotFoundError:
        print("Error: 'sentiment_analysis_results.json' not found.")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON in 'sentiment_analysis_results.json'.")
        return

    # Prepare examples covering different scenarios
    examples = {
        "positive_sentiment": [],
        "negative_sentiment": [],
        "neutral_sentiment": [],
    }

    for stock, result in sentiment_results.items():
        combined_sentiment = result["combined_sentiment"]
        if combined_sentiment > 0:
            examples["positive_sentiment"].append({stock: result})
        elif combined_sentiment < 0:
            examples["negative_sentiment"].append({stock: result})
        else:
            examples["neutral_sentiment"].append({stock: result})

    # Save examples to a new JSON file
    try:
        with open("examples_output.json", "w") as f:
            json.dump(examples, f, indent=2)
        print("Examples prepared and saved in 'examples_output.json'.")
    except IOError as e:
        print(f"Error: Unable to write to 'examples_output.json'. {str(e)}")


if __name__ == "__main__":
    prepare_examples()
