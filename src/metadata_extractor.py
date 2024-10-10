from openai import OpenAI
import json
import os
import sys
import argparse

def extract_metadata_from_text(text):
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "text": "Extract metadata from a given text formatted in Markdown.",
                        "type": "text"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        ],
        temperature=0,
        max_tokens=4095,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "extract_metadata",
                    "strict": True,
                    "parameters": {
                        "type": "object",
                        "required": [
                            "Title",
                            "type",
                            "theme",
                            "keywords",
                            "authors",
                            "journal",
                            "date",
                            "abbreviations",
                            "definitions",
                            "references"
                        ],
                        "properties": {
                            "date": {
                                "type": "string",
                                "description": "Date of publication in YYYY-MM-DD format"
                            },
                            "type": {
                                "type": "string",
                                "description": "Type of content (e.g., guideline, interview)"
                            },
                            "Title": {
                                "type": "string",
                                "description": "Title of the documents"
                            },
                            "theme": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "description": "A theme related to the document"
                                },
                                "description": "Theme of the document, multiple sub-entries possible"
                            },
                            "authors": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "description": "Name of an author"
                                },
                                "description": "List of authors of the document"
                            },
                            "journal": {
                                "type": "string",
                                "description": "Journal name if applicable"
                            },
                            "keywords": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "description": "Keyword associated with the document"
                                },
                                "description": "Keywords related to the document"
                            },
                            "references": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "description": "ALL References cited in the document"
                                },
                                "description": "ALL References cited in the document"
                            },
                            "definitions": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "description": "A definition provided in the document"
                                },
                                "description": "Definitions described in the document"
                            },
                            "abbreviations": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "description": "A single abbreviation used in the document"
                                },
                                "description": "Abbreviations used in the document"
                            }
                        },
                        "additionalProperties": False
                    }
                }
            }
        ],
        parallel_tool_calls=True,
        response_format={
            "type": "text"
        }
    )

    return response

def extract_json_metadata(response):
    # Check if there are choices in the response and if they contain tool calls
    if response and response.choices:
        choice = response.choices[0]  # Access the first choice
        if hasattr(choice.message, 'tool_calls') and choice.message.tool_calls:
            tool_call = choice.message.tool_calls[0]  # Access the first tool call
            
            # Check if the tool call contains the extracted metadata in arguments
            if hasattr(tool_call.function, 'arguments'):
                # Extract the arguments as a string and parse it as JSON
                metadata_json = json.loads(tool_call.function.arguments)
                return metadata_json
    return None

def main(input_folder):
    output_folder = './output/metadata'
    os.makedirs(output_folder, exist_ok=True)  # Create output directory if it doesn't exist

    for filename in os.listdir(input_folder):
        if filename.endswith('.md'):  # Process only Markdown files
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r') as file:
                text = file.read()
                response = extract_metadata_from_text(text)
                metadata = extract_json_metadata(response)

                # Save metadata to a file
                output_file_path = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}_metadata.json')
                with open(output_file_path, 'w') as output_file:
                    json.dump(metadata, output_file, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract metadata from Markdown files.")
    parser.add_argument('--folder', type=str, help='Input folder containing Markdown files')
    parser.add_argument('--file', type=str, help='Single Markdown file to process')

    args = parser.parse_args()

    if args.folder:
        main(args.folder)
    elif args.file:
        # If a single file is provided, process it
        if os.path.isfile(args.file) and args.file.endswith('.md'):
            output_folder = './output/metadata'
            os.makedirs(output_folder, exist_ok=True)  # Create output directory if it doesn't exist

            with open(args.file, 'r') as file:
                text = file.read()
                response = extract_metadata_from_text(text)
                metadata = extract_json_metadata(response)

                # Save metadata to a file
                output_file_path = os.path.join(output_folder, f'{os.path.splitext(os.path.basename(args.file))[0]}_metadata.json')
                with open(output_file_path, 'w') as output_file:
                    json.dump(metadata, output_file, indent=4)
        else:
            print("Please provide a valid Markdown file.")
            sys.exit(1)
    else:
        print("Usage: python src/metadata_extractor.py --folder input_folder or --file input_file")
        sys.exit(1)