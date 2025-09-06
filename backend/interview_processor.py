# backend/interview_processor.py
from typing import Dict, Optional
import random

class InterviewProcessor:
    def __init__(self):
        self.question_number = 0
        self.current_question = ""
        self.questions = [
            "Расскажите о вашем опыте работы?",
            "Какие технологии вы используете?",
            "Как вы решаете сложные задачи?",
            "Расскажите о вашем последнем проекте?",
            "Какие у вас карьерные цели?"
        ]
    
    def read_docx(self, file_path: str) -> str:
        """Чтение DOCX файла (заглушка)"""
        return "Текст документа"
    
    def start_interview(self, vacancy_text: str, resume_text: str) -> str:
        """Начало интервью (заглушка)"""
        self.question_number = 1
        self.current_question = self.questions[0]
        return self.current_question
    
    def process_response(self, response: str) -> Optional[str]:
        """Обработка ответа (заглушка)"""
        if self.question_number >= len(self.questions):
            return None
        self.question_number += 1
        self.current_question = self.questions[self.question_number - 1]
        return self.current_question
    
    def evaluate_candidate(self) -> Dict:
        """Оценка кандидата (заглушка)"""
        return {
            "score": random.randint(60, 95),
            "feedback": "Кандидат показал хорошие результаты",
            "recommendation": "Пригласить на следующий этап"
        }