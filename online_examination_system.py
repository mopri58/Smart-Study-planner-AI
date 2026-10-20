questions = [
    {"question": "Which keyword defines a function in Python?",
     "options": ["A. func", "B. def", "C. function", "D. define"], "answer": "B"},
    {"question": "Which data type stores True or False?",
     "options": ["A. int", "B. str", "C. bool", "D. list"], "answer": "C"},
    {"question": "Which symbol starts a comment in Python?",
     "options": ["A. //", "B. <!--", "C. #", "D. **"], "answer": "C"},
    {"question": "Which collection uses key-value pairs?",
     "options": ["A. tuple", "B. dictionary", "C. set", "D. string"], "answer": "B"},
    {"question": "What does len('cat') return?",
     "options": ["A. 2", "B. 3", "C. 4", "D. 0"], "answer": "B"}
]

print("=== Online Examination System ===")
student = input("Student name: ").strip() or "Student"
score = 0
for number, q in enumerate(questions, start=1):
    print(f"\\nQ{number}. {q['question']}")
    for option in q["options"]:
        print(option)
    answer = input("Your answer (A/B/C/D): ").strip().upper()
    if answer == q["answer"]:
        score += 1
print(f"\\nStudent: {student}")
print(f"Score: {score}/{len(questions)}")
print(f"Percentage: {score / len(questions) * 100:.1f}%")
if score >= 4:
    print("Result: Excellent")
elif score >= 3:
    print("Result: Pass")
else:
    print("Result: Keep practicing")
