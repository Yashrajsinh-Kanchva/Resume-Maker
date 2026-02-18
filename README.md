# 📄 Resume Maker - Professional Resume Builder

A **full-stack web application** for creating **ATS-friendly resumes** with AI-powered features, multiple professional templates, and comprehensive resume analysis tools. Built with Flask and modern web technologies.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-4.16.0-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ Features

### 🎨 Resume Creation
- **18+ Professional Templates** - Choose from modern, elegant, academic, and creative designs
- **Step-by-Step Builder** - Intuitive multi-step form for easy resume creation
- **Live Preview** - Real-time preview of your resume as you build
- **PDF Export** - Download your resume as a high-quality PDF
- **Resume Management** - Save, edit, and manage multiple resumes
- **Custom Sections** - Add custom sections like projects, awards, publications

### 🤖 AI-Powered Features
- **AI Resume Generator** - Generate professional resumes using OpenAI GPT
- **Smart Resume Scoring** - Get instant feedback on resume quality
- **ATS Score Checker** - Analyze resume compatibility with Applicant Tracking Systems
- **Keyword Matching** - Advanced TF-IDF and word overlap analysis
- **AI Suggestions** - Get personalized improvement recommendations

### 🔍 ATS Analysis
- **Keyword Similarity** - Compare resume keywords with job descriptions
- **Structure Analysis** - Verify required sections are present
- **Formatting Check** - Detect ATS-unfriendly formatting issues
- **Missing Keywords** - Identify important keywords to add
- **Improvement Suggestions** - Actionable tips to boost ATS compatibility

### 👤 User Management
- **User Authentication** - Secure signup and login system
- **Google OAuth** - Quick sign-in with Google account
- **Password Recovery** - Forgot password functionality with email verification
- **Session Management** - Secure session handling
- **User Dashboard** - Manage all your resumes in one place

### 🛡️ Admin Panel
- **Streamlit Admin Dashboard** - Comprehensive admin interface
- **User Management** - View, block, and manage users
- **Resume Analytics** - Track resume creation statistics
- **System Logs** - Monitor application activity
- **AI Chatbot** - Admin support chatbot powered by OpenAI
- **Data Export** - Export user and resume data to CSV

### 🎯 Additional Features
- **Resume Ranking** - Automatic ranking based on completeness
- **Skill Suggestions** - AI-powered skill recommendations
- **Contact Form** - Email support functionality
- **Responsive Design** - Works seamlessly on desktop and mobile
- **Dark Theme** - Modern dark UI with neon accents

---

## 🛠️ Tech Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with custom properties and animations
- **JavaScript (Vanilla)** - No framework dependencies
- **Bootstrap Icons** - Icon library
- **jsPDF** - PDF generation
- **html2canvas** - Screenshot capture for PDF

### Backend
- **Python 3.8+** - Core programming language
- **Flask 3.1.2** - Web framework
- **MongoDB** - NoSQL database (via PyMongo)
- **Redis** - Caching and session storage
- **JWT** - Token-based authentication

### AI & ML
- **OpenAI GPT** - AI resume generation and suggestions
- **spaCy** - Natural language processing
- **scikit-learn** - TF-IDF vectorization and cosine similarity
- **NLP** - Keyword extraction and analysis

### Additional Libraries
- **pdfplumber** - PDF text extraction
- **Flask-CORS** - Cross-origin resource sharing
- **Flask-Mail** - Email functionality
- **Authlib** - OAuth integration
- **python-dotenv** - Environment variable management
- **Streamlit** - Admin dashboard framework

### Development Tools
- **Git** - Version control
- **Virtual Environment** - Python dependency isolation
- **Logging** - Comprehensive logging system

---

## 📂 Project Structure

