# 🎓 Career Guidance System

A comprehensive career guidance platform that helps students make informed decisions about their academic and professional paths. The system provides personalized stream and course recommendations based on academic performance, skills, and interests.

## 🌟 Features

### 1. Multi-Language Support
- Supports English, Hindi, Urdu, and Kashmiri
- Right-to-Left (RTL) language support for Urdu and Kashmiri
- Dynamic language switching with local storage persistence
- Automatic browser language detection

### 2. Stream Recommendation System
- Recommends Science (PCM/PCB), Commerce, or Arts streams for Class 10 students
- Considers academic performance in core subjects (Math, Science, English, etc.)
- Analyzes aptitudes and skills (logical reasoning, creativity, etc.)
- Provides detailed insights and justifications for recommendations

### 3. Course Recommendations
- Personalized course suggestions for Class 12 students
- Stream-specific recommendations (Science, Commerce, Arts, Vocational)
- Career path visualization for different educational routes
- Detailed course information and future prospects

### 4. Career Dashboard
- Personalized student dashboard with progress tracking
- Skill gap analysis and development recommendations
- Academic timeline and important deadline tracking
- Saved recommendations and favorite courses/institutions
- Progress visualization and achievement tracking

### 5. Institution Directory
- Comprehensive directory of colleges and schools
- Advanced filtering by:
  - Location (city, state, country)
  - Courses offered
  - Accreditation and ratings
  - Admission requirements
- Detailed institution profiles with:
  - Contact information
  - Courses and fees
  - Admission process
  - Campus facilities
  - Student reviews

### 6. E-Learning Resources
- Digital library of ebooks and study materials
- Subject-wise resource categorization
- Downloadable and online reading options
- Resource recommendations based on student's stream and interests

### 7. Timeline Tracker
- Academic milestone tracking
- Customizable task management
- Deadline reminders and notifications
- Progress visualization

### 8. Career Visualization Tools
- Interactive career path mapping
- Industry and job role exploration
- Salary expectations and job market trends
- Required qualifications and skill development paths

## 🛠️ Technical Stack

### Frontend
- **Core Technologies**
  - HTML5, CSS3, JavaScript (ES6+)
  - Bootstrap 5.1.3 for responsive design
  - Font Awesome 6.0 for icons
  - jQuery 3.6.0 for DOM manipulation
  - Chart.js for data visualizations
  - Popper.js for tooltips and popovers
  - DataTables for interactive tables

### Backend
- **Core Framework**
  - Python 3.8+
  - Flask 2.0.1 web framework
  - Flask-CORS for handling cross-origin requests
  - Jinja2 templating engine

- **Machine Learning & Data Processing**
  - Scikit-learn 1.0.2 for ML models
  - Pandas 1.3.4 for data manipulation
  - NumPy 1.21.4 for numerical operations
  - Joblib 1.1.0 for model persistence
  - Mistral AI for natural language processing

- **APIs & Integration**
  - RESTful API endpoints
  - JSON data exchange format
  - Axios for HTTP requests
  - Environment variable management using python-dotenv

- **Authentication & Security**
  - Session-based authentication
  - CSRF protection
  - Input validation and sanitization
  - Secure password hashing

### Machine Learning
- Random Forest Classifier for stream recommendations
- Feature scaling and label encoding
- Model persistence with joblib

## 📊 Dataset Directory Structure

### 1. Arts Dataset (`/Dataset/Arts_dataset/`)
- **Data Files**
  - `arts_courses_dataset.csv`: Core dataset containing arts courses and related attributes
  - `arts_courses_with_careers.csv`: Extended dataset mapping courses to career paths
  - `dataset.pkl`: Serialized dataset for quick loading
  - `feature_columns.pkl`: Saved feature columns for model inference

- **Models**
  - `course_classifier.pkl`: Trained classifier for arts course recommendations
  - `recommendation_system.pkl`: Saved recommendation system
  - `label_encoder.pkl`: Label encoder for categorical features
  - `scaler.pkl`: Feature scaler for model input

