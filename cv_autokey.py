
from dotenv import load_dotenv

from utils.cache import json_cache
from utils.config import YAMLConfig
from utils.web_scraper import get_text_from_url
from utils.prompts import get_tailor_resume_prompt

from models.model_factory import get_model
from cv_reader.reader_factory import get_reader
from cv_writer.writer_factory import get_writer


class CVAutoKey:
    def __init__(self, config_path):
        self.config = YAMLConfig(config_path).read()
        self.model = get_model(self.config["model"], self.config["model_name"])
        self.client = self.model.get_client()
        self.read_resume(self.config["input"])
    
    def read_resume(self, resume_path):
        reader = get_reader(self.config['input_format'])
        self.full_resume = reader.read(resume_path)
        self.experience = reader.extract_experience(resume_path)
        self.skills = reader.extract_skills(resume_path)

    @json_cache(key_args=["url"])
    def extract_tech_keywords(self, url):
        job_description = get_text_from_url(url)
        
        prompt = f"""
        Analyze this Backend/Data Engineering Job Description. 
        Extract:
        1. Primary Languages (e.g. Go, Python, Scala)
        2. Data Stack (e.g. Spark, Airflow, Snowflake, Kafka, Postgres)
        3. Infrastructure (e.g. AWS, K8s, Terraform, CI/CD)
        4. Concepts (e.g. Distributed Systems, ETL, Microservices, Observability)
        
        Job Description:
        {job_description}
        """
        print("[API Call] Extracting tech keywords from job description...")
        response = self.model.generate(prompt=prompt)
        result = response.strip()
        
        self.keywords = result
        return result
    
    @json_cache(key_args=["url"])
    def tailor_resume(self, url):
        prompt = get_tailor_resume_prompt(
            role=self.config['role'],
            original_experience=self.experience,
            original_skills=self.skills,
            keywords=self.keywords,
            output_format=self.config['output_format']
        )

        print("[API Call] Tailoring resume experience and skills sections...")
        response = self.model.generate(prompt=prompt)
        result = response.strip()
        
        # Clean up result: remove markdown formatting and explanatory text
        # Keep only content
        lines = result.split('\n')
        cv_lines = []
        for line in lines:
            # Skip markdown headers, dividers, and explanatory sections
            if line.startswith('###') or line.startswith('***') or line.startswith('1.') or line.startswith('2.'):
                continue
            if line.startswith('**Note:') or line.startswith('*   **'):
                continue
            # Keep content
            cv_lines.append(line)
        result = '\n'.join(cv_lines).strip()
        return result

    def format_and_write_output(self, tailored_content):
        writer = get_writer(self.config['output_format'])
        writer.format_output(self.full_resume, tailored_content)
        writer.write_output(self.config['output'])

    def run(self, url):
        self.extract_tech_keywords(url)
        result = self.tailor_resume(url)
        self.format_and_write_output(result)
    