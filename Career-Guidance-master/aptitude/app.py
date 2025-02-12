from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Sample questions (You can extend this list)
questions = [
    {"question": "Do you enjoy solving logical puzzles?", "category": "Science"},
    {"question": "Do you like painting or designing?", "category": "Arts"},
    {"question": "Do you love coding and problem-solving?", "category": "Engineering"},
    {"question": "Are you interested in managing businesses?", "category": "Commerce"},
    {"question": "Do you like exploring new recipes?", "category": "Culinary Arts"}
]

career_paths = {
    "Science": "Consider Science Stream with focus on Engineering, Medicine, or Research.",
    "Arts": "You may opt for Arts Stream: Fine Arts, Design, or Literature.",
    "Engineering": "Engineering (CS, Mechanical, Civil) could be a great choice!",
    "Commerce": "Commerce can lead to careers in Finance, Business, or Economics.",
    "Culinary Arts": "Hospitality and Culinary Arts might be a good career option."
}

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/start-test')
def start_test():
    session['responses'] = []  # Reset responses
    return render_template("test.html", questions=random.sample(questions, len(questions)))

@app.route('/submit-test', methods=['POST'])
def submit_test():
    responses = request.json.get("responses", [])
    ssc_marks = int(request.json.get("ssc_marks", 0))
    
    category_scores = {}
    for response in responses:
        category = response["category"]
        if response["answer"]:
            category_scores[category] = category_scores.get(category, 0) + 1
    
    best_category = max(category_scores, key=category_scores.get, default="General Studies")
    
    # Career recommendation based on SSC marks
    if ssc_marks >= 85:
        recommendation = career_paths.get(best_category, "Explore various career options based on your interests.")
    elif 60 <= ssc_marks < 85:
        recommendation = "Consider a balanced approach with practical career choices."
    else:
        recommendation = "Explore skill-based courses or vocational training for better opportunities."
    
    return jsonify({"best_category": best_category, "recommendation": recommendation})

if __name__ == '__main__':
    app.run(debug=True)
