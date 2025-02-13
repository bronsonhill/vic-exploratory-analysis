import pandas as pd
import openai
import json
from dotenv import load_dotenv
import os
from itertools import islice
from datetime import datetime
import csv


MODEL_NAME = "gpt-4o" # choose between 'gpt-4o' and 'gpt-4o-mini'
SUBSET_SIZE = 2 # Number of theses to classify. Set to 1000 for all theses.
CLASSIFICATION_METHOD = 'accuracy' # Choose between 'accuracy' and 'cost'
DATASET_PATH = 'thesis_records_train.csv' # choose between 'thesis_records_train.csv' and 'thesis_records_test.csv'
CATEGORY_BOOK_PATH = 'category_book.csv' # choose your categroy book.

def classify_theses(method='accuracy'):
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')
    theses = get_thesis_records(SUBSET_SIZE)
    all_categories = get_all_categories()
    results = []
    for thesis in theses:
        print(f"Classifying thesis: {thesis['Link']}")
        if method == 'accuracy':
            categories = classify_thesis(thesis['Text'])
        elif method == 'cost':
            categories = classify_thesis_cost_effective(thesis['Text'])
        else:
            raise ValueError("Invalid classification method. Choose 'accuracy' or 'cost'.")
        thesis_result = thesis.copy()
        if method == 'accuracy':
            for category in all_categories.keys():
                thesis_result[category] = 1 if categories.get(category, {}).get('value', False) else 0
        else:
            for category in all_categories.keys():
                thesis_result[category] = 1 if category in categories['categories'] else 0
        results.append(thesis_result)
    save_results_to_csv(results)
    return results

def get_thesis_records(count=1000):
    try:
        # Read the CSV file
        thesis_records = pd.read_csv('thesis_records_train.csv')
        # Limit the number of records
        thesis_records = thesis_records.head(count)
        return thesis_records.to_dict('records')
    except Exception as e:
        print(f"Error fetching thesis records: {e}")
        return []

def chunk_dict(data, chunk_size=33):
    """Split dictionary into smaller chunks."""
    it = iter(data.items())
    for i in range(0, len(data), chunk_size):
        yield dict(islice(it, chunk_size))

def get_classifier_function_schema(categories_dict):
    """Creates schema for a subset of categories."""
    function_schema = {
        "name": "extract_investment_categories_from_thesis",
        "description": "Given a thesis, identify whether each investment approach in the list applies. Return true or false, plus a justification.",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "categories": {
                    "type": "object",
                    "description": "A dictionary of categories with booleans representing their presence in the input text",
                    "properties": categories_dict,
                    "additionalProperties": False,
                    "required": list(categories_dict.keys())
                }
            },
            "required": ["categories"],
            "additionalProperties": False
        }
    }
    return function_schema

def get_all_categories(category_book_path='category_book.csv'):
    """Get all categories from the category book."""
    category_book = pd.read_csv(category_book_path)
    categories = {}
    for index, row in category_book.iterrows():
        categories[row['Label']] = {
            "type": "object",
            "properties": {
                "value": {
                    "type": "boolean",
                    "description": f"Indicates if {row['Label']} approach is present in the thesis, described as: {row['Description']}"
                },
                "justification": {
                    "type": "string",
                    "description": f"A brief explanation of why the {row['Label']} category was assigned true or false, using quotes or references to the thesis text."
                }
            },
            "required": ["value", "justification"],
            "additionalProperties": False
        }
    return categories

def classify_thesis(thesis_text):
    all_categories = get_all_categories()
    all_results = {"categories": {}}

    for chunk in chunk_dict(all_categories, 30):
        print(f"Classifying chunk: {chunk.keys()}")
        messages = [
            {"role": "system", "content": "You are a helpful investment thesis categorisation assistant."},
            {"role": "user", "content": f"Provide categories for the following investment thesis: {thesis_text}"}
        ]

        response = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=[
                {
                    "type": "function",
                    "function": get_classifier_function_schema(chunk)
                }
            ],
            tool_choice={"type": "function", "function": {"name": "extract_investment_categories_from_thesis"}}
        )

        try:
            chunk_result = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
            all_results["categories"].update(chunk_result["categories"])
        except Exception as e:
            print(f"Error processing chunk: {e}")

    return all_results["categories"]

def classify_thesis_cost_effective(thesis_text):
    category_book = pd.read_csv(CATEGORY_BOOK_PATH)
    messages = [
        {"role": "system", "content": f"You are a helpful investment thesis categorisation assistant. You return an array of categories present in the thesis from the following: {category_book}"},
        {"role": "user", "content": f"Provide categories for the following investment thesis: {thesis_text}"}
    ]

    response = openai.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "extract_investment_categories_from_thesis",
                    "description": f"Given a thesis, identify which of the provided categories are present. Return an array of the categories present, use the exact labels of the categories given.",
                    "strict": True,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "categories": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "description": "An array of categories present in the thesis."
                            }
                        },
                        "required": ["categories"],
                        "additionalProperties": False
                    }
                }
            }
        ],
        tool_choice={"type": "function", "function": {"name": "extract_investment_categories_from_thesis"}}
    )

    try:
        categories_present = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        print(categories_present)
        return categories_present
    except Exception as e:
        print(f"Error processing response: {e}")
        return []

def save_results_to_csv(results):
    if not results:
        return
    fieldnames = [field for field in results[0].keys() if field != 'Text']
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"classification_results_{timestamp}.csv"
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            result.pop('Text', None)
            writer.writerow(result)

# Example usage
if __name__ == "__main__":
    res = classify_theses(method=CLASSIFICATION_METHOD)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"classification_results_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(res, f, indent=4)