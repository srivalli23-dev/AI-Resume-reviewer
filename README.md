# AI Resume Reviewer & Student Guide Platform

## Project Overview
A modern, student-friendly web platform that reviews resumes, provides career guidance, and features an AI-powered chat assistant. Built with Flask (Python) backend and HTML/CSS/JS frontend.

## Features
- Animated landing page with gradient background and floating bubbles
- Resume upload (PDF only) with feedback (positives, recommendations, efficiency score, conclusion)
- Profession-specific recommendations
- Details mismatch detection
- Persistent chatbox ("Resume Guider") for career and resume questions
- Responsive, mobile-friendly design

## Tech Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- PDF Parsing: PyPDF2
- AI/Chat: OpenAI API (if available)

## How to Run
1. Install Python 3.8+
2. Create a virtual environment and activate it
3. Install dependencies: `pip install -r requirements.txt`
4. Run the Flask app: `python app.py`
5. Open `http://localhost:5000` in your browser

## Notes
- Replace OpenAI API key placeholder in `.env` if using AI features.
- All static assets are in the `static/` folder.
- Templates are in the `templates/` folder.

---
