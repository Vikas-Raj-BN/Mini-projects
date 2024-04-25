import time

def run_quiz(questions):
    score = 0
    for question in questions:
        print(question["prompt"])
        for option in question["options"]:
            print(option)
        answer = input("Enter your answer (A, B, C, or D): ").upper()
        if answer == question["answer"]:
            print("Correct!\n")
            score += 1
        else:
            print("Wrong! The correct answer was", question["answer"], "\n")
    print(f"You got {score} out of {len(questions)} questions correct.")
    

# List of quiz questions. Each question is a dictionary.
questions = [
    {
        "prompt": "What does the acronym HTML stand for?",
        "options": ["A. Hyper Text Markup Language", "B. High Technical Markup Language", "C. Hyperlinks and Text Markup Language", "D. Home Tool Markup Language"],
        "answer": "A"
    },
    {
        "prompt": "Which of the following programming languages is used for creating dynamic and interactive web pages?",
        "options": ["A. Java", "B. Python", "C. JavaScript", "D. C++"],
        "answer": "C"
    },
    {
        "prompt": "What is the smallest prime number?",
        "options": ["A. 1", "B. 2", "C. 3", "D. 5"],
        "answer": "B"
    },
    {
        "prompt": "What does the term API stand for in the context of programming?",
        "options": ["A. Advanced Program Integration", "B. Application Programming Interface", "C. Automated Program Interaction", "D. Advanced Programming Interface"],
        "answer": "B"
    },
    {
        "prompt": "What does the term SQL stand for in the context of databases?",
        "options": ["A. Structured Query Language", "B. Sequential Query Language", "C. Standard Query Language", "D. Server Query Language"],
        "answer": "A"
    },
    {
        "prompt": "What does the acronym HTTP stand for in the context of web development?",
        "options": ["A. Hyper Text Transfer Protocol", "B. High Technical Transfer Protocol", "C. Home Tool Transfer Protocol", "D. Hyperlinks and Text Transfer Protocol"],
        "answer": "A"
    },
    {
        "prompt": "What does the acronym URL stand for in the context of web development?",
        "options": ["A. Universal Resource Locator", "B. Unified Resource Locator", "C. Uniform Resource Locator", "D. Unique Resource Locator"],
        "answer": "C"
    },
    {
        "prompt": "Which of the following is not a valid loop statement in Python?",
        "options": ["A. for", "B. while", "C. loop", "D. do-while"],
        "answer": "C"
    },
    {
        "prompt": "Which of the following is a popular version control system used in software development?",
        "options": ["A. SVN", "B. CVS", "C. Git", "D. Mercurial"],
        "answer": "C"
    },
    {
        "prompt": "Which of the following data structures follows the Last-In-First-Out (LIFO) principle?",
        "options": ["A. Queue", "B. Stack", "C. Linked List", "D. Array"],
        "answer": "B"
    },
]

# Run the quiz
run_quiz(questions)