- **Application**
  - `app.py`: Main application file
  - `flask_app.py`: Flask web application for the arts module
  - `train.ipynb`: Jupyter notebook for model training
  - `requirements.txt`: Python dependencies

```
Career Guidance/
│
├── Dataset/                           # All stream-specific datasets and models
│   │
│   ├── Commerce_dataset/              # Commerce stream resources
│   │   ├── About the dataset.docx     # Documentation
│   │   ├── app.py                     # Main application file
│   │   ├── commerce_course_classifier.pkl  # Pre-trained classifier model
│   │   ├── commerce_courses_dataset.csv    # Main dataset in CSV format
│   │   ├── commerce_courses_with_careers.csv  # Career mapping data
│   │   ├── commerce_dataset.pkl       # Serialized dataset
│   │   ├── commerce_feature_columns.pkl   # Feature columns for the model
│   │   ├── commerce_label_encoder.pkl # Label encoder for categorical data
│   │   ├── commerce_scaler.pkl        # Feature scaler
│   │   ├── flask_app.py               # Flask web application
│   │   ├── run_commerce_app.bat       # Batch file to run the commerce app
│   │   ├── setup_and_run.bat          # Setup and execution batch file
│   │   ├── static/                    # Empty directory
│   │   ├── templates/                 # HTML templates
│   │   │   └── commerce_course_recommendation.html
│   │   └── train.ipynb                # Jupyter notebook for training
│   │
│   ├── Arts_dataset/                  # Arts stream resources
│   │   ├── About the dataset.docx     # Documentation
│   │   ├── app.py                     # Main application
│   │   ├── arts_courses_dataset.csv   # Main dataset
│   │   ├── arts_courses_with_careers.csv  # Career mapping
│   │   ├── course_classifier.pkl      # Classifier model
│   │   ├── dataset.pkl                # Serialized dataset
│   │   ├── feature_columns.pkl        # Feature columns
│   │   ├── flask_app.py               # Flask application
│   │   ├── label_encoder.pkl          # Label encoder
│   │   ├── recommendation_system.pkl  # Recommendation model
│   │   ├── requirements.txt           # Dependencies
│   │   ├── scaler.pkl                 # Feature scaler
│   │   ├── static/                    # Static files
│   │   │   └── arts_course_recommendation.html
│   │   └── train.ipynb                # Training notebook
│   │
│   ├── Vocational_dataset/            # Vocational training resources
│   │   ├── About the dataset.docx     # Documentation
│   │   ├── __pycache__/               # Python cache
│   │   ├── app.py                     # Main application
│   │   ├── flask_app.py               # Flask application
│   │   ├── run_vocational_app.bat     # Batch file to run the app
│   │   ├── static/                    # Empty directory
│   │   ├── templates/                 # HTML templates
│   │   │   └── vocational_recommendation.html
│   │   ├── train.ipynb                # Training notebook
│   │   ├── vocational_course_classifier.pkl  # Classifier model
│   │   ├── vocational_courses_dataset.csv    # Main dataset
│   │   ├── vocational_courses_with_careers.csv  # Career mapping
│   │   ├── vocational_dataset.pkl     # Serialized dataset
│   │   ├── vocational_feature_columns.pkl  # Feature columns
│   │   ├── vocational_label_encoder.pkl  # Label encoder
│   │   └── vocational_scaler.pkl      # Feature scaler
│   │
│   ├── pcb_dataset/                   # PCB stream resources (Physics, Chemistry, Biology)
│   │   ├── About the dataset.docx     # Documentation
│   │   ├── app.py                     # Main application
│   │   ├── flask_app.py               # Flask application
│   │   ├── pcb_course_classifier.pkl  # Classifier model
│   │   ├── pcb_courses_with_careers_single_option.csv  # Career mapping
│   │   ├── pcb_dataset.pkl            # Serialized dataset
│   │   ├── pcb_feature_columns.pkl    # Feature columns
│   │   ├── pcb_label_encoder.pkl      # Label encoder
│   │   ├── pcb_recommendation.html    # Recommendation page
│   │   ├── pcb_scaler.pkl             # Feature scaler
│   │   ├── static/                    # Empty directory
│   │   ├── templates/                 # HTML templates
│   │   │   └── pcb_recommendation.html
│   │   └── train.ipynb                # Training notebook
│   │
│   └── pcm_dataset/                   # PCM stream resources (Physics, Chemistry, Mathematics)
│       ├── About the dataset.docx     # Documentation
│       ├── app.py                     # Main application
│       ├── flask_app.py               # Flask application
│       ├── pcm_course_classifier.pkl  # Classifier model
│       ├── pcm_course_recommendation_dataset.csv  # Main dataset
│       ├── pcm_courses_with_careers.csv  # Career mapping
│       ├── pcm_dataset.pkl            # Serialized dataset
│       ├── pcm_feature_columns.pkl    # Feature columns
│       ├── pcm_label_encoder.pkl      # Label encoder
│       ├── pcm_scaler.pkl             # Feature scaler
│       ├── requirements.txt           # Dependencies
│       ├── static/                    # Empty directory
│       ├── templates/                 # HTML templates
│       │   └── pcm_recommendation.html
│       └── train.ipynb                # Training notebook
│
├── training/                         # Initial stream recommendation system
│   ├── 10_dataset.ipynb              # Jupyter notebook for training the model
│   ├── app.py                        # Main application file
│   ├── flask_app.py                  # Flask application file
│   ├── static/                       # Static files
│   │   └── css/                      # CSS stylesheets
│   │       └── styles.css            # Main stylesheet
│   ├── stream_label_encoder.pkl      # Label encoder for stream prediction
│   ├── stream_model.pkl              # Pre-trained stream prediction model
│   ├── stream_recommendation_dataset_2000.csv  # Dataset for stream recommendations
│   ├── stream_scaler.pkl             # Scaler for feature normalization
│   └── templates/                    # HTML templates
│       └── index.html                # Main web interface
│
├── career_env/                       # Python virtual environment
│
├── pkl_files/                        # Collection of pre-trained models (40+ models)
│   ├── career_path_model.pkl         # Career path prediction models
│   ├── career_predictor.pkl
│   ├── career_recommendation_model.pkl
│   ├── career_recommendation_system.pkl
│   ├── career_recommender.pkl
│   ├── career_stream_model.pkl
│   ├── career_stream_predictor.pkl
│   ├── career_suggestor.pkl
│   ├── career_system.pkl
│   ├── career_trends_model.pkl
│   ├── career_trends_predictor.pkl
│   ├── course_recommendation_model.pkl
│   ├── education_career_model.pkl
│   ├── education_career_predictor.pkl
│   ├── education_career_recommender.pkl
│   ├── education_career_system.pkl
│   ├── education_path_model.pkl
│   ├── education_path_predictor.pkl
│   ├── education_system.pkl
│   ├── job_market_model.pkl
│   ├── job_market_predictor.pkl
│   ├── job_market_system.pkl
│   ├── job_recommendation_model.pkl
│   ├── job_recommendation_system.pkl
│   ├── job_recommender.pkl
│   ├── job_skill_matcher.pkl
│   ├── job_skill_model.pkl
│   ├── job_skill_predictor.pkl
│   ├── job_skills_model.pkl
│   ├── job_skills_predictor.pkl
│   ├── job_trends_model.pkl
│   ├── job_trends_predictor.pkl
│   ├── job_trends_system.pkl
│   ├── occupation_predictor.pkl
│   ├── occupation_recommendation_model.pkl
│   ├── pathway_model.pkl
│   ├── pathway_predictor.pkl
│   ├── pathway_system.pkl
│   ├── personality_career_model.pkl
│   ├── personality_career_predictor.pkl
│   ├── personality_model.pkl
│   ├── personality_predictor.pkl
│   ├── personality_traits_model.pkl
│   └── personality_traits_predictor.pkl
│
├── static/                           # Static files (CSS, JS, images)
│   └── js/                           # JavaScript files
│
├── Career Path Visualization.docx    # Documentation
├── Mistral_Chatbot.py               # Main chatbot implementation
├── README.md                        # Project documentation
├── career_path_visualization.html   # Interactive career path visualization
├── dashboard.html                   # User dashboard
├── ebooks.html                      # E-books and resources
├── home.html                        # Landing page
├── institution_directory_fixed.html # Directory of educational institutions
├── jammu_kashmir_colleges.json      # College data in JSON format
├── prototype_flowchart.png          # Project flowchart/design
├── recommendation_hub.html          # Central hub for recommendations
├── requirements.txt                 # Python dependencies
├── school_directory.html            # School directory
├── stream_selection.html            # Stream selection interface
└── timeline_tracker.html            # Academic/career timeline tracker

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Node.js and npm (for frontend dependencies)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd career-guidance
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask application:
   ```bash
   cd training
   python flask_app.py
   ```

5. Open your browser and navigate to `http://localhost:5006`

