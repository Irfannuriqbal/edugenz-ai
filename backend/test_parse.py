import sqlite3
from services.quiz_service import parse_quiz_text

conn = sqlite3.connect('database/app.db')
conn.row_factory = sqlite3.Row
quiz = conn.execute('SELECT id, quiz FROM quizzes WHERE id = 4').fetchone()

print("=== QUIZ DATA (first 1000 chars) ===")
print(quiz['quiz'][:1000])
print("\n=== PARSING ===")
questions = parse_quiz_text(quiz['quiz'])
print(f"Total questions parsed: {len(questions)}")
if questions:
    for i, q in enumerate(questions[:2]):
        print(f"\nQuestion {i+1}:")
        print(f"  Text: {q.get('question')[:60] if q.get('question') else 'NO TEXT'}...")
        print(f"  Options: {list(q.get('options', {}).keys())}")
        print(f"  Correct: {q.get('correct_answer')}")
else:
    print("NO QUESTIONS PARSED!")
