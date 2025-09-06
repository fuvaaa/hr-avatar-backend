# import os
# from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse, StreamingResponse
# from typing import List, Dict, Optional
# import tempfile
# import shutil
# import uuid
# import json
# from datetime import datetime
# import io

# # Импорты наших модулей (упрощенные версии)
# from rag_processor import RAGHRSystem
# from interview_processor import InterviewProcessor
# from report_generator import ReportGenerator
# from voice_processor import VoiceProcessor
# from file_processor import FileProcessor

# app = FastAPI(title="HR-Avatar API")

# # Настройка CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Разрешаем все origins для разработки
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Инициализация процессоров
# file_processor = FileProcessor()
# rag_processor = RAGHRSystem()
# interview_processor = InterviewProcessor()

# # Хранилище сессий
# interview_sessions = {}

# @app.get("/")
# async def root():
#     return {
#         "message": "HR-Avatar API is running!",
#         "version": "1.0.0",
#         "status": "active"
#     }

# @app.get("/health")
# async def health_check():
#     return {
#         "status": "healthy", 
#         "service": "HR-Avatar API",
#         "environment": os.environ.get("ENVIRONMENT", "development")
#     }

# # ======== Базовые endpoint'ы ========
# @app.post("/api/upload-documents")
# async def upload_documents(
#     vacancy_file: UploadFile = File(...),
#     resume_files: List[UploadFile] = File(...)
# ):
#     """Загрузка и обработка вакансии и резюме"""
#     try:
#         # Извлекаем текст из файлов
#         vacancy_text = await file_processor.extract_text_from_file(vacancy_file)
#         resumes_texts = await file_processor.process_uploaded_files(resume_files)
        
#         return JSONResponse({
#             "status": "success",
#             "vacancy_filename": vacancy_file.filename,
#             "resume_filenames": [r.filename for r in resume_files],
#             "vacancy_preview": vacancy_text[:200] + "..." if len(vacancy_text) > 200 else vacancy_text,
#             "resumes_count": len(resumes_texts)
#         })
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")

# @app.post("/api/analyze-match")
# async def analyze_match(
#     vacancy_file: UploadFile = File(...), 
#     resume_file: UploadFile = File(...)
# ):
#     """Анализ соответствия резюме вакансии"""
#     try:
#         # Извлекаем текст
#         vacancy_text = await file_processor.extract_text_from_file(vacancy_file)
#         resume_text = await file_processor.extract_text_from_file(resume_file)
        
#         # Анализируем соответствие
#         analysis = rag_processor.analyze_vacancy_match(vacancy_text, resume_text)
#         match_percentage = rag_processor.extract_match_percentage(analysis)
        
#         return JSONResponse({
#             "status": "success",
#             "match_percentage": match_percentage,
#             "skills_matched": rag_processor.extract_skills(analysis),
#             "skills_missing": rag_processor.extract_missing_skills(analysis),
#             "analysis_preview": analysis[:500] + "..." if len(analysis) > 500 else analysis
#         })
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

# # ======== Интервью функционал ========
# @app.post("/api/start-interview")
# async def start_interview(
#     vacancy_file: UploadFile = File(...), 
#     resume_file: UploadFile = File(...)
# ):
#     """Начало интервью с кандидатом"""
#     try:
#         session_id = str(uuid.uuid4())
        
#         # Извлекаем текст
#         vacancy_text = await file_processor.extract_text_from_file(vacancy_file)
#         resume_text = await file_processor.extract_text_from_file(resume_file)
        
#         # Начинаем интервью
#         first_question = interview_processor.start_interview(vacancy_text, resume_text)
        
#         # Сохраняем сессию
#         interview_sessions[session_id] = {
#             "vacancy_text": vacancy_text,
#             "resume_text": resume_text,
#             "start_time": datetime.now(),
#             "responses": [],
#             "questions_asked": [first_question]
#         }
        
