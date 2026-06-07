#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from services.gemini_service import ask_chatbot, generate_summary, generate_quiz

def test_chatbot():
    print("=" * 60)
    print("TEST 1: Chatbot - Apa itu Machine Learning?")
    print("=" * 60)
    try:
        answer = ask_chatbot("Apa itu Machine Learning?")
        print(f"✓ Jawaban: {answer[:200]}...")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_summary():
    print("\n" + "=" * 60)
    print("TEST 2: Summary Generation")
    print("=" * 60)
    sample_text = "Machine learning adalah cabang dari artificial intelligence yang memungkinkan komputer untuk belajar dari data tanpa diprogram secara eksplisit. Algoritma machine learning dapat menemukan pola dalam data dan membuat prediksi berdasarkan pola tersebut."
    try:
        summary = generate_summary(sample_text)
        print(f"✓ Ringkasan: {summary[:200]}...")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_quiz():
    print("\n" + "=" * 60)
    print("TEST 3: Quiz Generation")
    print("=" * 60)
    sample_text = "Python adalah bahasa pemrograman tingkat tinggi yang mudah dipelajari. Python digunakan dalam berbagai aplikasi termasuk web development, data science, dan machine learning."
    try:
        quiz = generate_quiz(sample_text)
        print(f"✓ Quiz: {quiz[:200]}...")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("\nTesting EduGenZ AI - Gemini Integration")
    print("=" * 60)
    
    results = {
        "Chatbot": test_chatbot(),
        "Summary": test_summary(),
        "Quiz": test_quiz(),
    }
    
    print("\n" + "=" * 60)
    print("HASIL TESTING")
    print("=" * 60)
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    print("=" * 60)
    if all_passed:
        print("✓ SEMUA TEST BERHASIL!")
    else:
        print("✗ ADA TEST YANG GAGAL")
    print("=" * 60)
