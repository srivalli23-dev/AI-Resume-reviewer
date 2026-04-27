from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from werkzeug.utils import secure_filename
import os
import PyPDF2
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'supersecretkey')
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_pdf(filepath):
    text = ''
    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ''
    return text

def generate_feedback(text, name, designation):
    # Default feedback system based on designation and content analysis
    positives = []
    recommendations = []
    
    # Basic content checks
    if len(text.split()) > 200:
        positives.append("Comprehensive content")
    else:
        recommendations.append("Add more detailed information")
        
    if any(tech in text.lower() for tech in ['python', 'java', 'javascript', 'c++', 'sql']):
        positives.append("Good technical skills highlighted")
    
    # Designation-specific feedback
    if designation.lower() == 'engineer':
        if any(word in text.lower() for word in ['project', 'developed', 'implemented']):
            positives.append("Project experience well documented")
        else:
            recommendations.append("Include more project details")
            
    elif designation.lower() == 'data analyst':
        if any(word in text.lower() for word in ['analysis', 'data', 'statistics']):
            positives.append("Relevant analytical skills mentioned")
        else:
            recommendations.append("Highlight data analysis experience")
            
    elif designation.lower() == 'doctor':
        if any(word in text.lower() for word in ['patient', 'clinical', 'medical']):
            positives.append("Clinical experience highlighted")
        else:
            recommendations.append("Add more healthcare-specific details")
            
    elif designation.lower() == 'ias aspirant':
        if any(word in text.lower() for word in ['public', 'policy', 'administration']):
            positives.append("Public service focus evident")
        else:
            recommendations.append("Include public administration experience")
    
    # Add default positive if none found
    if not positives:
        positives.append("Clear presentation")
    
    # Add default recommendation if none found
    if not recommendations:
        recommendations.append(f"Consider adding more {designation}-specific achievements")
    
    # Calculate efficiency score
    current_score = min(85, 55 + (len(positives) * 10))
    improved_score = min(95, current_score + 15)
    
    feedback = (
        f"Positives: {'; '.join(positives)}.\n"
        f"Recommendations: {'; '.join(recommendations)}.\n"
        f"Efficiency Score: {current_score} -> {improved_score}.\n"
        f"Conclusion: Shows potential, implement recommendations for improved impact."
    )
    
    return feedback

def details_match(text, name, designation):
    return name.lower() in text.lower() or designation.lower() in text.lower()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        designation = request.form['designation']
        file = request.files['resume']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            text = extract_text_from_pdf(filepath)
            session['name'] = name
            session['age'] = age
            session['designation'] = designation
            session['resume_text'] = text
            session['resume_file'] = filename
            
            if not details_match(text, name, designation):
                return redirect(url_for('feedback', mismatch=1))
            return redirect(url_for('feedback'))
        else:
            return render_template('index.html', error='Please upload a valid PDF file.')
    return render_template('index.html')

@app.route('/feedback')
def feedback():
    name = session.get('name')
    designation = session.get('designation')
    text = session.get('resume_text')
    mismatch = request.args.get('mismatch')
    
    if mismatch:
        return render_template('feedback.html', mismatch=True)
    
    feedback_text = generate_feedback(text, name, designation)
    
    # Parse feedback into sections
    parts = {'positives': '', 'recommendations': '', 'efficiency': '', 'conclusion': ''}
    for line in feedback_text.split('\n'):
        if line.lower().startswith('positives'):
            parts['positives'] = line.split(':',1)[-1].strip()
        elif line.lower().startswith('recommendations'):
            parts['recommendations'] = line.split(':',1)[-1].strip()
        elif line.lower().startswith('efficiency'):
            parts['efficiency'] = line.split(':',1)[-1].strip()
        elif line.lower().startswith('conclusion'):
            parts['conclusion'] = line.split(':',1)[-1].strip()
    
    return render_template('feedback.html', **parts, mismatch=False)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').lower()
    
    # Simple rule-based responses
    if any(word in user_message for word in ['resume', 'cv']):
        answer = f"You asked: {data.get('message')}\nA strong resume should be clear, concise, and highlight your most relevant achievements. Use action verbs and quantify your accomplishments where possible."
    
    elif any(word in user_message for word in ['job', 'career', 'work']):
        answer = f"You asked: {data.get('message')}\nConsider factors like work-life balance, growth opportunities, and company culture. Research companies on platforms like LinkedIn and Glassdoor."
    
    elif any(word in user_message for word in ['interview', 'hiring']):
        answer = f"You asked: {data.get('message')}\nPrepare by researching the company, practicing common questions, and preparing examples of your achievements. Remember the STAR method for behavioral questions."
    
    elif any(word in user_message for word in ['study', 'college', 'university']):
        answer = f"You asked: {data.get('message')}\nConsider factors like program reputation, course content, career opportunities, and location. Talk to alumni and current students if possible."
    
    else:
        answer = f"You asked: {data.get('message')}\nFor specific guidance on this topic, consider consulting career counselors or industry professionals who can provide detailed insights."
    
    return jsonify({'answer': answer})

if __name__ == '__main__':
    print("Starting Flask server...")
    try:
        app.run(debug=True, port=5000)
        print("Server is running at http://localhost:5000")
    except Exception as e:
        print(f"Error starting server: {e}")