import PyPDF2
import google.generativeai as genai
import json

class ResumeAnalyzer:
    def __init__(self, api_key):
        """
        Initializes the Gemini AI model with the user-provided API key.
        """
        genai.configure(api_key=api_key)
        # Using gemini-1.5-flash for high-speed analysis and technical accuracy
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def extract_text(self, pdf_file):
        """
        Extracts raw text from an uploaded PDF resume.
        """
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    def analyze_resume(self, text, jd=""):
        """
        Performs deep semantic analysis focusing on action-verbs, 
        JD alignment, and project impact metrics.
        """
        prompt = f"""
        Role: Senior Technical Recruiter & AI Resume Specialist.
        Task: Analyze the provided Resume Text against the Target Job Description (if provided).
        
        RESUME TEXT: 
        {text}
        
        TARGET JOB DESCRIPTION: 
        {jd}

        STRICT JSON OUTPUT FORMAT:
        {{
          "skills": ["List of top technical/soft skills"],
          "keywords": ["Industry-specific keywords identified"],
          "rating": 0, 
          "summary": "A high-impact 2-line professional summary for the top of the resume.",
          "suggestions": {{
            "Experience/Projects": "Identify passive descriptions and suggest STAR-method improvements.",
            "Technical Skills": "Highlight missing core technologies based on the JD.",
            "Tone/Clarity": "Evaluate professional tone and formatting impact."
          }},
          "action_tasks": [
            "Specific Task 1: Replace [weak verb] with a metric-driven result.",
            "Specific Task 2: To reach an 8/10 score, add [specific missing skill]."
          ],
          "alignment_gaps": ["List specific skills or experiences missing for the target JD"]
        }}

        EVALUATION CRITERIA:
        1. Rating (out of 10): Give a score based on clarity and measurable impact.
        2. Impact: Focus on "action-oriented" descriptions. Use words like 'Spearheaded', 'Optimized', or 'Architected'.
        3. Innovation: Suggest innovative ways to present data (e.g., quantifiable results).
        
        Return ONLY valid JSON.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Cleaning the response to ensure valid JSON parsing
            clean_json = response.text.replace('```json', '').replace('```', '').strip()
            return json.loads(clean_json)
        except Exception as e:
            return {
                "error": "Failed to analyze resume. Check your API key or file format.",
                "details": str(e)
            }