## 🌐 Flask Applications and Ports

The Career Guidance System consists of multiple specialized Flask applications, each running on different ports:

### **Available Applications**

| **Application** | **Port** | **Access URL** | **Purpose** |
|----------------|----------|----------------|-------------|
| **Main Stream Predictor** | 5006 | `http://localhost:5006` | Stream recommendation (Science/Commerce/Arts) |
| **Commerce Courses** | 5001 | `http://localhost:5001` | Commerce stream course recommendations |
| **Arts Courses** | 5000 | `http://localhost:5000` | Arts stream course recommendations |
| **Vocational Training** | 5005 | `http://localhost:5005` | Vocational course recommendations |
| **PCB Stream** | 5002 | `http://localhost:5002` | Physics, Chemistry, Biology courses |
| **PCM Stream** | 5003 | `http://localhost:5003` | Physics, Chemistry, Mathematics courses |

### **Running Multiple Applications**

To run all applications simultaneously, open separate terminal windows:

```bash
# Terminal 1 - Main Application
cd training
python flask_app.py

# Terminal 2 - Commerce
cd Dataset/Commerce_dataset
python flask_app.py

# Terminal 3 - Arts
cd Dataset/Arts_dataset
python flask_app.py

# Terminal 4 - Vocational
cd Dataset/Vocational_dataset
python flask_app.py

# Terminal 5 - PCB
cd Dataset/pcb_dataset
python flask_app.py

# Terminal 6 - PCM
cd Dataset/pcm_dataset
python flask_app.py
```

