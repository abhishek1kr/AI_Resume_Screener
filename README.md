# AI-Powered Resume Screener

An intelligent web application that helps recruiters automatically screen, parse, and rank resumes against job descriptions.

##  Key Features

- **Automated Resume Parsing**: Extracts text from PDF and DOCX formats.
- **Smart Skill Extraction**: Identifies technical skills using NLP usage patterns.
- **Semantic Matching**: Uses TF-IDF & Cosine Similarity to understand context, not just keywords.
- **Gap Analysis**: Automatically highlights skills missing from the candidate's profile.
- **Advanced Scoring**: Weighted system using Semantic Match (40%), Skill Overlap (40%), and Experience (20%).
- **Experience Classification**: Auto-detects Junior/Mid/Senior levels.
- **Job Fit Prediction**: Predicts probability of candidate fit (High/Moderate/Low).
- **Adaptive Feedback**: "Thumbs Up/Down" feedback system to collect data for future learning.
- **Bias-Reduced**: Evaluates candidates based purely on skills and match scores.
- **Multi-Resume Support**: Process dozens of resumes in seconds.
- **Interactive UI**: Clean, drag-and-drop interface for ease of use.

##  Technology Stack

- **Backend**: Python, Flask
- **NLP / ML**: scikit-learn, NLTK/Spacy (logic implemented with regex/set operations for speed), TF-IDF Vectorizer
- **Frontend**: HTML5, CSS3 (Modern Glassmorphism Design), JavaScript
- **File Handling**: PyPDF2, python-docx

##  Prerequisites

- Python 3.8+
- pip (Python Package Manager)

##  Installation

1. **Clone the repository** (or download files):
   ```bash
   git clone <repository-url>
   cd "mini project"
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access the UI**:
   Open you browser and navigate to: `http://127.0.0.1:5000`

##  How to Use

1. **Paste Job Description**: Copy the text of the job description into the dedicated text area.
2. **Upload Resumes**: Drag & drop multiple PDF or DOCX files into the upload zone.
3. **Analyze**: Click the "Analyze Resumes" button.
4. **View Results**: The candidates will be ranked by relevance score, with missing skills highlighted.

##  Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
