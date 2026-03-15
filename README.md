# CV-Autokey

Automatically tailor your resume to job postings using AI. CV-Autokey extracts key technologies and requirements from a job description and intelligently customizes your resume's experience and skills sections to match.

## Features

- **Job Description Analysis**: Automatically scrapes and analyzes job descriptions from URLs
- **AI-Powered Tailoring**: Uses Gemini AI to extract technical keywords and tailor resume content
- **Smart Caching**: Caches API responses to avoid redundant calls for the same job posting
- **LaTeX Support**: Generates professionally formatted PDF resumes with LaTeX
- **Configurable**: YAML-based configuration for different roles and models
- **Multi-format Support**: Handles LaTeX and other resume formats

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install LaTeX compiler (required for PDF generation):
   
   **Linux (Debian/Ubuntu):**
   ```bash
   sudo apt-get install texlive-latex-base texlive-latex-extra
   ```
   
   **macOS:**
   ```bash
   brew install basictex
   # or install full TeX Live via MacTeX
   ```
   
   **Windows:**
   - Download and install [MiKTeX](https://miktex.org/download) or [TeX Live](https://tug.org/texlive/acquire-netinstall.html)

5. Set up environment variables:
   - Create a `.env` file with your Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

## Configuration

Edit `config.yaml` to configure:
- `role`: Job role you're targeting (e.g., `swe_backend_data`)
- `model`: AI model to use (e.g., `gemini`)
- `model_name`: Specific model version (e.g., `gemini-3-flash-preview`)
- `input`: Path to your resume LaTeX file
- `output`: Path for the tailored resume
- `output_pdf`: Path for the generated PDF

## Usage

Run the main script with the resume config and job URL:

```bash
python3 main.py config.yaml "https://example.com/job-posting"
```

Or use the provided shell script:

```bash
./run.sh "https://example.com/job-posting"
```

The script will:
1. Extract your resume's experience and skills
2. Analyze the job description for required technologies
3. Generate a tailored resume in LaTeX format
4. Compile to PDF
5. Cache results for future use

## Project Structure

```
.
├── main.py                 # Entry point
├── cv_autokey.py          # Main application logic
├── config.yaml            # Configuration file
├── requirements.txt       # Python dependencies
│
├── models/                # AI model implementations
│   ├── base_model.py      # Base model interface
│   ├── gemini.py          # Gemini AI integration
│   └── model_factory.py   # Model instantiation
│
├── cv_reader/             # Resume parsing
│   ├── base_reader.py     # Base reader interface
│   ├── latex_reader.py    # LaTeX resume parsing
│   └── reader_factory.py  # Reader instantiation
│
├── cv_writer/             # Resume generation
│   ├── base_writer.py     # Base writer interface
│   ├── tex_writer.py      # LaTeX resume generation
│   └── writer_factory.py  # Writer instantiation
│
├── utils/                 # Utility modules
│   ├── cache.py           # JSON-based caching decorator
│   ├── config.py          # YAML config reader
│   ├── web_scraper.py     # Job description scraper
│   └── prompts.py         # AI prompt templates
│
├── scripts/               # Helper scripts
│   └── latex_compiler.sh  # LaTeX to PDF compiler
│
├── input/                 # Resume and class files
│   ├── resume_faang.tex   # Base resume template
│   └── resume.cls         # LaTeX resume class
│
└── output/                # Generated files
    ├── tailored_resume.tex
    └── tailored_resume.pdf
```

## How It Works

1. **Resume Reading**: Parses your LaTeX resume to extract experience and skills sections
2. **Job Analysis**: Scrapes the job posting and uses Gemini AI to identify key technologies
3. **Content Tailoring**: Generates customized experience and skills sections relevant to the job
4. **Resume Generation**: Replaces sections in your original resume with tailored content
5. **PDF Compilation**: Compiles the LaTeX to a professional PDF using pdflatex

## Caching System

Results are cached in `cache.json` to avoid:
- Redundant API calls for the same job posting
- Repeated scraping of the same URL

Cache keys are based on SHA256 hashes of function inputs.

## Dependencies

- Python 3.8+
- pdflatex (for PDF generation)
- python-dotenv
- google-generativeai (or similar for Gemini)
- PyYAML

See `requirements.txt` for full list.

## Sources

- [FAANGPath Resume Template](https://www.overleaf.com/latex/templates/faangpath-simple-template/npsfpdqnxmbc)