#         return JSONResponse({
#             "session_id": session_id,
#             "question": first_question,
#             "question_number": 1
#         })
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Interview start error: {str(e)}")

# @app.post("/api/next-question")
# async def next_question(
#     session_id: str, 
#     response: str, 
#     voice_response: Optional[UploadFile] = File(None)
# ):
#     """Следующий вопрос интервью"""
#     try:
#         if session_id not in interview_sessions:
#             raise HTTPException(status_code=404, detail="Session not found")
        
#         session = interview_sessions[session_id]
        
#         # Обработка голосового ответа
#         if voice_response:
#             voice_processor = VoiceProcessor()
#             response = voice_processor.voice_to_text(voice_response.file)
        
#         # Получаем следующий вопрос
#         next_question = interview_processor.process_response(response)
        
#         # Сохраняем ответ
#         session["responses"].append({
#             "question": session["questions_asked"][-1],
#             "response": response,
#             "timestamp": datetime.now()
#         })
        
#         if next_question:
#             session["questions_asked"].append(next_question)
            
#             return JSONResponse({
#                 "session_id": session_id,
#                 "question": next_question,
#                 "question_number": len(session["questions_asked"])
#             })
#         else:
#             # Интервью завершено
#             return JSONResponse({
#                 "session_id": session_id,
#                 "message": "Interview completed",
#                 "total_questions": len(session["questions_asked"])
#             })
            
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Next question error: {str(e)}")

# @app.post("/api/finish-interview")
# async def finish_interview(session_id: str):
#     """Завершение интервью и получение оценки"""
#     try:
#         if session_id not in interview_sessions:
#             raise HTTPException(status_code=404, detail="Session not found")
        
#         session = interview_sessions[session_id]
        
#         # Генерируем оценку
#         evaluation = interview_processor.evaluate_candidate()
        
#         # Удаляем сессию
#         del interview_sessions[session_id]
        
#         return JSONResponse({
#             "session_id": session_id,
#             "evaluation": evaluation,
#             "duration_seconds": (datetime.now() - session["start_time"]).total_seconds(),
#             "total_questions": len(session["questions_asked"]),
#             "total_responses": len(session["responses"])
#         })
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Finish interview error: {str(e)}")

# # ======== Голосовой функционал ========
# @app.post("/api/voice-to-text")
# async def voice_to_text(audio_file: UploadFile = File(...)):
#     """Преобразование голоса в текст"""
#     try:
#         voice_processor = VoiceProcessor()
#         text = voice_processor.voice_to_text(audio_file.file)
        
#         return JSONResponse({
#             "text": text,
#             "audio_filename": audio_file.filename,
#             "text_length": len(text)
#         })
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Voice to text error: {str(e)}")

# @app.get("/api/text-to-voice")
# async def text_to_voice(text: str, language: str = "ru"):
#     """Преобразование текста в голос"""
#     try:
#         voice_processor = VoiceProcessor()
#         audio_data = voice_processor.text_to_speech(text, language)
        
#         return StreamingResponse(
#             io.BytesIO(audio_data),
#             media_type="audio/mpeg",
#             headers={"Content-Disposition": f"attachment; filename=speech.mp3"}
#         )
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Text to voice error: {str(e)}")

# # ======== Дополнительные endpoint'ы ========
# @app.get("/api/sessions")
# async def list_sessions():
#     """Список активных сессий"""
#     return {
#         "active_sessions": len(interview_sessions),
#         "sessions": list(interview_sessions.keys())
#     }

# @app.delete("/api/clear-sessions")
# async def clear_sessions():
#     """Очистка всех сессий"""
#     global interview_sessions
#     count = len(interview_sessions)
#     interview_sessions = {}
#     return {"message": f"Cleared {count} sessions"}

# # ======== Запуск приложения ========
# if __name__ == "__main__":
#     import uvicorn
#     port = int(os.environ.get("PORT", 8000))
#     uvicorn.run(app, host="0.0.0.0", port=port)


# backend/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API работает!"}

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)