### **Quick Access**
- **Stream Selection**: http://localhost:5006
- **Course Recommendations**: http://localhost:5000 - 5003
- **Institution Directory**: Available through main interfaces
- **Career Dashboard**: Accessible via recommendation interfaces

## 🌐 Complete Website Flow & User Journey

The Career Guidance System provides a comprehensive, multi-phase user experience designed to guide students from initial assessment through ongoing career development support.

### **Phase 1: Onboarding & Information Collection**

#### **1. Home Page (`home.html`) - Entry Point**
- **Purpose**: Student information collection and system entry
- **Multi-language Support**: English, Hindi, Urdu, Kashmiri (with RTL support)
- **Data Collection**:
  - Personal Information (Name, Email, Phone, Address)
  - Form validation with real-time feedback
  - Local storage integration for user data persistence
- **Flow**: After submission → Redirects to `recommendation_hub.html`

### **Phase 2: Academic Level Selection**

#### **2. Recommendation Hub (`recommendation_hub.html`) - Main Navigation**
- **Purpose**: Academic level selection and central navigation hub
- **Sidebar Navigation**:
  - Dashboard, Career Recommendations, Top Colleges
  - Recommended Courses, College Directory, School Directory
  - E-Books Library, Timeline Tracker
- **Academic Level Selection**:
  - **Class 10 Students**: Stream recommendation path
  - **Class 12 Students**: Course recommendation path
