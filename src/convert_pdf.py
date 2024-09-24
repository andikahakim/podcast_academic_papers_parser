# src/convert_pdf.py
import os
import sys
import subprocess
import json

def convert_pdf_to_markdown(pdf_path, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Construct the command
    command = ["nougat", "--markdown", "pdf", pdf_path, "--out", output_folder]
    print(f"Running command: {' '.join(command)}")  # Debug statement
    
    # Run the command
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')  # Set encoding to 'utf-8'
    
    # Check the result
    if result.returncode != 0:
        print(f"Error converting {pdf_path}: {result.stderr}")
        print(f"Full error output: {result.stdout}")
    else:
        print(f"Successfully converted {pdf_path} to Markdown.")
        # Read the generated Markdown file
        markdown_file = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(pdf_path))[0]}.mmd")
        if os.path.exists(markdown_file):
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()
            # Create metadata
            metadata = {
                "title": os.path.basename(pdf_path),
                "source": "PDF",
                "content": content
            }
            # Save metadata to JSON
            json_output_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(pdf_path))[0]}.json")
            save_to_json(metadata, json_output_path)
            print(f"Saved JSON metadata to {json_output_path}")

def save_to_json(data, output_path):
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

def process_pdfs(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for pdf_file in os.listdir(input_folder):
        if pdf_file.endswith('.pdf'):
            pdf_path = os.path.join(input_folder, pdf_file)
            output_file_name = f"{os.path.splitext(pdf_file)[0]}.mmd"
            output_path = os.path.join(output_folder, output_file_name)
            
            if os.path.exists(output_path):
                print(f"Skipping {pdf_file} as Markdown file already exists.")
                continue
            
            print(f"Converting {pdf_path} to {output_folder}")  # Debug statement
            convert_pdf_to_markdown(pdf_path, output_folder)
            print(f"Converted {pdf_file} to Markdown.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/convert_pdf.py <input_folder>")
        sys.exit(1)
    
    input_folder = sys.argv[1]
    output_folder = 'output/publications'
    
    print(f"Processing PDFs from {input_folder} to {output_folder}")  # Debug statement
    process_pdfs(input_folder, output_folder)