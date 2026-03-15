#!/bin/bash

# Compile a LaTeX file to PDF using pdflatex
#
# Usage: compile_latex_to_pdf <tex_file> <pdf_output>
#
# Args:
#     $1: Path to the input .tex file
#     $2: Path to the output .pdf file
#
# Returns:
#     0 if compilation is successful, 1 otherwise
#
# Features:
#     - Compiles tex file to pdf using pdflatex (runs twice for proper references)
#     - Copies resume.cls from project input/ directory if needed
#     - On success: removes auxiliary files (.log, .out, .aux)
#     - On failure: keeps auxiliary files for debugging

compile_latex_to_pdf() {
    local tex_file="$1"
    local pdf_output="$2"
    
    # Validate inputs
    if [[ -z "$tex_file" || -z "$pdf_output" ]]; then
        echo "Error: Missing arguments. Usage: compile_latex_to_pdf <tex_file> <pdf_output>"
        return 1
    fi
    
    # Check if tex file exists
    if [[ ! -f "$tex_file" ]]; then
        echo "Error: LaTeX file not found: $tex_file"
        return 1
    fi
    
    # Get file and directory information
    local tex_dir=$(dirname "$tex_file")
    local tex_basename=$(basename "$tex_file")
    
    # Get project root from script location
    local script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
    local project_root=$(dirname "$script_dir")
    local input_dir="$project_root/input"
    
    # Convert tex_dir to absolute path if relative
    if [[ ! "$tex_dir" = /* ]]; then
        tex_dir="$PWD/$tex_dir"
    fi
    
    # Copy resume.cls from input directory to tex directory
    if [[ -f "$input_dir/resume.cls" ]]; then
        cp "$input_dir/resume.cls" "$tex_dir/"
    fi
    
    # Change to tex directory
    cd "$tex_dir" || return 1
    
    # Set TEXINPUTS for LaTeX to find class files
    export TEXINPUTS=".:$input_dir:$project_root:"
    
    # First compilation pass
    pdflatex -interaction=nonstopmode -output-directory="." "$tex_basename" > /dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        echo "Error: LaTeX compilation failed"
        return 1
    fi
    
    # Second compilation pass (for proper references)
    pdflatex -interaction=nonstopmode -output-directory="." "$tex_basename" > /dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        echo "Error: LaTeX compilation failed"
        return 1
    fi
    
    # Verify PDF was generated
    local pdf_name="${tex_basename%.tex}.pdf"
    if [[ ! -f "$pdf_name" ]]; then
        echo "Error: PDF file was not generated"
        return 1
    fi
    
    # Store auxiliary file names before moving PDF
    local base_name="${tex_basename%.tex}"
    local aux_files=("${base_name}.log" "${base_name}.out" "${base_name}.aux")
    
    echo "Successfully generated: $pdf_output"
    
    # Clean up auxiliary files
    for aux_file in "${aux_files[@]}"; do
        if [[ -f "$aux_file" ]]; then
            rm -f "$aux_file"
        fi
    done
    
    # Clean up copied files
    rm -f "$tex_dir/resume.cls"
    
    return 0
}

# Export function for use in other scripts
export -f compile_latex_to_pdf
