import json
import re
import random


def parse_quiz_text(quiz_text):
    """
    Parse quiz text dari Gemini API ke format terstruktur
    Handles various formats including preamble
    """
    questions = []
    current_question = None
    current_options = {}
    correct_answer = None
    
    lines = quiz_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Deteksi nomor soal (Soal 1:, 1., **Soal 1:**, etc)
        # More lenient regex to catch various formats
        soal_match = re.match(r'^(\*+)?(?:Soal\s*)?(\d+)[.:\)]*(\*+)?[\s:]*(.+?)$', line)
        if soal_match and soal_match.group(4):
            # Simpan soal sebelumnya jika ada
            if current_question and current_options:
                current_question['options'] = current_options
                current_question['correct_answer'] = correct_answer
                questions.append(current_question)
            
            # Buat soal baru
            question_text = soal_match.group(4).strip()
            # Hapus tanda tanya di akhir jika ada
            question_text = question_text.rstrip('?')
            current_question = {
                'question': question_text,
                'options': {},
                'correct_answer': None
            }
            current_options = {}
            correct_answer = None
            continue
        
        # Deteksi pilihan (A), (B), (C), (D) atau A), B), atau A. B. etc
        # Handle both ) and . as separators, and optional parentheses
        option_match = re.match(r'^(\*+)?[)]?([A-D])[.)\s]*(\*+)?[\s]*(.+?)(\*+)?$', line)
        if option_match and option_match.group(4):
            option_key = option_match.group(2)
            option_text = option_match.group(4).strip()
            # Remove asterisks from text
            option_text = option_text.strip('*')
            current_options[option_key] = option_text
            continue
        
        # Cek jika ada indikasi jawaban benar
        # Format: Jawaban: A, Jawaban benar: B, Kunci: C, etc
        if any(keyword in line.lower() for keyword in ['jawaban', 'kunci', 'benar', 'answer']):
            # Extract jawaban jika ada huruf A-D
            match = re.search(r'[:\s]([A-D])[).\s]?$', line)
            if match:
                correct_answer = match.group(1)
    
    # Simpan soal terakhir
    if current_question and current_options:
        current_question['options'] = current_options
        current_question['correct_answer'] = correct_answer
        questions.append(current_question)
    
    return questions


def generate_random_correct_answers(questions):
    """
    Jika parsing tidak berhasil extract jawaban benar,
    generate secara random (untuk development/testing)
    """
    for q in questions:
        if not q.get('correct_answer'):
            q['correct_answer'] = random.choice(list(q.get('options', {}).keys()))
    return questions


def calculate_score(questions, answers):
    """
    Hitung score dari jawaban user
    answers: dict {question_index: answer_key}
    """
    total = len(questions)
    correct = 0
    
    for idx, question in enumerate(questions):
        user_answer = answers.get(str(idx))
        correct_answer = question.get('correct_answer')
        
        if user_answer == correct_answer:
            correct += 1
    
    percentage = (correct / total * 100) if total > 0 else 0
    
    return {
        'correct': correct,
        'total': total,
        'percentage': round(percentage, 1),
        'score': f"{correct}/{total}"
    }


def get_question_result(question, user_answer, index):
    """Get result untuk satu soal"""
    correct_answer = question.get('correct_answer')
    is_correct = user_answer == correct_answer
    
    return {
        'index': index,
        'question': question.get('question'),
        'user_answer': user_answer,
        'user_answer_text': question.get('options', {}).get(user_answer, ''),
        'correct_answer': correct_answer,
        'correct_answer_text': question.get('options', {}).get(correct_answer, ''),
        'is_correct': is_correct,
        'options': question.get('options', {})
    }


def get_badge_grade(percentage):
    """
    Return badge grade berdasarkan persentase
    """
    if percentage >= 85:
        return {'grade': 'A', 'color': 'success', 'label': 'Sempurna'}
    elif percentage >= 75:
        return {'grade': 'B', 'color': 'info', 'label': 'Baik'}
    elif percentage >= 65:
        return {'grade': 'C', 'color': 'warning', 'label': 'Cukup'}
    else:
        return {'grade': 'D', 'color': 'danger', 'label': 'Kurang'}


