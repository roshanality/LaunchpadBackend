from dotenv import load_dotenv  # type: ignore
load_dotenv()
from flask import Flask, request, jsonify, send_from_directory  # type: ignore
from flask_cors import CORS  # type: ignore
from core_middleware import log_request_info, register_jwt_error_handlers, get_user_id_from_jwt
from database import get_db_path, get_db_connection
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity  # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash  # type: ignore
from werkzeug.utils import secure_filename  # type: ignore
import sqlite3
import os
import json
import uuid
from datetime import datetime, timedelta



app = Flask(__name__)
app.url_map.strict_slashes = False
from extensions import limiter
limiter.init_app(app)
from auth.auth_controller import auth_bp
from profile.profile_controller import profile_bp
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(profile_bp, url_prefix='/api/profile')
from launchpad.launchpad_controller import launchpad_bp
app.register_blueprint(launchpad_bp, url_prefix='/api')
from launchdeck.launchdeck_controller import launchdeck_bp
app.register_blueprint(launchdeck_bp, url_prefix='/api')
from events.events_controller import events_bp
app.register_blueprint(events_bp, url_prefix='/api')
from courses.courses_controller import courses_bp
app.register_blueprint(courses_bp, url_prefix='/api')
from messages.messages_controller import messages_bp
app.register_blueprint(messages_bp, url_prefix='/api')
from resources.resources_controller import resources_bp
app.register_blueprint(resources_bp, url_prefix='/api')
from admin.admin_controller import admin_bp
app.register_blueprint(admin_bp, url_prefix='/api/admin')
from sitemap.sitemap_controller import sitemap_bp
app.register_blueprint(sitemap_bp)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['UPLOAD_FOLDER'] = '.uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

