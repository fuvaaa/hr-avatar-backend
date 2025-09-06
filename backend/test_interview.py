#!/usr/bin/env python3
import sys
import os
import importlib
from dotenv import load_dotenv

load_dotenv()

print("🚀 ЗАПУСК ТЕСТА СИСТЕМЫ ИНТЕРВЬЮ")
print("=" * 50)
print(f"Текущая директория: {os.getcwd()}")
print(f"Python: {sys.executable}")

def test_basic():
    print("🔍 Базовый тест...")
    try:
        import PyPDF2
        print("✅ PyPDF2 установлен")
        return True
    except ImportError as e:
        print(f"❌ PyPDF2: {e}")
        return False

def test_docx():
    print("📄 Тест docx...")
    try:
        import docx
        print("✅ python-docx установлен")
        return True
    except ImportError as e:
        print(f"❌ docx: {e}")
        return False

def test_langchain():
    print("🤖 Тест LangChain...")
    try:
        import langchain_openai
        print("✅ langchain-openai установлен")
        return True
    except ImportError as e:
        print(f"❌ langchain: {e}")
        return False

def test_spacy():
    print("🔤 Тест spaCy...")
    try:
        import spacy
        print("✅ spaCy установлен")
        return True
    except ImportError as e:
        print(f"❌ spaCy: {e}")
        return False

def test_sklearn():
    print("📊 Тест scikit-learn...")
    try:
        import sklearn
        print("✅ scikit-learn установлен")
        return True
    except ImportError as e:
        print(f"❌ scikit-learn: {e}")
        return False

def test_openai_key():
    print("🔑 Тест OpenAI ключа...")
    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key:
        print(f"✅ OPENAI_API_KEY: {api_key[:10]}...")
        return True
    else:
        print("❌ OPENAI_API_KEY не найден")
        print("👉 Проверьте .env файл или export OPENAI_API_KEY='ваш_ключ'")
        return False

if __name__ == "__main__":
    print("Начинаем тестирование...\n")
    tests = [test_basic, test_docx, test_langchain, test_spacy, test_sklearn, test_openai_key]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    passed = sum(results)
    total = len(results)
    print("=" * 50)
    print(f"📊 РЕЗУЛЬТАТ: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Система готова к работе!")
    else:
        print("⚠️  Есть проблемы с настройкой. Решите указанные выше ошибки.")
    
    print("=" * 50)