```
resume-maker-clean/
│
├── FSD/                          # Frontend Static Directory
│   ├── HTML/                     # HTML pages
│   │   ├── loginPage.html
│   │   ├── signUp.html
│   │   ├── documents.html       # Resume management
│   │   ├── step-1.html          # Personal info
│   │   ├── step-2.html          # Education
│   │   ├── step-3.html          # Experience
│   │   ├── step-4.html          # Skills
│   │   └── choose-template.html
│   │
│   ├── CSS/                      # Stylesheets
│   │   ├── main.css
│   │   ├── documents.css
│   │   └── step-*.css
│   │
│   ├── JS/                       # JavaScript files
│   │   ├── documents.js
│   │   ├── step-*.js
│   │   └── build-resume.js
│   │
│   ├── IMG/                      # Images & assets
│   │
│   └── templates/                # Resume templates (18+)
│       ├── template-academic-yellow/
│       ├── template-blue-corporate/
│       ├── template-dark-elegant/
│       ├── template-glassmorphism/
│       └── ... (15 more templates)
│
├── Python/                       # Backend source code
│   ├── config/                   # Configuration files
│   │   ├── app_config.py
│   │   ├── db.py                 # MongoDB connection
│   │   └── redis_config.py
│   │
│   ├── Controller/               # Route controllers
│   │   ├── user_controller.py
│   │   ├── resume_controller.py
│   │   ├── ats_controller.py
│   │   ├── ai_resume_controller.py
│   │   └── admin_controller.py
│   │
│   ├── services/                 # Business logic layer
│   │   ├── resume_service.py
│   │   ├── user_service.py
│   │   ├── ats_checker_service.py
│   │   ├── ai_resume_service.py
│   │   └── resume_score_service.py
│   │
│   ├── repo/                     # Data access layer
│   │   ├── user_repo.py
│   │   └── resume_repo.py
│   │
│   ├── DTO/                      # Data Transfer Objects
│   │
│   ├── utils/                    # Utility helpers
│   │   ├── logger.py
│   │   ├── crypto_utils.py
│   │   └── mail_utils.py
│   │
│   ├── ai/                       # AI-related modules
│   │   ├── resume_generator.py
│   │   └── prompts.py
│   │
│   ├── api/                      # API endpoints
│   │   └── admin/
│   │       └── chatbot.py
│   │
│   ├── logs/                     # Application logs
│   │
│   ├── app.py                    # Flask app factory
│   └── run.py                    # Application entry point
│
├── admin/                        # Admin panel (Streamlit)
│   ├── admin_app.py
│   └── sections/
│       ├── dashboard.py
│       ├── users.py
│       ├── resumes.py
│       ├── analytics.py
│       ├── chatbot.py
│       └── system.py
│
├── .env                          # Environment variables (create this)
├── .gitignore
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── ATS_SETUP.md                  # ATS checker setup guide
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** installed
- **MongoDB** running locally or connection string
- **Redis** server (optional, for caching)
- **OpenAI API Key** (optional, for AI features)

### Installation Steps

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/mihir021/resume-maker-.git
cd resume-maker-clean
```

#### 2️⃣ Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4️⃣ Install spaCy Model (Required for ATS Checker)

```bash
python -m spacy download en_core_web_sm
```

#### 5️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your_secret_key_here_min_32_chars

# Database
MONGODB_URI=mongodb://localhost:27017/resume_maker

# Redis (Optional)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# OpenAI (Optional - for AI features)
OPENAI_API_KEY=your_openai_api_key

# Email Configuration (Optional)
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
```

#### 6️⃣ Run the Application

**Main Application:**
```bash
python run.py
```

**Admin Panel (Separate Terminal):**
```bash
streamlit run admin/admin_app.py
```

The application will be available at:
- **Main App:** http://localhost:5000
- **Admin Panel:** http://localhost:8501

---

## 🔧 Configuration

### MongoDB Setup

1. Install MongoDB locally or use MongoDB Atlas (cloud)
2. Update `MONGODB_URI` in `.env` file
3. Default database name: `resume_maker`

### Redis Setup (Optional)

Redis is used for caching and session management. If not available, the app will continue without it.

**Install Redis:**
- **Windows:** Download from https://redis.io/download
- **Linux:** `sudo apt-get install redis-server`
- **macOS:** `brew install redis`

### OpenAI Setup (Optional)

AI features require an OpenAI API key:

1. Sign up at https://platform.openai.com
2. Get your API key from https://platform.openai.com/api-keys
3. Add to `.env` file: `OPENAI_API_KEY=sk-...`

**Features that require OpenAI:**
- AI Resume Generator
- AI-powered improvement suggestions
- Admin chatbot

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `http://localhost:5000/api/google/callback`
6. Copy Client ID and Secret to `.env`

---

## 📖 Usage Guide

### Creating a Resume

1. **Sign Up / Login** - Create an account or sign in with Google
2. **Choose Template** - Select from 18+ professional templates
3. **Fill Personal Info** - Name, title, contact details, summary
4. **Add Education** - Degree, institution, field of study
5. **Add Experience** - Job titles, companies, descriptions
6. **Add Skills** - Technical and soft skills
7. **Preview & Download** - Review and export as PDF

### Using AI Resume Generator

1. Click **"Create with AI"** button
2. Enter job role and description
3. Fill in your personal information
4. Select experience level
5. AI will generate a professional resume
6. Review and save

### ATS Score Checker

1. Click **"ATS Score Checker"** button
2. Select a saved resume
3. Paste the job description
4. Click **"Check ATS Score"**
5. Review:
   - Overall ATS score (0-100)
   - Keyword match percentage
   - Missing keywords
   - Structure analysis
   - Formatting issues
   - Improvement suggestions

### Admin Panel

1. Run Streamlit admin app: `streamlit run admin/admin_app.py`
2. Access at http://localhost:8501
3. Features:
   - View all users and resumes
   - Block/unblock users
   - View analytics and statistics
   - Chat with AI assistant
   - Export data to CSV
   - View system logs