- **Flow Logic**:
  - Class 10 → `training/templates/index.html` (Stream assessment)
  - Class 12 → `stream_selection.html` (Course selection by stream)

### **Phase 3: Stream & Course Recommendations**

#### **3. Stream Selection (`stream_selection.html`) - For Class 12 Students**
- **Stream Options**:
  - **Science (PCM)**: Physics, Chemistry, Mathematics
  - **Science (PCB)**: Physics, Chemistry, Biology
  - **Commerce**: Accountancy, Business Studies, Economics
  - **Arts/Humanities**: History, Political Science, Psychology
  - **Vocational**: Skill-based professional courses
- **Visual Design**: Card-based layout with images and descriptions
- **Flow**: After selection → Stream-specific recommendation pages

#### **4. Stream Assessment (`training/templates/index.html`) - For Class 10 Students**
- **Comprehensive Assessment**:
  - **Academic Performance**: Mathematics, Science, Biology, English, Social Studies, Language
  - **Aptitude & Skills**: Logical Reasoning, Analytical Skills, Numerical Ability, Creativity, Communication, Artistic Skills, Practical Skills
- **Interactive Sliders**: Real-time value display (0-100%)
- **AI Integration**: Mistral AI for personalized insights and follow-up questions
- **Results Display**: Charts showing stream match percentages with detailed explanations

### **Phase 4: Stream-Specific Course Recommendations**

#### **5. Course Recommendation Pages** - Stream-Specific
Each educational stream has its dedicated recommendation interface:

- **Commerce** (`Dataset/Commerce_dataset/templates/commerce_course_recommendation_.html`)
- **Arts** (`Dataset/Arts_dataset/static/arts_course_recommendation.html`)
- **Vocational** (`Dataset/Vocational_dataset/templates/vocational_recommendation.html`)
- **PCB** (`Dataset/pcb_dataset/templates/pcb_recommendation.html`)
- **PCM** (`Dataset/pcm_dataset/templates/pcm_recommendation.html`)

**Common Features**:
- Subject-wise skill assessment sliders with real-time feedback
- Course similarity scoring and ranking
- Career option mapping for each recommended course
- Visual charts and progress indicators
- Personalized recommendations based on user profile

### **Phase 5: Dashboard & Progress Tracking**

#### **6. Dashboard (`dashboard.html`) - Central Hub**
- **Personalized Welcome**: User-specific greeting and progress overview
- **Progress Tracking**:
  - Career Readiness Score with visual indicators
  - Active Courses Count and completion status
  - Upcoming Deadlines with calendar integration
  - Skills Mastered counter and development tracking
- **Recommendations Display**:
  - Top Recommended Streams with match percentages
  - Learning Path Progress with milestone tracking
  - Career Matches with salary ranges and growth potential
  - Skill Gap Analysis with development suggestions
- **Calendar Integration**: Important deadlines and events with visual timeline

### **Phase 6: Supporting Features & Resources**

#### **7. Institution Directory (`institution_directory_fixed.html`)**
- **Comprehensive Database**: 1000+ colleges and educational institutions
- **Advanced Filtering**:
  - Location-based search (city, state, country)
  - Course availability and specializations
  - Accreditation ratings (NAAC grades)
  - Admission requirements and eligibility criteria
- **Detailed Profiles**: Contact info, courses, facilities, fees, student reviews
- **Visual Cards**: Image galleries and interactive rating systems

#### **8. E-Learning Resources (`ebooks.html`)**
- **Digital Library**: Comprehensive collection organized by educational streams
- **Subject-wise Organization**: Resources categorized by stream and subject
- **Multiple Formats**: Downloadable PDFs and online reading options
- **Personalized Recommendations**: Resource suggestions based on user profiles
- **Stream-Specific Content**: Tailored materials for different educational paths

