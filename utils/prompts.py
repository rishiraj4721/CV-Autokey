
def get_tailor_resume_prompt(role, original_experience, original_skills, keywords, output_format):
    output_format_prompt = get_output_format_prompt(output_format)

    prompt = ROLES.get(role)
    if not prompt:
        raise ValueError(f"Role '{role}' not found in ROLES. Available roles: {list(ROLES.keys())}")
    return prompt(original_experience, original_skills, keywords, output_format_prompt)

def get_output_format_prompt(output_format):
    match output_format:
        case "latex":
            return f"""
            [EXPERIENCE_START]
            <LaTeX formatted experience with itemize>
            [EXPERIENCE_END]
            [SKILLS_START]
            <LaTeX formatted skills>
            [SKILLS_END]

            Return ONLY the LaTeX formatted sections with the delimiters. No other text.
            """
        case _:
            raise ValueError(f"Unsupported output format: {output_format}")


def prompt_swe_backend_data(original_experience, original_skills, keywords, output_format):
    prompt = f"""
    You are an expert technical resume writer. Your task is to rewrite BOTH the 'Experience' and 'Skills' sections of this resume to match the job requirements.
    
    CONTEXT:
    The candidate is a Software Engineer focusing on Backend and Data Engineering. 
    Job Requirements Keywords: {keywords}
    
    STRICT GUIDELINES FOR EXPERIENCE SECTION:
    1. Focus on engineering impact with specific metrics (latency %, data volume in TB/PB, cost savings, percentage improvements).
    2. Use the STAR method (Situation, Task, Action, Result) for each bullet point.
    3. Integrate tools and technologies naturally without sounding forced.
    4. Use LaTeX itemize environment: \\begin{{itemize}} \\item ... \\end{{itemize}}
    
    STRICT GUIDELINES FOR SKILLS SECTION:
    1. Prioritize and reorganize technical skills to match the job requirements.
    2. Add relevant skills from the keywords if the candidate clearly demonstrates them in their experience.
    3. Organize skills by category (Languages, Databases, Data Tools, Infrastructure, etc.) if necessary.
    4. Do not invent skills; only rephrase and reorganize existing ones to better match the job.
    5. Use LaTeX tabular environment or itemize as appropriate.
    
    GENERAL GUIDELINES:
    6. Do not invent experience or skills that don't exist; only rephrase and reorganize.
    7. OUTPUT FORMAT: Return ONLY LaTeX formatted content. Do NOT include markdown, code blocks, explanations, or commentary.
    8. Use ONLY the delimiters [EXPERIENCE_START] and [EXPERIENCE_END] and [SKILLS_START] and [SKILLS_END] to mark sections.
    
    Original Experience Section:
    {original_experience}
    
    Original Skills Section:
    {original_skills}
    
    OUTPUT FORMAT (strictly follow this):
    {output_format}
    """
    return prompt


ROLES = {
    "swe_backend_data": prompt_swe_backend_data,
}