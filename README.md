# Resume Maker Clean

Resume Maker Clean is a **full-stack web application** that allows users to create **ATS-friendly resumes** using a structured form and live preview.  
The project follows a **clean separation of frontend and backend**, using **Python (Flask)** for server-side logic and **HTML, CSS, and JavaScript** for the UI.

This project is suitable for academic submissions, portfolio projects, and further extension into a production-ready resume builder.

---

## 🚀 Features

- Resume creation using structured input
- Clean and ATS-friendly resume templates
- Frontend built with HTML, CSS, and JavaScript
- Backend powered by Python (Flask architecture)
- Modular and scalable project structure
- Environment-based configuration support

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript (Vanilla)

### Backend
- Python
- Flask (app-based architecture)

### Tools
- Git & GitHub
- Virtual Environment (`venv`)

---

## 📂 Project Structure

resume-maker-clean/
│
├── FSD/ # Frontend Static Directory

│ ├── HTML/ # HTML pages

│ ├── CSS/ # Stylesheets

│ ├── JS/ # JavaScript files

│ ├── IMG/ # Images & assets

│ └── templates/ # HTML templates used by Flask

│
├── Python/ # Backend source code

│ ├── config/ # Configuration files

│ ├── Controller/ # Route controllers

│ ├── services/ # Business logic

│ ├── repo/ # Data access layer

│ ├── DTO/ # Data Transfer Objects

│ ├── utils/ # Utility helpers

│ └── logs/ # Backend logs

│
├── admin/ # Admin-related modules (if applicable)

├── logs/ # Application logs

│
├── app.py # Flask app initialization

├── run.py # Application entry point

├── test.py # General testing

├── test_openai.py # OpenAI/API testing file

│
├── .env # Environment variables

├── requirements.txt # Python dependencies

├── .gitignore

└── README.md


---

## 🔧 Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/mihir021/resume-maker-.git
cd resume-maker-clean
2️⃣ Create Virtual Environment
python -m venv venv
Activate it:

Windows

venv\Scripts\activate
Linux / macOS

source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run the Application
python run.py
The application will start on:

http://localhost:5000
🌐 Frontend Usage
HTML files are located in FSD/HTML

CSS files are in FSD/CSS

JavaScript files are in FSD/JS

Templates used by Flask are in FSD/templates

🧪 Testing
test.py → General backend testing

test_openai.py → API/OpenAI testing (if configured)

🔐 Environment Variables
Create a .env file in the root directory and define required variables:

FLASK_ENV=development
SECRET_KEY=your_secret_key
🤝 Contributing
Fork the repository

Create a feature branch

git checkout -b feature/your-feature
Commit your changes

git commit -m "Add new feature"
Push and open a Pull Request

📄 License
This project is licensed under the MIT License.