jwt = JWTManager(app)
# Configure CORS to allow all origins and headers for now to fix the blocking issue
CORS(app, origins="*", allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Handle CORS preflight BEFORE any JWT middleware runs.
# @jwt_required() routes return 401 on OPTIONS (no token in preflight),
# which causes the browser to reject the preflight entirely.
from flask import make_response as _make_response
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = _make_response()
        res.headers["Access-Control-Allow-Origin"] = "*"
        res.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        res.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        res.status_code = 200
        return res

# Register middlewares
app.before_request(log_request_info)
register_jwt_error_handlers(jwt)

# Database initialization
def init_db():
    db_path = get_db_path()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('student', 'alumni', 'founder', 'mentor', 'investor', 'admin')),
            graduation_year INTEGER,
            department TEXT,
            hall TEXT,
            branch TEXT,
            bio TEXT,
            current_company TEXT,
            current_position TEXT,
            location TEXT,
            work_preference TEXT CHECK (work_preference IN ('onsite', 'remote', 'hybrid')),
            phone TEXT,
            website TEXT,
            linkedin TEXT,
            github TEXT,
            avatar TEXT,
            is_available BOOLEAN DEFAULT 1,
            is_approved BOOLEAN DEFAULT 1,
            is_blocked BOOLEAN DEFAULT 0,
            alumni_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Site Stats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS site_stats (
            key TEXT PRIMARY KEY,
            label TEXT NOT NULL,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Add new columns if they don't exist (for existing databases)
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN hall TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN branch TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN alumni_type TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN bio TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN current_company TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN current_position TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN location TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN work_preference TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN phone TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN website TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN linkedin TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN github TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN avatar TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN years_of_experience INTEGER')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN domain TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN tech_skills TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN is_blocked BOOLEAN DEFAULT 0')
    except:
        pass

    # Site Stats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS site_stats (
            key TEXT PRIMARY KEY,
            label TEXT NOT NULL,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    try:
        cursor.execute('ALTER TABLE users ADD COLUMN program TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN cv_pdf TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN joining_year INTEGER')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN institute TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN specialization TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN past_projects TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN is_available BOOLEAN DEFAULT 1')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN is_approved BOOLEAN DEFAULT 1')
    except:
        pass
    
    # Mentorship requests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mentorship_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            alumni_id INTEGER NOT NULL,
            message TEXT,
            status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'declined')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES users (id),
            FOREIGN KEY (alumni_id) REFERENCES users (id)
        )
    ''')
    
    # User skills table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            skill_name TEXT NOT NULL,
            skill_type TEXT DEFAULT 'technical' CHECK (skill_type IN ('technical', 'soft', 'language')),
            proficiency_level TEXT DEFAULT 'intermediate' CHECK (proficiency_level IN ('beginner', 'intermediate', 'advanced', 'expert')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # User achievements table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            achievement_type TEXT DEFAULT 'award' CHECK (achievement_type IN ('award', 'certification', 'project', 'publication', 'other')),
            date_earned DATE,
            issuer TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # User languages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_languages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            language_name TEXT NOT NULL,
            proficiency_level TEXT DEFAULT 'intermediate' CHECK (proficiency_level IN ('beginner', 'intermediate', 'advanced', 'native')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Launchpad Services table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            provider_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            price_range TEXT,
            delivery_time TEXT,
            image_url TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (provider_id) REFERENCES users (id)
        )
    ''')
    
    # Launchpad Service Requests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            service_id INTEGER,
            project_type TEXT NOT NULL,
            description TEXT NOT NULL,
            budget_range TEXT,
            status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'contacted', 'in_progress', 'completed', 'cancelled')),
            admin_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (service_id) REFERENCES services (id)
        )
    ''')
    # Service timeline items (for "How we do" / journey per service, managed by admin)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_timeline_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT,
            image TEXT,
            status TEXT DEFAULT 'upcoming' CHECK (status IN ('completed', 'current', 'upcoming')),
            category TEXT,
            sort_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (service_id) REFERENCES services (id)
        )
    ''')
    # Service reviews & past work (for Reviews & Past Work section on service detail)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id INTEGER NOT NULL,
            author_name TEXT NOT NULL,
            content TEXT NOT NULL,
            rating INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (service_id) REFERENCES services (id)
        )
    ''')

    # Student service profile (CV + important data for service matching)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_service_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            resume_url TEXT,
            skills TEXT,
            experience TEXT,
            education TEXT,
            linkedin_url TEXT,
            portfolio_url TEXT,
            other_info TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    # Service allotments (student selected for a service; agree/decline)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_allotments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending_agreement' CHECK (status IN ('pending_agreement', 'agreed', 'declined')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            agreed_at TIMESTAMP,
            FOREIGN KEY (service_id) REFERENCES services (id),
            FOREIGN KEY (student_id) REFERENCES users (id),
            UNIQUE(service_id, student_id)
        )
    ''')

    # Courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            type TEXT NOT NULL, -- Podcast, Seminar, Webinar, Fundae Session, Meeting
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            location TEXT, -- Can be physical or link
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event_enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (event_id) REFERENCES events (id)
        )
    ''')
    
    # Add speaker fields to events table if they don't exist
    try:
        cursor.execute('ALTER TABLE events ADD COLUMN speaker_name TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE events ADD COLUMN speaker_bio TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE events ADD COLUMN speaker_image TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE events ADD COLUMN speaker_contact TEXT')
    except:
        pass

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            perks TEXT,
            timeline TEXT,
            duration TEXT,
            assignments TEXT,
            category TEXT NOT NULL,
            image_url TEXT,
            price REAL,
            start_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Add instructor and curriculum fields to courses table
    try:
        cursor.execute('ALTER TABLE courses ADD COLUMN instructor_name TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE courses ADD COLUMN instructor_bio TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE courses ADD COLUMN instructor_image TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE courses ADD COLUMN what_you_learn TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE courses ADD COLUMN requirements TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE courses ADD COLUMN lessons TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE courses ADD COLUMN skill_tags TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE courses ADD COLUMN lessons_count INTEGER DEFAULT 0')
    except:
        pass

    # Course Enrollments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS course_enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
            payment_status TEXT DEFAULT 'pending' CHECK (payment_status IN ('pending', 'paid')),
            enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (course_id) REFERENCES courses (id),
            UNIQUE(user_id, course_id)
        )
    ''')
    
    # Student verification columns
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN roll_number TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN id_card_image TEXT')
    except:
        pass
    
    # Service request admin_notes column
    try:
        cursor.execute('ALTER TABLE service_requests ADD COLUMN admin_notes TEXT')
    except:
        pass
    # Resources table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            link TEXT,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # LaunchDeck - Pitches table (founder startup pitch data)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pitches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            founder_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            tagline TEXT,
            logo TEXT,
            pitch_overview TEXT,
            highlights TEXT,
            team_members TEXT,
            pitch_deck_images TEXT,
            category TEXT,
            website TEXT,
            social_links TEXT,
            status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'closed')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (founder_id) REFERENCES users (id)
        )
    ''')

    # LaunchDeck - Pitch Interests table (investor interest submissions)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pitch_interests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pitch_id INTEGER NOT NULL,
            investor_id INTEGER NOT NULL,
            message TEXT,
            status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'admin_notified', 'meeting_setup')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (pitch_id) REFERENCES pitches (id),
            FOREIGN KEY (investor_id) REFERENCES users (id),
            UNIQUE(pitch_id, investor_id)
        )
    ''')

    # LaunchDeck - Mentorship Requests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS launchdeck_mentorship_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pitch_id INTEGER NOT NULL,
            founder_id INTEGER NOT NULL,
            mentor_id INTEGER,
            message TEXT,
            status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'declined', 'assigned')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (pitch_id) REFERENCES pitches (id),
            FOREIGN KEY (founder_id) REFERENCES users (id),
            FOREIGN KEY (mentor_id) REFERENCES users (id)
        )
    ''')

    # LaunchDeck - Admin Notifications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            reference_id INTEGER,
            message TEXT NOT NULL,
            is_read BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Payment screenshot columns
    try:
        cursor.execute('ALTER TABLE course_enrollments ADD COLUMN payment_screenshot TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE service_requests ADD COLUMN payment_screenshot TEXT')
    except:
        pass

    conn.commit()
    conn.close()

@app.route('/', methods=['GET'])
def health_check():
    db_path = get_db_path()
    db_status = 'connected' if os.path.exists(db_path) else 'missing'
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': db_status
    }), 200

@app.route('/api/health', methods=['GET'])
def api_health():
    db_path = get_db_path()
    db_status = 'connected' if os.path.exists(db_path) else 'missing'
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat(),
        'database': db_status
    }), 200

init_db()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
    app.run(debug=True, port=5001)
