import os
import json
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from utils import (
    extract_text_from_pdf, extract_text_from_docx, extract_skills, 
    calculate_weighted_score, predict_job_fit, extract_experience, 
    classify_experience_level
)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
FEEDBACK_FILE = 'feedback.json'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'job_description' not in request.form:
        return jsonify({'error': 'Missing Job Description'}), 400
    
    jd = request.form['job_description']
    files = request.files.getlist('resumes')
    
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files uploaded'}), 400

    results = []
    jd_skills = extract_skills(jd)

    for f in files:
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            f.save(path)

            try:
                text = ""
                if filename.endswith('.pdf'):
                    text = extract_text_from_pdf(path)
                elif filename.endswith('.docx'):
                    text = extract_text_from_docx(path)
                
                if not text: continue

                res_skills = extract_skills(text)
                exp_years = extract_experience(text)
                exp_level = classify_experience_level(exp_years)
                
                score = calculate_weighted_score(jd, text, res_skills, jd_skills, exp_years)
                fit = predict_job_fit(score)
                
                missing = [s for s in jd_skills if s not in res_skills]

                results.append({
                    'filename': filename,
                    'score': score,
                    'experience_years': exp_years,
                    'experience_level': exp_level,
                    'job_fit': fit,
                    'skills': res_skills,
                    'missing_skills': missing
                })

            except Exception as e:
                print(f"Error: {e}")
            finally:
                if os.path.exists(path):
                    os.remove(path)

    results.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({'results': results})

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    entry = {'filename': data.get('filename'), 'rating': data.get('rating')}
    
    history = []
    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, 'r') as f:
                history = json.load(f)
        except: pass
    
    history.append(entry)
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(history, f, indent=4)
        
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)