---

## 🧪 Testing

### Backend Testing

```bash
python test.py
```

### OpenAI API Testing

```bash
python test_openai.py
```

### Manual Testing

1. Test user registration and login
2. Create a sample resume
3. Test PDF download
4. Test ATS checker with a job description
5. Test AI resume generator

---

## 🔐 Security Features

- **Password Hashing** - Bcrypt password encryption
- **Session Security** - Secure session cookies
- **CORS Protection** - Configured CORS policies
- **Input Validation** - Server-side validation
- **SQL Injection Protection** - Using parameterized queries (MongoDB)
- **XSS Protection** - Input sanitization
- **CSRF Protection** - Session-based CSRF tokens

---

## 📊 API Endpoints

### User Endpoints
- `POST /api/users/signup` - User registration
- `POST /api/users/login` - User login
- `GET /api/users/profile` - Get user profile
- `POST /api/users/logout` - User logout

### Resume Endpoints
- `GET /api/resumes` - Get all user resumes
- `POST /api/resumes` - Create new resume
- `GET /api/resumes/:id` - Get resume by ID
- `PUT /api/resumes/:id` - Update resume
- `DELETE /api/resumes/:id` - Delete resume

### AI Resume Endpoints
- `POST /api/ai-resume/create` - Generate AI resume

### ATS Checker Endpoints
- `POST /api/ats/check` - Check resume from PDF
- `POST /api/ats/check-from-resume` - Check saved resume

### Admin Endpoints
- `GET /api/admin/users` - Get all users
- `POST /api/admin/users/:id/block` - Block user
- `GET /api/admin/resumes` - Get all resumes
- `GET /api/admin/analytics` - Get analytics

---

## 🎨 Available Templates

1. **Academic Yellow** - Perfect for academic positions
2. **Blue Corporate** - Professional corporate style
3. **Dark Elegant** - Modern dark theme
4. **Glassmorphism** - Trendy glass effect design
5. **Timeline Resume** - Chronological layout
6. **Tech Look** - Technology-focused design
7. **Ultra Clean** - Minimalist and clean
8. **Classic Serif** - Traditional professional
9. **Card Based** - Card-style layout
10. **Infographic** - Visual and creative
11. **Bold Red Accent** - Eye-catching red accents
12. **Soft Green Minimal** - Subtle green theme
13. **Split Header Modern** - Modern split design
14. **Fresh Gradient** - Colorful gradients
15. **Box Shadow** - Depth with shadows
16. **Ultra Minimal** - Maximum simplicity
17. **Modern Clean** - Contemporary clean design
18. **Clean Profile** - Profile-focused layout

---

## 🐛 Troubleshooting

### Common Issues

**Issue: MongoDB connection error**
- Ensure MongoDB is running
- Check `MONGODB_URI` in `.env`
- Verify network connectivity

**Issue: Redis connection error**
- Redis is optional - app works without it
- Check Redis server is running if needed
- Verify `REDIS_HOST` and `REDIS_PORT` in `.env`

**Issue: spaCy model not found**
```bash
python -m spacy download en_core_web_sm
```

**Issue: OpenAI API errors**
- Verify API key in `.env`
- Check API quota and billing
- Ensure internet connection

**Issue: PDF generation fails**
- Check browser console for errors
- Ensure jsPDF library is loaded
- Try different browser

**Issue: OAuth not working**
- Verify Google OAuth credentials
- Check redirect URI matches exactly
- Ensure OAuth consent screen is configured

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed
4. **Commit your changes**
   ```bash
   git commit -m "Add: Description of your feature"
   ```
5. **Push to your branch**
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request**
   - Describe your changes
   - Reference any related issues
   - Add screenshots if UI changes

### Code Style

- Use meaningful variable names
- Add docstrings to functions
- Follow PEP 8 for Python code
- Use consistent indentation (4 spaces)
- Comment complex logic

---

## 📝 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** - For GPT API powering AI features
- **spaCy** - For NLP capabilities
- **scikit-learn** - For ML algorithms
- **Flask** - For the web framework
- **MongoDB** - For database
- **Bootstrap Icons** - For icon library
- **jsPDF** - For PDF generation

---

## 📧 Support

For issues, questions, or contributions:

- **GitHub Issues:** [Create an issue](https://github.com/mihir021/resume-maker-/issues)
- **Email:** [Your email here]

---

## 🗺️ Roadmap

- [ ] Multi-language support
- [ ] Resume sharing via link
- [ ] Cover letter generator
- [ ] Resume templates marketplace
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Integration with job boards
- [ ] Resume versioning system
- [ ] Collaborative editing
- [ ] Video resume support

---

**Made with ❤️ for job seekers worldwide**

*Last updated: February 2026*
