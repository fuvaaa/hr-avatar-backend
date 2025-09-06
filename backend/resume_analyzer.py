import os
import re
from typing import Dict, List, Tuple
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import HumanMessage, SystemMessage
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ResumeAnalyzer:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.nlp = spacy.load("ru_core_news_sm")
        
        # Ключевые навыки для IT специалистов
        self.tech_skills = [
            'python', 'java', 'javascript', 'typescript', 'html', 'css', 
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'fastapi',
            'postgresql', 'mysql', 'mongodb', 'redis', 'docker', 'kubernetes',
            'aws', 'azure', 'gcp', 'git', 'linux', 'bash', 'sql', 'nosql',
            'rest', 'api', 'graphql', 'microservices', 'ci/cd', 'jenkins',
            'terraform', 'ansible', 'puppet', 'chef', 'agile', 'scrum'
        ]
    
    def extract_skills_from_text(self, text: str) -> List[str]:
        """Извлекает технические навыки из текста"""
        found_skills = []
        text_lower = text.lower()
        
        for skill in self.tech_skills:
            if skill in text_lower:
                # Проверяем, что это отдельное слово, а не часть другого слова
                if re.search(rf'\b{skill}\b', text_lower):
                    found_skills.append(skill)
        
        return list(set(found_skills))  # Убираем дубликаты
    
    def extract_experience(self, text: str) -> int:
        """Извлекает опыт работы из текста резюме"""
        # Паттерны для поиска опыта работы
        patterns = [
            r'(\d+)\s*(год|года|лет)\s+опыт',
            r'опыт\s+работы\s+(\d+)\s*(год|года|лет)',
            r'experience\s+(\d+)\s*(year|years)',
            r'(\d+)\+?\s*(год|года|лет|year|years)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return int(match.group(1))
        
        return 0  # Если опыт не указан
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Вычисляет косинусную схожесть между текстами"""
        vectorizer = TfidfVectorizer()
        try:
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return round(similarity * 100, 2)  # Проценты
        except:
            return 0.0
    
    def analyze_resume_vacancy_match(self, resume_text: str, vacancy_text: str) -> Dict:
        """Анализирует соответствие резюме вакансии"""
        # Извлекаем навыки
        resume_skills = self.extract_skills_from_text(resume_text)
        vacancy_skills = self.extract_skills_from_text(vacancy_text)
        
        # Находим совпадения и отсутствующие навыки
        matched_skills = list(set(resume_skills) & set(vacancy_skills))
        missing_skills = list(set(vacancy_skills) - set(resume_skills))
        
        # Вычисляем опыт
        experience_years = self.extract_experience(resume_text)
        
        # Вычисляем схожесть
        similarity_score = self.calculate_similarity(resume_text, vacancy_text)
        
        return {
            "match_score": similarity_score,
            "skills_found": resume_skills,
            "skills_matched": matched_skills,
            "skills_missing": missing_skills,
            "experience_years": experience_years,
            "similarity_score": similarity_score
        }
    
    def generate_detailed_analysis(self, resume_text: str, vacancy_text: str) -> str:
        """Генерирует детальный анализ с помощью AI"""
        prompt = PromptTemplate(
            input_variables=["resume_text", "vacancy_text"],
            template="""Проанализируй соответствие резюме кандидата требованиям вакансии.

ВАКАНСИЯ:
{vacancy_text}

РЕЗЮМЕ КАНДИДАТА:
{resume_text}

Проанализируй и представь подробный отчет в следующем формате:

1. ОБЩЕЕ СООТВЕТСТВИЕ: X%
2. СОВПАДАЮЩИЕ НАВЫКИ И ОПЫТ:
   - Навык 1: описание
   - Навак 2: описание
3. ОТСУТСТВУЮЩИЕ ТРЕБОВАНИЯ:
   - Требование 1: описание
   - Требование 2: описание
4. РЕКОМЕНДАЦИИ:
   - Рекомендация 1
   - Рекомендация 2
5. ИТОГОВАЯ ОЦЕНКА: [Отлично/Хорошо/Удовлетворительно/Не подходит]"""
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        result = chain.run({
            "resume_text": resume_text[:3000],  # Ограничение длины
            "vacancy_text": vacancy_text[:3000]
        })
        
        return result
    
    def extract_match_percentage(self, analysis_text: str) -> float:
        """Извлекает процент соответствия из анализа"""
        match = re.search(r'ОБЩЕЕ СООТВЕТСТВИЕ:\s*(\d+)%', analysis_text)
        if match:
            return float(match.group(1))
        return 0.0
    
    def extract_skills_section(self, analysis_text: str, section_name: str) -> List[str]:
        """Извлекает раздел навыков из анализа"""
        section_pattern = rf"{section_name}:(.*?)(?=\n\d+\.|\n[A-ZА-Я]|$)"
        match = re.search(section_pattern, analysis_text, re.DOTALL | re.IGNORECASE)
        
        if match:
            section_text = match.group(1)
            # Извлекаем пункты списка
            items = re.findall(r'[•\-]\s*(.+?)(?=\n|$)', section_text)
            return [item.strip() for item in items if item.strip()]
        
        return []
    
    def analyze_multiple_resumes(self, vacancy_text: str, resumes_texts: List[str]) -> List[Dict]:
        """Анализирует несколько резюме против одной вакансии"""
        results = []
        
        for i, resume_text in enumerate(resumes_texts):
            analysis = self.analyze_resume_vacancy_match(resume_text, vacancy_text)
            detailed_analysis = self.generate_detailed_analysis(resume_text, vacancy_text)
            
            results.append({
                "resume_index": i,
                "match_score": analysis["match_score"],
                "similarity_score": analysis["similarity_score"],
                "skills_matched": analysis["skills_matched"],
                "skills_missing": analysis["skills_missing"],
                "experience_years": analysis["experience_years"],
                "detailed_analysis": detailed_analysis,
                "summary": self.generate_summary(analysis)
            })
        
        # Сортируем по убыванию соответствия
        results.sort(key=lambda x: x["match_score"], reverse=True)
        return results
    
    def generate_summary(self, analysis: Dict) -> str:
        """Генерирует краткое summary"""
        score = analysis["match_score"]
        
        if score >= 80:
            return "Отличное соответствие -强烈推荐"
        elif score >= 60:
            return "Хорошее соответствие - рекомендуется"
        elif score >= 40:
            return "Удовлетворительное соответствие - рассмотреть"
        else:
            return "Низкое соответствие - не рекомендуется"

# Создаем экземпляр для импорта
resume_analyzer = ResumeAnalyzer()