#### **9. Timeline Tracker (`timeline_tracker.html`)**
- **Academic Milestones**: Important deadlines and events tracking
- **Task Management**: Customizable task creation and progress monitoring
- **Progress Visualization**: Visual timeline of academic journey
- **Reminder System**: Smart notifications for important dates
- **Goal Setting**: Academic and career goal tracking with progress indicators

#### **10. Career Path Visualization (`career_path_visualization.html`)**
- **Interactive Mapping**: Visual representation of career progression paths
- **Industry Exploration**: Job role and industry information with requirements
- **Market Intelligence**: Salary expectations and job market trends
- **Skill Development**: Required qualifications and learning path suggestions
- **Career Trajectory**: Long-term career planning with milestone tracking

### **Phase 7: AI-Powered Support & Integration**

#### **11. AI Career Advisor (Integrated throughout)**
- **Mistral AI Integration**: Advanced NLP for personalized career guidance
- **Context-Aware Responses**: Based on complete user profile and interaction history
- **Multi-language Support**: Conversational interface in 4 languages
- **Personalized Recommendations**: Tailored advice considering academic performance, interests, and goals
- **Follow-up Support**: Continuous guidance through career development journey

## 🔄 **Complete User Flow Summary**

```
1. Landing → 2. Information Collection → 3. Academic Level Selection
         ↓
4. Stream Selection (Class 12) OR Stream Assessment (Class 10)
         ↓
5. Course Recommendations (Stream-specific with AI insights)
         ↓
6. Dashboard (Progress tracking and ongoing recommendations)
         ↓
7. Supporting Features (Institution search, resources, timeline)
         ↓
8. Continuous AI Support and Career Development
```

## 🎨 **Design & User Experience Features**

- **Consistent Visual Language**: Purple/blue gradient theme with modern animations
- **Multi-language Support**: 4 languages with RTL support for Urdu/Kashmiri
- **Responsive Design**: Mobile-first approach with progressive enhancement
- **Interactive Elements**: Hover effects, smooth animations, and real-time feedback
- **Accessibility**: WCAG compliant with proper ARIA labels and keyboard navigation
- **Progressive Enhancement**: Core functionality works without JavaScript, enhanced with it

## 🔗 **Technical Integration & Architecture**

- **Modular Architecture**: Each stream has independent Flask applications (5000-5006 ports)
- **Centralized AI**: Mistral AI integrated across all recommendation interfaces
- **Cross-Application Navigation**: Seamless flow between different tools and features
- **Real-time Updates**: Dynamic content loading and state management
- **Data Persistence**: Local storage for user preferences and progress tracking
- **API Integration**: RESTful endpoints for data exchange between components

This comprehensive flow ensures users receive **personalized, step-by-step career guidance** from initial assessment through ongoing support, creating a complete ecosystem for educational and career development! 🚀

## 🤖 Machine Learning Model

The recommendation system uses a Random Forest Classifier trained on student performance data. The model takes into account:

### Academic Performance
- Mathematics
- Science (Physics + Chemistry)
- Biology
- English
- Social Studies
- Second Language

### Aptitudes & Skills
- Logical Reasoning
- Analytical Skills
- Numerical Ability
- Creativity
- Communication Skills
- Artistic Skills
- Practical Skills

## 🌐 API Endpoints

- `GET /` - Main application interface
- `POST /predict` - Get stream recommendations
- `POST /insights` - Get AI-powered career insights

## 📊 Data Sources

- Student academic performance data
- Career path information
- Institution databases
- Course catalogs

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Educational institutions for providing data
- Open-source contributors for libraries and frameworks
- The development team for their hard work and dedication

## 📞 Contact

For support or inquiries, please contact [shubhammallick678@gmail.com](mailto:your-email@example.com).

---

<div align="center">
  Made with ❤️ by the Career Guidance Team
</div>
