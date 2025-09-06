# backend/report_generator.py
from typing import List, Dict

class ReportGenerator:
    def generate_report(self, vacancy_text: str, resume_text: str, responses: List[Dict]) -> Dict:
        """Генерация отчета (заглушка)"""
        return {
            "summary": "Детальный анализ кандидата",
            "score": 85,
            "strengths": ["Опыт работы", "Технические навыки"],
            "weaknesses": ["Отсутствие опыта с Docker", "Ограниченный опыт руководства"],
            "recommendation": "Рекомендован к найму"
        }