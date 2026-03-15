#!/bin/bash
set -e

URL=$1 # url = "https://www.indeed.com/viewjob?jk=12345"  # Replace with actual job description URL
CONFIG_FILE="config.yaml"

# source venv/bin/activate
python3 main.py "$CONFIG_FILE" "$URL"


# Source the latex compiler function
source scripts/latex_compiler.sh

# Extract tex file path (from 'output' field, which is the tailored resume in tex format)
TEX_FILE=$(grep "^output:" "$CONFIG_FILE" | sed 's/output: *//')

# Extract pdf output path
PDF_OUTPUT=$(grep "^output_pdf:" "$CONFIG_FILE" | sed 's/output_pdf: *//')

# Validate that values were read
if [[ -z "$TEX_FILE" || -z "$PDF_OUTPUT" ]]; then
    echo "Error: Could not read tex file or pdf output path from $CONFIG_FILE"
    exit 1
fi

echo "Reading from config:"
echo "  TeX file: $TEX_FILE"
echo "  PDF output: $PDF_OUTPUT"

# Compile LaTeX to PDF
compile_latex_to_pdf "$TEX_FILE" "$PDF_OUTPUT"
if [[ $? -eq 0 ]]; then
    echo "PDF generated successfully: $PDF_OUTPUT"
else
    echo "Error: LaTeX compilation failed"
    exit 1
fi