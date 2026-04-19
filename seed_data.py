import sqlite3
from werkzeug.security import generate_password_hash  # type: ignore
from datetime import datetime, timedelta
import json
import random
from app import init_db  # type: ignore

def seed_database():
    # Initialize database tables first
    init_db()
    
    conn = sqlite3.connect('launchpad.db')
    cursor = conn.cursor()
    
    # Helper to execute safely for tables that might not exist anymore
    def safe_execute(query, params=()):
        try:
            return cursor.execute(query, params)
        except sqlite3.OperationalError as e:
            if 'no such table' in str(e):
                pass
            else:
                raise e

    # Clear existing data safely
    tables = [
        'project_applications', 'project_positions', 'conversations', 'messages',
        'blog_likes', 'user_skills', 'user_achievements', 'user_languages',
        'mentorship_requests', 'blog_posts', 'projects', 'users', 'courses',
        'course_enrollments', 'events', 'event_enrollments', 'site_stats',
        'service_reviews', 'service_timeline_items', 'service_requests', 'services',
        'pitches', 'pitch_interests', 'launchdeck_mentorship_requests', 'admin_notifications'
    ]
    for table_name in tables:
        safe_execute(f'DELETE FROM {table_name}')

    # ----------------- Admin User -----------------
    admin_password = generate_password_hash('IITKGP2026', method='pbkdf2:sha256')
    safe_execute('''
        INSERT INTO users (name, email, password_hash, role, is_approved, is_blocked)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('Admin', 'Admin@kgplaunchpad.in', admin_password, 'admin', True, False))
    print("✓ Admin user created")
    
    # ----------------- Users with Complete Profiles -----------------
    # DISTRIBUTION: 5 Students, 4 Founders, 3 Investors, 3 Mentors
    users = [
        # ====== FOUNDERS (4) — alumni with alumni_type='Founder' ======
        {
            'name': 'Dr. Rajesh Kumar',
            'email': 'rajesh.kumar@iitkgp.ac.in',
            'password': 'password123',
            'role': 'alumni',
            'alumni_type': 'Founder',
            'graduation_year': 2010,
            'department': 'Computer Science and Engineering',
            'hall': 'Nehru Hall',
            'branch': 'B.Tech CSE',
            'bio': 'AI researcher turned entrepreneur. Founded NeuralMesh AI to democratize machine learning for SMBs. Ex-Google AI, Stanford PhD. Passionate about using ML to solve real-world problems.',
            'current_company': 'NeuralMesh AI',
            'current_position': 'CEO & Founder',
            'location': 'Bangalore, Karnataka',
            'work_preference': 'remote',
            'phone': '+91-9876543210',
            'website': 'https://neuralmesh.ai',
            'linkedin': 'https://linkedin.com/in/rajeshkumar',
            'github': 'https://github.com/rajeshkumar',
            'avatar': 'https://randomuser.me/api/portraits/men/1.jpg',
            'years_of_experience': 14,
            'domain': 'AI/ML, Machine Learning',
            'tech_skills': json.dumps(['Python', 'TensorFlow', 'PyTorch', 'Computer Vision', 'AWS', 'Docker']),
            'program': 'B.Tech',
            'joining_year': 2006,
            'institute': 'IIT Kharagpur',
            'specialization': 'Artificial Intelligence and Machine Learning'
        },
        {
            'name': 'Amit Singh',
            'email': 'amit.singh@iitkgp.ac.in',
            'password': 'password123',
            'role': 'alumni',
            'alumni_type': 'Founder',
            'graduation_year': 2015,
            'department': 'Mechanical Engineering',
            'hall': 'Patel Hall',
            'branch': 'B.Tech ME',
            'bio': 'Cleantech founder building GreenHarvest to bring AI-powered precision agriculture to Indian farmers. Forbes 30 Under 30 Asia. Previously at RoboLearn Inc.',
            'current_company': 'GreenHarvest AgriTech',
            'current_position': 'Co-founder & CTO',
            'location': 'Hyderabad, Telangana',
            'work_preference': 'hybrid',
            'phone': '+91-9876543212',
            'website': 'https://greenharvest.in',
            'linkedin': 'https://linkedin.com/in/amitsingh',
            'github': 'https://github.com/amitsingh',
            'avatar': 'https://randomuser.me/api/portraits/men/3.jpg',
            'years_of_experience': 9,
            'domain': 'AgriTech, Robotics, Automation',
            'tech_skills': json.dumps(['ROS', 'Python', 'C++', 'Computer Vision', 'IoT', 'Edge Computing']),
            'program': 'B.Tech',
            'joining_year': 2011,
            'institute': 'IIT Kharagpur',
            'specialization': 'Manufacturing and Automation'
        },
        {
            'name': 'Riya Chakraborty',
            'email': 'riya.chakraborty@iitkgp.ac.in',
            'password': 'password123',
            'role': 'alumni',
            'alumni_type': 'Founder',
            'graduation_year': 2016,
            'department': 'Electronics and Electrical Communication',
            'hall': 'Sarojini Naidu Hall',
            'branch': 'B.Tech ETC',
            'bio': 'EdTech innovator. Founded EduVerse to create immersive virtual campus experiences. Previously at Microsoft Research. Building the future of education with AR/VR.',
            'current_company': 'EduVerse Technologies',
            'current_position': 'Founder & CEO',
            'location': 'Mumbai, Maharashtra',
            'work_preference': 'remote',
            'phone': '+91-9876543230',
            'website': 'https://eduverse.tech',
            'linkedin': 'https://linkedin.com/in/riyachakraborty',
            'github': 'https://github.com/riyachakraborty',
            'avatar': 'https://randomuser.me/api/portraits/women/13.jpg',
            'years_of_experience': 10,
            'domain': 'EdTech, AR/VR',
            'tech_skills': json.dumps(['AR/VR', 'Unity', 'React', 'Node.js', 'WebRTC', 'Python']),
            'program': 'B.Tech',
            'joining_year': 2012,
            'institute': 'IIT Kharagpur',
            'specialization': 'Signal Processing'
        },
        {
            'name': 'Siddharth Joshi',
            'email': 'siddharth.joshi@iitkgp.ac.in',
            'password': 'password123',
            'role': 'alumni',
            'alumni_type': 'Founder',
            'graduation_year': 2017,
            'department': 'Industrial and Systems Engineering',
            'hall': 'Azad Hall',
            'branch': 'B.Tech ISE',
            'bio': 'FinTech builder. Co-founded PaySwift to enable instant cross-border payments for freelancers. Ex-Razorpay. Building the future of global payments.',
            'current_company': 'PaySwift',
            'current_position': 'Co-founder',
            'location': 'Delhi, NCR',
            'work_preference': 'onsite',
            'phone': '+91-9876543231',
            'website': 'https://payswift.io',
            'linkedin': 'https://linkedin.com/in/siddharthjoshi',
            'github': 'https://github.com/siddharthjoshi',
            'avatar': 'https://randomuser.me/api/portraits/men/14.jpg',
            'years_of_experience': 7,
            'domain': 'FinTech, Blockchain',
            'tech_skills': json.dumps(['FinTech', 'Blockchain', 'Golang', 'Kubernetes', 'Microservices']),
            'program': 'B.Tech',
            'joining_year': 2013,
            'institute': 'IIT Kharagpur',
            'specialization': 'Operations Research'
        },

        # ====== INVESTORS (3) — alumni with alumni_type='Investor' ======
        {
            'name': 'Ananya Iyer',
            'email': 'ananya.iyer@iitkgp.ac.in',
            'password': 'password123',
            'role': 'alumni',
            'alumni_type': 'Investor',
            'graduation_year': 2008,
            'department': 'Computer Science and Engineering',
            'hall': 'Indira Gandhi Hall',
            'branch': 'B.Tech CSE',
            'bio': 'Venture partner at Sequoia Capital India. Invested in 25+ startups across SaaS, FinTech, and DeepTech. Board member at 3 unicorns.',
            'current_company': 'Sequoia Capital India',
            'current_position': 'Venture Partner',
            'location': 'Bangalore, Karnataka',
            'work_preference': 'hybrid',
            'phone': '+91-9876543213',
            'website': 'https://sequoiacap.com',
            'linkedin': 'https://linkedin.com/in/ananyaiyer',
            'github': 'https://github.com/ananyaiyer',
            'avatar': 'https://randomuser.me/api/portraits/women/4.jpg',
            'years_of_experience': 16,
            'domain': 'Venture Capital, DeepTech',
            'tech_skills': json.dumps(['Python', 'R', 'Data Science', 'Financial Modeling']),
            'program': 'B.Tech',
            'joining_year': 2004,
            'institute': 'IIT Kharagpur',
            'specialization': 'Computer Science'
        },
        {
            'name': 'Vikram Patel',
            'email': 'vikram.patel@iitkgp.ac.in',
            'password': 'password123',
            'role': 'alumni',
            'alumni_type': 'Investor',
            'graduation_year': 2009,
            'department': 'Civil Engineering',
            'hall': 'Azad Hall',
            'branch': 'B.Tech CE',
            'bio': 'Angel investor and ex-CTO of Flipkart. Passionate about funding deep-tech and climate-tech startups. Managing Partner at VP Capital.',
            'current_company': 'VP Capital',
            'current_position': 'Managing Partner',
            'location': 'Mumbai, Maharashtra',
            'work_preference': 'remote',
            'phone': '+91-9876543214',
            'website': 'https://vpcapital.in',
            'linkedin': 'https://linkedin.com/in/vikrampatel',
            'github': 'https://github.com/vikrampatel',
            'avatar': 'https://randomuser.me/api/portraits/men/5.jpg',
            'years_of_experience': 15,
            'domain': 'Angel Investing, Infrastructure',
            'tech_skills': json.dumps(['GIS', 'AutoCAD', 'Python', 'ArcGIS', 'BIM', '3D Modeling']),
            'program': 'B.Tech',
            'joining_year': 2005,
            'institute': 'IIT Kharagpur',
            'specialization': 'Structural Engineering'
        },
        {
            'name': 'Tanya Bose',
            'email': 'tanya.bose@iitkgp.ac.in',
            'password': 'password123',
            'role': 'alumni',
            'alumni_type': 'Investor',
            'graduation_year': 2011,
            'department': 'Chemical Engineering',
            'hall': 'Sarojini Naidu Hall',
            'branch': 'B.Tech ChE',
            'bio': 'Principal at Accel Partners. Focus on seed-to-Series-A investments in HealthTech and EdTech. Former McKinsey consultant.',
            'current_company': 'Accel Partners',
            'current_position': 'Principal',
            'location': 'Bangalore, Karnataka',
            'work_preference': 'onsite',
            'phone': '+91-9876543232',
            'website': 'https://accel.com',
            'linkedin': 'https://linkedin.com/in/tanyabose',
            'github': None,
            'avatar': 'https://randomuser.me/api/portraits/women/15.jpg',
            'years_of_experience': 13,
            'domain': 'Private Equity, HealthTech',
            'tech_skills': json.dumps(['Financial Modeling', 'Data Analytics', 'Python']),
            'program': 'B.Tech',
            'joining_year': 2007,
            'institute': 'IIT Kharagpur',
            'specialization': 'Process Systems Engineering'
        },

        # ====== MENTORS (3) — alumni with alumni_type='Mentor' ======
        {
            'name': 'Priya Sharma',
            'email': 'priya.sharma@iitkgp.ac.in',
            'password': 'password123',
            'role': 'alumni',
            'alumni_type': 'Mentor',
            'graduation_year': 2007,
            'department': 'Electrical Engineering',
            'hall': 'Sarojini Naidu Hall',
            'branch': 'B.Tech EE',
            'bio': 'Serial entrepreneur and startup mentor. Founded 2 successful exits (combined $40M). Now mentoring early-stage founders on product-market fit. Former Tesla engineer.',
            'current_company': 'Self-employed',
            'current_position': 'Startup Mentor & Advisor',
            'location': 'Pune, Maharashtra',
            'work_preference': 'remote',
            'phone': '+91-9876543211',
            'website': 'https://priyasharma.dev',
            'linkedin': 'https://linkedin.com/in/priyasharma',
            'github': 'https://github.com/priyasharma',
            'avatar': 'https://randomuser.me/api/portraits/women/2.jpg',
            'years_of_experience': 17,
            'domain': 'Product Strategy, IoT, Renewable Energy',
            'tech_skills': json.dumps(['IoT', 'Embedded Systems', 'Python', 'MQTT', 'Node.js', 'React']),
            'program': 'B.Tech',
            'joining_year': 2003,
            'institute': 'IIT Kharagpur',
            'specialization': 'Power Electronics and Drives'
        },
        {
            'name': 'Meera Krishnan',
            'email': 'meera.krishnan@iitkgp.ac.in',
            'password': 'password123',
            'role': 'alumni',
            'alumni_type': 'Mentor',
            'graduation_year': 2006,
            'department': 'Chemical Engineering',
            'hall': 'Sarojini Naidu Hall',
            'branch': 'B.Tech ChE',
            'bio': 'VP Engineering at Amazon India (prev. Netflix). Mentors founders on scaling engineering teams, system design, and tech leadership. Green chemistry advocate.',
            'current_company': 'Amazon India',
            'current_position': 'VP Engineering',
            'location': 'Chennai, Tamil Nadu',
            'work_preference': 'hybrid',
            'phone': '+91-9876543215',
            'website': 'https://chemoptima.com',
            'linkedin': 'https://linkedin.com/in/meerakrishnan',
            'github': 'https://github.com/meerakrishnan',
            'avatar': 'https://randomuser.me/api/portraits/women/6.jpg',
            'years_of_experience': 18,
            'domain': 'Engineering Leadership, Chemical Engineering',
            'tech_skills': json.dumps(['ASPEN', 'MATLAB', 'Python', 'Process Simulation', 'Machine Learning']),
            'program': 'B.Tech',
            'joining_year': 2002,
            'institute': 'IIT Kharagpur',
            'specialization': 'Process Systems Engineering'
        },
        {
            'name': 'Rohan Desai',
            'email': 'rohan.desai@iitkgp.ac.in',
            'password': 'password123',
            'role': 'alumni',
            'alumni_type': 'Mentor',
            'graduation_year': 2010,
            'department': 'Architecture and Regional Planning',
            'hall': 'Azad Hall',
            'branch': 'B.Arch',
            'bio': 'Growth advisor and ex-CMO of Swiggy. Helps startups with GTM strategy, brand building, and scaling from 0 to 1. Smart city consultant.',
            'current_company': 'GrowthX',
            'current_position': 'Growth Advisor',
            'location': 'Bangalore, Karnataka',
            'work_preference': 'remote',
            'phone': '+91-9876543233',
            'website': 'https://growthx.club',
            'linkedin': 'https://linkedin.com/in/rohandesai',
            'github': 'https://github.com/rohandesai',
            'avatar': 'https://randomuser.me/api/portraits/men/16.jpg',
            'years_of_experience': 14,
            'domain': 'Growth & Marketing, Urban Planning',
            'tech_skills': json.dumps(['GIS', 'AutoCAD', 'Python', 'Data Analytics']),
            'program': 'B.Arch',
            'joining_year': 2005,
            'institute': 'IIT Kharagpur',
            'specialization': 'Urban Planning'
        },

        # ====== STUDENTS (5) ======
        {
            'name': 'Sneha Reddy',
            'email': 'sneha.reddy@iitkgp.ac.in',
            'password': 'password123',
            'role': 'student',
            'graduation_year': None,
            'department': 'Computer Science and Engineering',
            'hall': 'Indira Gandhi Hall',
            'branch': 'B.Tech CSE',
            'bio': 'Third-year CSE student passionate about AI and healthcare. Building ML models for disease prediction. Active member of KGP AI Club and Women in Tech.',
            'current_company': None,
            'current_position': 'Student',
            'location': 'Kharagpur, West Bengal',
            'work_preference': 'remote',
            'phone': '+91-9876543216',
            'website': 'https://snehareddy.dev',
            'linkedin': 'https://linkedin.com/in/snehareddy',
            'github': 'https://github.com/snehareddy',
            'avatar': 'https://randomuser.me/api/portraits/women/7.jpg',
            'program': 'B.Tech',
            'joining_year': 2022,
            'institute': 'IIT Kharagpur',
            'specialization': 'Artificial Intelligence',
            'past_projects': json.dumps([
                {'title': 'Disease Prediction System', 'description': 'ML model for early disease detection', 'tech': ['Python', 'TensorFlow', 'Flask']},
                {'title': 'Smart Attendance System', 'description': 'Face recognition based attendance', 'tech': ['OpenCV', 'Python', 'React']}
            ])
        },
        {
            'name': 'Karan Malhotra',
            'email': 'karan.malhotra@iitkgp.ac.in',
            'password': 'password123',
            'role': 'student',
            'graduation_year': None,
            'department': 'Electrical Engineering',
            'hall': 'Patel Hall',
            'branch': 'B.Tech EE',
            'bio': 'Electrical engineering student with a passion for renewable energy and IoT. Working on smart grid optimization. Member of Kharagpur Robotics Society.',
            'current_company': None,
            'current_position': 'Student',
            'location': 'Kharagpur, West Bengal',
            'work_preference': 'hybrid',
            'phone': '+91-9876543217',
            'website': 'https://karanmalhotra.tech',
            'linkedin': 'https://linkedin.com/in/karanmalhotra',
            'github': 'https://github.com/karanmalhotra',
            'avatar': 'https://randomuser.me/api/portraits/men/8.jpg',
            'program': 'B.Tech',
            'joining_year': 2022,
            'institute': 'IIT Kharagpur',
            'specialization': 'Power Systems',
            'past_projects': json.dumps([
                {'title': 'IoT Weather Station', 'description': 'Real-time weather monitoring system', 'tech': ['Arduino', 'IoT', 'MQTT']},
                {'title': 'Solar Panel Optimizer', 'description': 'ML-based solar panel efficiency optimizer', 'tech': ['Python', 'Raspberry Pi']}
            ])
        },
        {
            'name': 'Neha Gupta',
            'email': 'neha.gupta@iitkgp.ac.in',
            'password': 'password123',
            'role': 'student',
            'graduation_year': None,
            'department': 'Biotechnology',
            'hall': 'Sarojini Naidu Hall',
            'branch': 'B.Tech BT',
            'bio': 'Biotechnology student interested in agricultural genomics and bioinformatics. Working on plant disease detection using computer vision. Active researcher in BioKGP lab.',
            'current_company': None,
            'current_position': 'Student',
            'location': 'Kharagpur, West Bengal',
            'work_preference': 'onsite',
            'phone': '+91-9876543218',
            'website': None,
            'linkedin': 'https://linkedin.com/in/nehagupta',
            'github': 'https://github.com/nehagupta',
            'avatar': 'https://randomuser.me/api/portraits/women/9.jpg',
            'program': 'B.Tech',
            'joining_year': 2022,
            'institute': 'IIT Kharagpur',
            'specialization': 'Agricultural Biotechnology',
            'past_projects': json.dumps([
                {'title': 'Plant Disease Detection', 'description': 'CNN-based plant disease classifier', 'tech': ['Python', 'TensorFlow', 'OpenCV']},
                {'title': 'Genome Analysis Tool', 'description': 'Bioinformatics pipeline for genome analysis', 'tech': ['Python', 'R', 'Biopython']}
            ])
        },
        {
            'name': 'Arjun Mehta',
            'email': 'arjun.mehta@iitkgp.ac.in',
            'password': 'password123',
            'role': 'student',
            'graduation_year': None,
            'department': 'Mechanical Engineering',
            'hall': 'Nehru Hall',
            'branch': 'B.Tech ME',
            'bio': 'Mechanical engineering student passionate about robotics and automation. Building autonomous robots. Captain of IIT KGP Robotics Team.',
            'current_company': None,
            'current_position': 'Student',
            'location': 'Kharagpur, West Bengal',
            'work_preference': 'onsite',
            'phone': '+91-9876543219',
            'website': 'https://arjunmehta.tech',
            'linkedin': 'https://linkedin.com/in/arjunmehta',
            'github': 'https://github.com/arjunmehta',
            'avatar': 'https://randomuser.me/api/portraits/men/10.jpg',
            'program': 'B.Tech',
            'joining_year': 2022,
            'institute': 'IIT Kharagpur',
            'specialization': 'Robotics and Automation',
            'past_projects': json.dumps([
                {'title': 'Line Following Robot', 'description': 'Autonomous line following robot using PID', 'tech': ['Arduino', 'C++', 'Sensors']},
                {'title': 'Robotic Arm', 'description': '6-DOF robotic arm with inverse kinematics', 'tech': ['ROS', 'Python', 'Gazebo']}
            ])
        },
        {
            'name': 'Divya Nair',
            'email': 'divya.nair@iitkgp.ac.in',
            'password': 'password123',
            'role': 'student',
            'graduation_year': None,
            'department': 'Chemical Engineering',
            'hall': 'Indira Gandhi Hall',
            'branch': 'B.Tech ChE',
            'bio': 'Chemical engineering student focused on sustainable manufacturing and green chemistry. Researching waste minimization techniques. Member of ChemE Society.',
            'current_company': None,
            'current_position': 'Student',
            'location': 'Kharagpur, West Bengal',
            'work_preference': 'hybrid',
            'phone': '+91-9876543220',
            'website': None,
            'linkedin': 'https://linkedin.com/in/divyanair',
            'github': 'https://github.com/divyanair',
            'avatar': 'https://randomuser.me/api/portraits/women/11.jpg',
            'program': 'B.Tech',
            'joining_year': 2022,
            'institute': 'IIT Kharagpur',
            'specialization': 'Process Engineering',
            'past_projects': json.dumps([
                {'title': 'Waste Water Treatment Model', 'description': 'Simulation of waste water treatment process', 'tech': ['ASPEN', 'MATLAB']},
                {'title': 'Process Optimization', 'description': 'AI-based chemical process optimizer', 'tech': ['Python', 'Machine Learning']}
            ])
        }
    ]
    
    user_ids = {}
    for user in users:
        password_hash = generate_password_hash(user['password'], method='pbkdf2:sha256')
        safe_execute('''
            INSERT INTO users (name, email, password_hash, role, graduation_year, department, hall, branch, bio,
                               current_company, current_position, location, work_preference, phone, website,
                               linkedin, github, avatar, years_of_experience, domain, tech_skills, program,
                               joining_year, institute, specialization, past_projects, is_available, alumni_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user['name'], user['email'], password_hash, user['role'], user['graduation_year'], 
              user['department'], user.get('hall'), user.get('branch'), user.get('bio'),
              user.get('current_company'), user.get('current_position'), user.get('location'),
              user.get('work_preference'), user.get('phone'), user.get('website'),
              user.get('linkedin'), user.get('github'), user.get('avatar'),
              user.get('years_of_experience'), user.get('domain'), user.get('tech_skills'),
              user.get('program'), user.get('joining_year'), user.get('institute'),
              user.get('specialization'), user.get('past_projects'), 
              1 if user['role'] == 'alumni' else None,
              user.get('alumni_type')))
        user_ids[user['email']] = cursor.lastrowid

    # ----------------- User Skills -----------------
    skills_data = {
        'rajesh.kumar@iitkgp.ac.in': [
            {'name': 'Python', 'type': 'technical', 'proficiency': 'expert'},
            {'name': 'Machine Learning', 'type': 'technical', 'proficiency': 'expert'},
            {'name': 'TensorFlow', 'type': 'technical', 'proficiency': 'expert'},
            {'name': 'Computer Vision', 'type': 'technical', 'proficiency': 'expert'},
            {'name': 'Leadership', 'type': 'soft', 'proficiency': 'expert'},
            {'name': 'Public Speaking', 'type': 'soft', 'proficiency': 'advanced'},
        ],
        'priya.sharma@iitkgp.ac.in': [
            {'name': 'IoT', 'type': 'technical', 'proficiency': 'expert'},
            {'name': 'Embedded Systems', 'type': 'technical', 'proficiency': 'expert'},
            {'name': 'Python', 'type': 'technical', 'proficiency': 'advanced'},
            {'name': 'MQTT', 'type': 'technical', 'proficiency': 'advanced'},
            {'name': 'Team Management', 'type': 'soft', 'proficiency': 'expert'},
        ],
        'sneha.reddy@iitkgp.ac.in': [
            {'name': 'Python', 'type': 'technical', 'proficiency': 'advanced'},
            {'name': 'TensorFlow', 'type': 'technical', 'proficiency': 'intermediate'},
            {'name': 'React', 'type': 'technical', 'proficiency': 'intermediate'},
            {'name': 'Communication', 'type': 'soft', 'proficiency': 'advanced'},
        ],
        'karan.malhotra@iitkgp.ac.in': [
            {'name': 'IoT', 'type': 'technical', 'proficiency': 'intermediate'},
            {'name': 'Python', 'type': 'technical', 'proficiency': 'intermediate'},
            {'name': 'Arduino', 'type': 'technical', 'proficiency': 'advanced'},
            {'name': 'Teamwork', 'type': 'soft', 'proficiency': 'advanced'},
        ],
    }
    
    for user_email, skills in skills_data.items():
        if user_email in user_ids:
            for skill in skills:
                safe_execute('''
                    INSERT INTO user_skills (user_id, skill_name, skill_type, proficiency_level)
                    VALUES (?, ?, ?, ?)
                ''', (user_ids[user_email], skill['name'], skill['type'], skill['proficiency']))

    # ----------------- User Achievements -----------------
    achievements_data = {
        'rajesh.kumar@iitkgp.ac.in': [
            {'title': 'Forbes 30 Under 30', 'description': 'Listed in Forbes 30 Under 30 Asia', 'type': 'award', 'date_earned': '2018-06-15', 'issuer': 'Forbes'},
            {'title': 'Best Healthcare Innovation Award', 'description': 'National Healthcare Innovation Award', 'type': 'award', 'date_earned': '2020-03-20', 'issuer': 'Ministry of Health'},
            {'title': 'AWS Certified Solutions Architect', 'description': 'Professional level certification', 'type': 'certification', 'date_earned': '2019-08-10', 'issuer': 'Amazon Web Services'},
        ],
        'priya.sharma@iitkgp.ac.in': [
            {'title': 'Clean Energy Innovator Award', 'description': 'Recognition for sustainable energy solutions', 'type': 'award', 'date_earned': '2021-09-15', 'issuer': 'MNRE'},
            {'title': 'Women in Tech Leadership Award', 'description': 'Outstanding contribution to technology', 'type': 'award', 'date_earned': '2022-03-08', 'issuer': 'WiT India'},
        ],
        'sneha.reddy@iitkgp.ac.in': [
            {'title': 'Best Project Award', 'description': 'Best undergraduate project in CSE', 'type': 'award', 'date_earned': '2024-04-20', 'issuer': 'IIT Kharagpur'},
            {'title': 'AI/ML Certification', 'description': 'Deep Learning Specialization', 'type': 'certification', 'date_earned': '2023-12-10', 'issuer': 'Coursera'},
        ],
    }
    
    for user_email, achievements in achievements_data.items():
        if user_email in user_ids:
            for achievement in achievements:
                safe_execute('''
                    INSERT INTO user_achievements (user_id, title, description, achievement_type, date_earned, issuer)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_ids[user_email], achievement['title'], achievement['description'], 
                      achievement['type'], achievement['date_earned'], achievement['issuer']))

    # ----------------- User Languages -----------------
    languages_data = {
        'rajesh.kumar@iitkgp.ac.in': [
            {'name': 'English', 'proficiency': 'native'},
            {'name': 'Hindi', 'proficiency': 'native'},
            {'name': 'Tamil', 'proficiency': 'advanced'},
        ],
        'priya.sharma@iitkgp.ac.in': [
            {'name': 'English', 'proficiency': 'native'},
            {'name': 'Hindi', 'proficiency': 'native'},
            {'name': 'Marathi', 'proficiency': 'intermediate'},
        ],
        'sneha.reddy@iitkgp.ac.in': [
            {'name': 'English', 'proficiency': 'advanced'},
            {'name': 'Hindi', 'proficiency': 'intermediate'},
            {'name': 'Telugu', 'proficiency': 'native'},
        ],
    }
    
    for user_email, languages in languages_data.items():
        if user_email in user_ids:
            for language in languages:
                safe_execute('''
                    INSERT INTO user_languages (user_id, language_name, proficiency_level)
                    VALUES (?, ?, ?)
                ''', (user_ids[user_email], language['name'], language['proficiency']))

    # ----------------- Projects -----------------
    placeholder_imgs = [
        'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?q=80&w=1200&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1576091160550-2173dba999ef?q=80&w=1200&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1581093588401-16f2d7f3d8ac?q=80&w=1200&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1518779578993-ec3579fee39f?q=80&w=1200&auto=format&fit=crop',
        'https://images.unsplash.com/photo-1555949963-aa79dcee981d?q=80&w=1200&auto=format&fit=crop',
    ]
    
    projects = [
        {
            'title': 'AI-Powered Healthcare Diagnostics',
            'description': 'Developing an ML platform for early disease detection using medical imaging and deep learning algorithms. The system can detect diseases like pneumonia, tuberculosis, and COVID-19 from chest X-rays with 95%+ accuracy. We are also working on integrating patient history and lab reports for comprehensive diagnosis.',
            'category': 'Healthcare AI',
            'status': 'active',
            'team_members': json.dumps(['Dr. Rajesh Kumar', 'Priya Sharma', 'External Consultants']),
            'tags': json.dumps(['AI/ML', 'Healthcare', 'Computer Vision', 'Deep Learning', 'TensorFlow', 'Python']),
            'created_by': user_ids['rajesh.kumar@iitkgp.ac.in'],
            'skills_required': json.dumps(['Python', 'TensorFlow', 'Computer Vision', 'Medical Imaging', 'Flask', 'REST API']),
            'is_recruiting': True,
            'images': json.dumps(placeholder_imgs[:3]), # type: ignore
            'project_links': json.dumps([
                {'label': 'Project Website', 'url': 'https://example.com/ai-health'},
                {'label': 'GitHub Repository', 'url': 'https://github.com/example/ai-health'},
                {'label': 'Research Paper', 'url': 'https://arxiv.org/example'}
            ]),
            'jd_pdf': 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf',
            'contact_details': json.dumps({
                'email': 'rajesh.kumar@iitkgp.ac.in',
                'phone': '+91-9876543210',
                'preferred_contact': 'email'
            }),
            'team_roles': json.dumps([
                {'role': 'ML Engineer', 'count': 2, 'description': 'Build and train ML models'},
                {'role': 'Backend Developer', 'count': 1, 'description': 'Develop APIs and backend'},
                {'role': 'UI/UX Designer', 'count': 1, 'description': 'Design user interface'}
            ]),
            'partners': json.dumps(['AIIMS Delhi', 'Apollo Hospitals', 'MediAI Solutions']),
            'funding': '₹50 Lakhs from DST-NIDHI',
            'highlights': json.dumps([
                '95%+ accuracy on disease detection',
                'Processing 1000+ scans daily',
                'Collaboration with top hospitals',
                'Published in IEEE Medical Imaging Journal'
            ])
        },
        {
            'title': 'Sustainable Energy Management System',
            'description': 'Building a smart grid optimization system for renewable energy distribution and management. The platform uses IoT sensors to monitor energy consumption, solar panel efficiency, and battery storage. AI algorithms optimize energy distribution to minimize waste and maximize renewable usage.',
            'category': 'Clean Tech',
            'status': 'active',
            'team_members': json.dumps(['Priya Sharma', 'Industry Partners']),
            'tags': json.dumps(['IoT', 'Sustainability', 'Energy', 'Smart Grid', 'Python', 'MQTT']),
            'created_by': user_ids['priya.sharma@iitkgp.ac.in'],
            'skills_required': json.dumps(['IoT', 'Embedded Systems', 'Python', 'Data Analytics', 'MQTT', 'Node.js']),
            'is_recruiting': True,
            'images': json.dumps(placeholder_imgs[1:4]), # type: ignore
            'project_links': json.dumps([
                {'label': 'Project Pitch', 'url': 'https://example.com/clean-tech'},
                {'label': 'Technical Docs', 'url': 'https://docs.example.com/clean-tech'}
            ]),
            'jd_pdf': 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf',
            'contact_details': json.dumps({
                'email': 'priya.sharma@iitkgp.ac.in',
                'phone': '+91-9876543211',
                'preferred_contact': 'email'
            }),
            'team_roles': json.dumps([
                {'role': 'IoT Developer', 'count': 2, 'description': 'Develop IoT solutions'},
                {'role': 'Data Analyst', 'count': 1, 'description': 'Analyze energy data'}
            ]),
            'partners': json.dumps(['GreenGrid Technologies', 'MNRE', 'Tata Power']),
            'funding': '₹35 Lakhs from MNRE Grant',
            'highlights': json.dumps([
                '30% reduction in energy waste',
                'Deployed in 50+ buildings',
                'Real-time monitoring dashboard',
                'Carbon footprint reduction of 500 tons/year'
            ])
        },
        {
            'title': 'EdTech Learning Platform',
            'description': 'Creating adaptive AI-powered learning paths for K-12 education with personalized content delivery. The platform uses ML to understand each student\'s learning style and pace, creating customized lesson plans and assessments.',
            'category': 'Education',
            'status': 'completed',
            'team_members': json.dumps(['Amit Singh', 'Development Team']),
            'tags': json.dumps(['EdTech', 'AI', 'Education', 'Personalization', 'React', 'Node.js']),
            'created_by': user_ids['amit.singh@iitkgp.ac.in'],
            'skills_required': json.dumps(['React', 'Node.js', 'MongoDB', 'AI/ML', 'Express.js']),
            'is_recruiting': False,
            'images': json.dumps(placeholder_imgs[:2]), # type: ignore
            'project_links': json.dumps([
                {'label': 'Platform Demo', 'url': 'https://example.com/edtech-demo'}
            ]),
            'jd_pdf': None,
            'contact_details': json.dumps({
                'email': 'amit.singh@iitkgp.ac.in',
                'phone': '+91-9876543212',
                'preferred_contact': 'email'
            }),
            'team_roles': json.dumps([]),
            'partners': json.dumps(['RoboLearn Inc', 'Central Board of Education']),
            'funding': '₹25 Lakhs from Angel Investors',
            'highlights': json.dumps([
                '2M+ active students',
                '85% improvement in learning outcomes',
                'Available in 8 Indian languages',
                'Featured in Education Times'
            ])
        },
        {
            'title': 'Blockchain Supply Chain Tracker',
            'description': 'Implementing blockchain-based secure and transparent supply chain tracking system. Every transaction and movement of goods is recorded on the blockchain, ensuring transparency and preventing fraud. Smart contracts automate payments and verification.',
            'category': 'FinTech',
            'status': 'active',
            'team_members': json.dumps(['Dr. Rajesh Kumar', 'Blockchain Team']),
            'tags': json.dumps(['Blockchain', 'Supply Chain', 'Transparency', 'Security', 'Web3', 'Solidity']),
            'created_by': user_ids['rajesh.kumar@iitkgp.ac.in'],
            'skills_required': json.dumps(['Blockchain', 'Solidity', 'Web3.js', 'Smart Contracts', 'Ethereum']),
            'is_recruiting': True,
            'images': json.dumps(placeholder_imgs),
            'project_links': json.dumps([
                {'label': 'Technical Documentation', 'url': 'https://example.com/scm-docs'},
                {'label': 'Smart Contract Repo', 'url': 'https://github.com/example/blockchain-scm'}
            ]),
            'jd_pdf': 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf',
            'contact_details': json.dumps({
                'email': 'rajesh.kumar@iitkgp.ac.in',
                'phone': '+91-9876543210',
                'preferred_contact': 'email'
            }),
            'team_roles': json.dumps([
                {'role': 'Blockchain Developer', 'count': 2, 'description': 'Develop smart contracts'},
                {'role': 'Frontend Developer', 'count': 1, 'description': 'Build Web3 interface'}
            ]),
            'partners': json.dumps(['Supply Chain Alliance', 'Ethereum Foundation']),
            'funding': '₹60 Lakhs from Blockchain Accelerator',
            'highlights': json.dumps([
                'Processing 10,000+ transactions daily',
                'Zero fraud incidents',
                '50+ companies using the platform',
                'Featured in TechCrunch'
            ])
        },
        {
            'title': 'Smart Agriculture Monitoring',
            'description': 'IoT-based real-time monitoring system for crop health, soil conditions, and weather patterns. Sensors deployed across farmlands collect data on soil moisture, pH, temperature, and nutrient levels. ML models predict optimal irrigation and fertilization schedules.',
            'category': 'AgriTech',
            'status': 'active',
            'team_members': json.dumps(['Ananya Iyer', 'Field Team']),
            'tags': json.dumps(['IoT', 'Agriculture', 'Monitoring', 'Data Analytics', 'Sensors']),
            'created_by': user_ids['ananya.iyer@iitkgp.ac.in'],
            'skills_required': json.dumps(['IoT', 'Sensors', 'Python', 'Data Visualization', 'Arduino']),
            'is_recruiting': True,
            'images': json.dumps(placeholder_imgs[::2]), # type: ignore
            'project_links': json.dumps([
                {'label': 'Live Dashboard', 'url': 'https://example.com/agri-dash'},
                {'label': 'Research Paper', 'url': 'https://example.com/agri-research'}
            ]),
            'jd_pdf': None,
            'contact_details': json.dumps({
                'email': 'ananya.iyer@iitkgp.ac.in',
                'phone': '+91-9876543213',
                'preferred_contact': 'email'
            }),
            'team_roles': json.dumps([
                {'role': 'IoT Engineer', 'count': 1, 'description': 'Deploy sensor networks'},
                {'role': 'Full Stack Developer', 'count': 1, 'description': 'Build monitoring dashboard'}
            ]),
            'partners': json.dumps(['FarmTech Innovations', 'ICAR', 'Farmer Cooperatives']),
            'funding': '₹20 Lakhs from ICAR Grant',
            'highlights': json.dumps([
                'Deployed across 500+ acres',
                '40% water savings',
                '25% increase in crop yield',
                'Helping 200+ farmers'
            ])
        },
        {
            'title': 'Urban Infrastructure Planning Tool',
            'description': 'GIS-based tool for urban planning and infrastructure development with 3D visualization. Planners can simulate different development scenarios, analyze traffic patterns, and optimize infrastructure placement. Includes augmented reality features for on-site visualization.',
            'category': 'Civil Tech',
            'status': 'active',
            'team_members': json.dumps(['Vikram Patel', 'Planning Team']),
            'tags': json.dumps(['GIS', 'Urban Planning', '3D Modeling', 'Infrastructure', 'AutoCAD']),
            'created_by': user_ids['vikram.patel@iitkgp.ac.in'],
            'skills_required': json.dumps(['GIS', 'AutoCAD', 'Python', '3D Modeling', 'ArcGIS', 'Three.js']),
            'is_recruiting': True,
            'images': json.dumps(placeholder_imgs[:3]), # type: ignore
            'project_links': json.dumps([
                {'label': 'Project Overview', 'url': 'https://example.com/urban-planning'}
            ]),
            'jd_pdf': 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf',
            'contact_details': json.dumps({
                'email': 'vikram.patel@iitkgp.ac.in',
                'phone': '+91-9876543214',
                'preferred_contact': 'email'
            }),
            'team_roles': json.dumps([
                {'role': 'GIS Specialist', 'count': 1, 'description': 'Develop GIS tools'},
                {'role': '3D Visualization Developer', 'count': 1, 'description': 'Create 3D models'}
            ]),
            'partners': json.dumps(['SmartCity Consulting', 'Ministry of Urban Development']),
            'funding': '₹45 Lakhs from Smart Cities Mission',
            'highlights': json.dumps([
                'Used by 15 city municipal corporations',
                'Saved ₹100 crores in planning costs',
                'AR features for on-site visualization',
                'Winner of Smart Cities Innovation Award'
            ])
        },
        {
            'title': 'Chemical Process Optimization Platform',
            'description': 'AI-driven platform for optimizing chemical manufacturing processes and reducing waste. Uses machine learning to analyze process parameters and suggest optimizations. Real-time monitoring prevents equipment failures and ensures product quality.',
            'category': 'Chemical Engineering',
            'status': 'active',
            'team_members': json.dumps(['Meera Krishnan', 'Process Team']),
            'tags': json.dumps(['Process Engineering', 'AI', 'Optimization', 'Sustainability', 'ASPEN']),
            'created_by': user_ids['meera.krishnan@iitkgp.ac.in'],
            'skills_required': json.dumps(['Chemical Engineering', 'Python', 'Machine Learning', 'Process Simulation', 'ASPEN']),
            'is_recruiting': True,
            'images': json.dumps(placeholder_imgs[1:4]), # type: ignore
            'project_links': json.dumps([
                {'label': 'Case Study', 'url': 'https://example.com/chem-case'},
                {'label': 'Technical Whitepaper', 'url': 'https://example.com/chem-whitepaper'}
            ]),
            'jd_pdf': None,
            'contact_details': json.dumps({
                'email': 'meera.krishnan@iitkgp.ac.in',
                'phone': '+91-9876543215',
                'preferred_contact': 'email'
            }),
            'team_roles': json.dumps([
                {'role': 'Process Engineer', 'count': 1, 'description': 'Optimize processes'},
                {'role': 'ML Engineer', 'count': 1, 'description': 'Develop predictive models'}
            ]),
            'partners': json.dumps(['ChemOptima Solutions', 'IIChE', 'Chemical Industries']),
            'funding': '₹30 Lakhs from Industry Partnership',
            'highlights': json.dumps([
                '20% reduction in waste',
                '15% improvement in yield',
                'Deployed in 10 manufacturing plants',
                'Savings of ₹50 lakhs annually per plant'
            ])
        },
        {
            'title': 'Robotics for Manufacturing Automation',
            'description': 'Developing robotic systems for automated manufacturing and quality control. Includes robotic arms for assembly, computer vision for quality inspection, and collaborative robots (cobots) that work alongside humans. System integrates with existing production lines.',
            'category': 'Robotics',
            'status': 'active',
            'team_members': json.dumps(['Amit Singh', 'Robotics Team']),
            'tags': json.dumps(['Robotics', 'Automation', 'Manufacturing', 'AI', 'ROS', 'Computer Vision']),
            'created_by': user_ids['amit.singh@iitkgp.ac.in'],
            'skills_required': json.dumps(['Robotics', 'ROS', 'Python', 'Computer Vision', 'C++', 'Control Systems']),
            'is_recruiting': True,
            'images': json.dumps(placeholder_imgs),
            'project_links': json.dumps([
                {'label': 'Technical Specification', 'url': 'https://example.com/robotics-spec'},
                {'label': 'Demo Video', 'url': 'https://youtube.com/example'}
            ]),
            'jd_pdf': 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf',
            'contact_details': json.dumps({
                'email': 'amit.singh@iitkgp.ac.in',
                'phone': '+91-9876543212',
                'preferred_contact': 'email'
            }),
            'team_roles': json.dumps([
                {'role': 'Robotics Engineer', 'count': 2, 'description': 'Design robotic systems'},
                {'role': 'Computer Vision Engineer', 'count': 1, 'description': 'Develop vision systems'}
            ]),
            'partners': json.dumps(['RoboLearn Inc', 'Manufacturing Companies', 'MSME Ministry']),
            'funding': '₹55 Lakhs from Technology Development Fund',
            'highlights': json.dumps([
                '50% reduction in manual labor',
                '99% quality inspection accuracy',
                'Deployed in 8 manufacturing facilities',
                'ROI achieved in 18 months'
            ])
        }
    ]
    
    project_ids = {}
    for project in projects:
        safe_execute('''
            INSERT INTO projects (title, description, category, status, team_members, tags, created_by, 
                                  skills_required, is_recruiting, images, project_links, jd_pdf, 
                                  contact_details, team_roles, partners, funding, highlights)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (project['title'], project['description'], project['category'], project['status'], 
              project['team_members'], project['tags'], project['created_by'], 
              project['skills_required'], project['is_recruiting'], project['images'], 
              project['project_links'], project['jd_pdf'], project['contact_details'], 
              project['team_roles'], project['partners'], project['funding'], project['highlights']))
        project_ids[project['title']] = cursor.lastrowid

    # ----------------- Project Positions -----------------
    project_positions = [
        # AI-Powered Healthcare Diagnostics - 3 positions
        {'project_id': project_ids['AI-Powered Healthcare Diagnostics'], 'title': 'ML Engineer', 
         'description': 'Develop and train deep learning models for medical image analysis. Work with CNNs, transfer learning, and model optimization techniques.', 
         'required_skills': json.dumps(['Python', 'TensorFlow', 'PyTorch', 'Computer Vision', 'Medical Imaging']), 
         'count': 2, 'filled_count': 1, 'is_active': True,
         'stipend': 25000, 'duration': '6 months', 'location': 'Bangalore (Hybrid)'},
        
        {'project_id': project_ids['AI-Powered Healthcare Diagnostics'], 'title': 'Backend Developer', 
         'description': 'Build scalable APIs and database architecture for the healthcare platform. Implement secure patient data handling and real-time processing.', 
         'required_skills': json.dumps(['Python', 'Flask', 'PostgreSQL', 'REST API', 'Docker']), 
         'count': 1, 'filled_count': 0, 'is_active': True,
         'stipend': 22000, 'duration': '6 months', 'location': 'Bangalore (Remote)'},
        
        {'project_id': project_ids['AI-Powered Healthcare Diagnostics'], 'title': 'UI/UX Designer', 
         'description': 'Design intuitive interfaces for healthcare professionals and patients. Create user flows and prototypes.', 
         'required_skills': json.dumps(['Figma', 'Adobe XD', 'UI Design', 'Healthcare UX', 'Prototyping']), 
         'count': 1, 'filled_count': 0, 'is_active': True,
         'stipend': 20000, 'duration': '4 months', 'location': 'Remote'},
        
        # Sustainable Energy Management System - 2 positions
        {'project_id': project_ids['Sustainable Energy Management System'], 'title': 'IoT Developer', 
         'description': 'Develop IoT sensors and edge computing solutions for energy monitoring. Work with MQTT protocols and real-time data processing.', 
         'required_skills': json.dumps(['IoT', 'Embedded Systems', 'C++', 'MQTT', 'Arduino', 'Raspberry Pi']), 
         'count': 2, 'filled_count': 0, 'is_active': True,
         'stipend': 20000, 'duration': '5 months', 'location': 'Pune (Onsite)'},
        
        {'project_id': project_ids['Sustainable Energy Management System'], 'title': 'Data Analyst', 
         'description': 'Analyze energy consumption patterns and optimize grid performance. Create dashboards and reports.', 
         'required_skills': json.dumps(['Python', 'Data Analytics', 'Power BI', 'SQL', 'Pandas']), 
         'count': 1, 'filled_count': 0, 'is_active': True,
         'stipend': 18000, 'duration': '4 months', 'location': 'Pune (Hybrid)'},
        
        # Blockchain Supply Chain Tracker - 2 positions
        {'project_id': project_ids['Blockchain Supply Chain Tracker'], 'title': 'Blockchain Developer', 
         'description': 'Develop smart contracts and blockchain infrastructure for supply chain tracking. Work with Ethereum and Solidity.', 
         'required_skills': json.dumps(['Solidity', 'Ethereum', 'Web3.js', 'Smart Contracts', 'Truffle']), 
         'count': 2, 'filled_count': 0, 'is_active': True,
         'stipend': 30000, 'duration': '6 months', 'location': 'Remote'},
        
        {'project_id': project_ids['Blockchain Supply Chain Tracker'], 'title': 'Frontend Developer', 
         'description': 'Build responsive web interface for supply chain tracking. Integrate Web3 wallet connections.', 
         'required_skills': json.dumps(['React', 'TypeScript', 'Web3.js', 'TailwindCSS', 'ethers.js']), 
         'count': 1, 'filled_count': 0, 'is_active': True,
         'stipend': 25000, 'duration': '5 months', 'location': 'Remote'},
        
        # Smart Agriculture Monitoring - 2 positions
        {'project_id': project_ids['Smart Agriculture Monitoring'], 'title': 'IoT Engineer', 
         'description': 'Design and deploy sensor networks for crop monitoring. Install and maintain field equipment.', 
         'required_skills': json.dumps(['IoT', 'Sensors', 'Arduino', 'Raspberry Pi', 'LoRaWAN']), 
         'count': 1, 'filled_count': 1, 'is_active': False,
         'stipend': 15000, 'duration': '3 months', 'location': 'Pune (Onsite)'},
        
        {'project_id': project_ids['Smart Agriculture Monitoring'], 'title': 'Full Stack Developer', 
         'description': 'Build web dashboard for real-time monitoring and alerts. Implement data visualization and reporting.', 
         'required_skills': json.dumps(['React', 'Node.js', 'MongoDB', 'Chart.js', 'Express']), 
         'count': 1, 'filled_count': 0, 'is_active': True,
         'stipend': 18000, 'duration': '4 months', 'location': 'Remote'},
        
        # Urban Infrastructure Planning Tool - 2 positions
        {'project_id': project_ids['Urban Infrastructure Planning Tool'], 'title': 'GIS Specialist', 
         'description': 'Develop GIS-based mapping and analysis tools. Work with spatial data and urban planning models.', 
         'required_skills': json.dumps(['GIS', 'ArcGIS', 'QGIS', 'Python', 'PostGIS']), 
         'count': 1, 'filled_count': 0, 'is_active': True,
         'stipend': 22000, 'duration': '5 months', 'location': 'Delhi (Onsite)'},
        
        {'project_id': project_ids['Urban Infrastructure Planning Tool'], 'title': '3D Visualization Developer', 
         'description': 'Create 3D models and visualization for urban planning. Implement AR features for on-site use.', 
         'required_skills': json.dumps(['Three.js', 'Blender', 'WebGL', 'AutoCAD', 'Unity']), 
         'count': 1, 'filled_count': 0, 'is_active': True,
         'stipend': 24000, 'duration': '5 months', 'location': 'Delhi (Hybrid)'},
        
        # Chemical Process Optimization Platform - 2 positions
        {'project_id': project_ids['Chemical Process Optimization Platform'], 'title': 'Process Engineer', 
         'description': 'Optimize chemical manufacturing processes using AI. Analyze process data and implement improvements.', 
         'required_skills': json.dumps(['Chemical Engineering', 'Process Simulation', 'Python', 'ASPEN', 'Optimization']), 
         'count': 1, 'filled_count': 1, 'is_active': False,
         'stipend': 20000, 'duration': '4 months', 'location': 'Chennai (Onsite)'},
        
        {'project_id': project_ids['Chemical Process Optimization Platform'], 'title': 'ML Engineer', 
         'description': 'Develop predictive models for process optimization. Work with time-series data and anomaly detection.', 
         'required_skills': json.dumps(['Machine Learning', 'Python', 'TensorFlow', 'Data Science', 'Time Series']), 
         'count': 1, 'filled_count': 0, 'is_active': True,
         'stipend': 22000, 'duration': '5 months', 'location': 'Chennai (Hybrid)'},
        
        # Robotics for Manufacturing Automation - 2 positions
        {'project_id': project_ids['Robotics for Manufacturing Automation'], 'title': 'Robotics Engineer', 
         'description': 'Design and program robotic systems for manufacturing. Implement control systems and kinematics.', 
         'required_skills': json.dumps(['Robotics', 'ROS', 'Python', 'Control Systems', 'C++']), 
         'count': 2, 'filled_count': 0, 'is_active': True,
         'stipend': 28000, 'duration': '6 months', 'location': 'Hyderabad (Onsite)'},
        
        {'project_id': project_ids['Robotics for Manufacturing Automation'], 'title': 'Computer Vision Engineer', 
         'description': 'Develop vision systems for quality control. Implement object detection and defect recognition.', 
         'required_skills': json.dumps(['Computer Vision', 'OpenCV', 'Python', 'Deep Learning', 'TensorFlow']), 
         'count': 1, 'filled_count': 0, 'is_active': True,
         'stipend': 26000, 'duration': '6 months', 'location': 'Hyderabad (Hybrid)'},
    ]
    
    position_ids = {}
    for pos in project_positions:
        safe_execute('''
            INSERT INTO project_positions (project_id, title, description, required_skills, count, filled_count, is_active, stipend, duration, location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (pos['project_id'], pos['title'], pos['description'], pos['required_skills'], 
              pos['count'], pos['filled_count'], pos['is_active'], pos['stipend'], pos['duration'], pos['location']))
        position_ids[f"{pos['project_id']}_{pos['title']}"] = cursor.lastrowid

    # ----------------- Blog Posts -----------------
    blog_posts = [
        {
            'title': 'From IIT KGP to Building a $50M Startup: My Journey',
            'content': '''When I graduated from IIT Kharagpur in 2010, I had no idea that a decade later I'd be running a healthcare AI startup valued at $50M. This is my story of failures, learnings, and eventual success.

**The Early Days**

It all started in my final year when I was working on a project using machine learning for medical image analysis. The accuracy was poor, the computational resources were limited, but the potential was immense. I was fascinated by how AI could potentially save lives.

**The First Failure**

After graduation, I joined a tech giant. Good salary, great perks, but something was missing. I wanted to make a real impact. So I quit after 2 years and started my first company - it failed within 8 months. Ran out of money, couldn't find product-market fit, and lost my savings.

**The Learning Phase**

I spent the next 3 years working with different healthcare startups, learning the domain inside-out. I understood that technology alone isn't enough - you need to deeply understand the problem you're solving.

**MediAI Solutions**

In 2016, I co-founded MediAI Solutions with a vision to make quality healthcare accessible through AI. We started with a simple product - detecting pneumonia from chest X-rays. Today, we process over a million scans annually and have saved countless lives.

**Lessons Learned**

1. Domain expertise matters as much as technical skills
2. Failure is just a stepping stone
3. Build a strong team - you can't do it alone
4. Focus on solving real problems, not building cool tech
5. Persistence beats talent

**Advice for Current Students**

Don't be afraid to take risks. IIT KGP gave us not just education, but the confidence to dream big. Use it wisely. And remember, success is never a straight line.

*Dr. Rajesh Kumar is the Founder & CEO of MediAI Solutions, a healthcare AI company valued at $50M. He graduated from IIT Kharagpur in 2010 with a B.Tech in Computer Science.*''',
            'category': 'Career',
            'author_id': user_ids['rajesh.kumar@iitkgp.ac.in']
        },
        {
            'title': 'How IIT KGP Shaped My Vision for Sustainable Technology',
            'content': '''IIT Kharagpur wasn't just my alma mater - it was the place that ignited my passion for sustainable technology and renewable energy. Here's how my journey unfolded.

**The Spark**

It was Professor Singh's lecture on energy crisis that changed everything. He showed us projections of India's energy needs by 2030 and the environmental cost of conventional energy. That day, I decided my career would be in clean energy.

**Campus Projects**

During my time at KGP, I was part of the Solar Car team. We worked late nights, faced countless failures, but eventually built a functional solar-powered vehicle. Those sleepless nights taught me more than any textbook could.

**The Real World**

After graduation, I joined Tesla's energy division. Working there showed me the global scale of the energy problem and the potential of smart grids and IoT.

**Coming Full Circle**

Today, my company GreenGrid Technologies is deploying smart energy management systems across India. We're making renewable energy accessible and affordable. And it all started in a classroom at IIT KGP.

**The Future**

India needs to add 500 GW of renewable capacity by 2030. This is the biggest challenge and opportunity of our generation. I'm excited to be part of this transformation.

*Priya Sharma is VP Engineering at GreenGrid Technologies. She graduated from IIT Kharagpur in 2012 with a B.Tech in Electrical Engineering.*''',
            'category': 'Startup',
            'author_id': user_ids['priya.sharma@iitkgp.ac.in']
        },
        {
            'title': 'Transforming Healthcare with AI: Lessons from Building MediAI',
            'content': '''Building a healthcare AI platform from scratch taught me lessons that no MBA could. Here's what I learned building MediAI Solutions from 0 to serving millions.

**Challenge 1: Data Quality**

Healthcare data is messy. X-rays from different machines, varying quality, inconsistent labeling. We spent 18 months just cleaning and curating our dataset.

**Challenge 2: Regulatory Approval**

Getting medical device approval is no joke. We had to conduct clinical trials, demonstrate efficacy, and ensure patient safety. It took 2 years and significant investment.

**Challenge 3: Doctor Adoption**

Doctors are rightfully skeptical of AI. We had to prove that our system augments, not replaces, their expertise. Building trust took time and transparency.

**The Breakthrough**

During COVID-19, our system helped hospitals screen thousands of patients quickly. That's when we scaled from 100 scans/day to 1000+. Crisis often reveals the true value of innovation.

**Technical Stack**

- TensorFlow for deep learning models
- Flask/FastAPI for backend
- PostgreSQL for data storage
- AWS for scalability
- Docker/Kubernetes for deployment

**Impact**

Today, we've processed over 5 million medical images, helped diagnose 50,000+ patients early, and partnered with 100+ hospitals. But the journey is just beginning.

*Dr. Rajesh Kumar is the Founder & CEO of MediAI Solutions.*''',
            'category': 'Technology',
            'author_id': user_ids['rajesh.kumar@iitkgp.ac.in']
        },
        {
            'title': 'The Future of Work: How AI is Changing the Job Market',
            'content': '''AI is not coming for your jobs - it's changing what jobs look like. Here's my analysis of the future job market and what students need to prepare for.

**The Shift**

Repetitive tasks are being automated. But creative, strategic, and empathetic work is more valuable than ever. The key is to position yourself in the right quadrant.

**Skills That Matter**

1. **Problem-solving**: AI can execute, but humans define problems
2. **Creativity**: Original thinking can't be automated
3. **Emotional Intelligence**: Human connection matters more than ever
4. **Adaptability**: Learning to learn is the meta-skill

**Industries to Watch**

- Healthcare AI
- Climate Tech
- EdTech
- AgriTech
- Fintech

**Advice for Students**

Don't just learn to code. Learn to think. Build projects that solve real problems. Understand domains deeply. And most importantly, stay curious.

The future belongs to those who can work WITH AI, not compete against it.

*Amit Singh is CTO at RoboLearn Inc and a 2015 graduate of IIT Kharagpur.*''',
            'category': 'Career',
            'author_id': user_ids['amit.singh@iitkgp.ac.in']
        },
        {
            'title': 'Biotechnology Innovations in Agriculture',
            'content': '''India feeds 1.4 billion people, but our agriculture faces massive challenges. Here's how biotechnology and technology convergence can transform farming.

**The Problem**

- Water scarcity
- Soil degradation
- Climate change impact
- Pest resistance
- Post-harvest losses (30-40%)

**The Solution: AgriTech + BioTech**

At FarmTech Innovations, we're combining biotechnology with IoT to create precision agriculture solutions. Our sensors monitor crop health in real-time, while our biotech solutions improve crop resilience.

**Real Impact**

We've deployed our system across 500+ acres, helping farmers:
- Reduce water usage by 40%
- Increase yield by 25%
- Reduce pesticide use by 50%
- Improve soil health

**The Science**

We use CRISPR for crop improvement, ML for disease prediction, and IoT for monitoring. It's a perfect blend of biology and technology.

**The Future**

India needs to double farm incomes by 2027. Technology is the only way to achieve this ambitious goal. And IIT KGP alumni are at the forefront of this revolution.

*Ananya Iyer is Chief Science Officer at FarmTech Innovations and a 2013 graduate of IIT Kharagpur.*''',
            'category': 'Technology',
            'author_id': user_ids['ananya.iyer@iitkgp.ac.in']
        },
        {
            'title': 'Smart Cities: The Role of Civil Engineers',
            'content': '''Civil engineering is undergoing a digital transformation. Smart cities are not just about technology - they're about reimagining urban infrastructure for the 21st century.

**The Vision**

India is building 100 smart cities. But what makes a city "smart"? It's the integration of technology with physical infrastructure to create sustainable, livable urban spaces.

**Our Approach**

At SmartCity Consulting, we use:
- GIS for urban planning
- IoT for infrastructure monitoring
- AI for traffic optimization
- BIM for building design
- Digital twins for simulation

**Case Study: Pune Smart City**

We helped design Pune's smart grid, intelligent traffic system, and waste management. The results:
- 30% reduction in traffic congestion
- 40% improvement in waste collection
- ₹100 crore savings in infrastructure costs

**Challenges**

- Integration with legacy systems
- Data privacy and security
- Training traditional engineers
- Funding constraints

**The Future**

By 2030, 40% of India's population will be urban. We need to build cities that are sustainable, resilient, and inclusive. Technology is the enabler, but human-centric design is the core.

*Vikram Patel is Senior Partner at SmartCity Consulting and a 2014 graduate of IIT Kharagpur.*''',
            'category': 'Technology',
            'author_id': user_ids['vikram.patel@iitkgp.ac.in']
        },
        {
            'title': 'Green Chemistry: Sustainable Manufacturing',
            'content': '''Chemical manufacturing has traditionally been resource-intensive and polluting. Green chemistry is changing that paradigm. Here's how.

**The 12 Principles of Green Chemistry**

From waste prevention to design for degradation, green chemistry principles guide us toward sustainable manufacturing.

**Our Journey**

At ChemOptima Solutions, we help companies reduce their environmental footprint while improving efficiency. Our AI-driven platform optimizes processes to:
- Reduce waste by 20-30%
- Lower energy consumption by 15-25%
- Improve yield by 10-20%
- Minimize hazardous byproducts

**Case Study: Pharmaceutical Manufacturing**

We worked with a pharmaceutical company to redesign their synthesis process. Results:
- 50% reduction in solvent usage
- 30% energy savings
- ₹50 lakhs annual cost savings
- Zero hazardous waste

**Technology Meets Chemistry**

We use:
- Process simulation (ASPEN)
- Machine learning for optimization
- Real-time monitoring
- Predictive maintenance

**The Business Case**

Sustainability isn't just good ethics - it's good business. Companies save money, reduce regulatory risk, and improve brand value.

**Call to Action**

Every chemical engineer graduating today has a responsibility. We must design processes that are sustainable from the start, not as an afterthought.

*Meera Krishnan is Director of Sustainability at ChemOptima Solutions and a 2011 graduate of IIT Kharagpur.*''',
            'category': 'Research',
            'author_id': user_ids['meera.krishnan@iitkgp.ac.in']
        },
        {
            'title': 'Lessons from My First Year as an Entrepreneur',
            'content': '''One year ago, I was a final year student with an idea. Today, RoboLearn serves 2 million students. Here are the brutal lessons I learned.

**Lesson 1: Ideas are Cheap, Execution is Everything**

I thought my idea was unique. It wasn't. What mattered was how well I executed it.

**Lesson 2: Fundraising is Hard**

I pitched to 50+ investors. Got rejected 47 times. Those 3 who said yes changed everything.

**Lesson 3: Hire Slow, Fire Fast**

My biggest mistake was hiring friends who weren't skilled. It took me 6 months to course-correct.

**Lesson 4: Product-Market Fit is Elusive**

Our first product failed. Our second pivoted three times. The third one finally clicked.

**Lesson 5: Mental Health Matters**

The stress of entrepreneurship is real. I burned out twice. Learning to take care of myself was crucial.

**The Reality Check**

- First 6 months: ₹0 revenue
- Month 7: First ₹10,000
- Month 9: Break-even
- Month 12: ₹50 lakhs ARR

**What Worked**

- Obsessing over customer feedback
- Building in public
- Networking relentlessly
- Learning from failures quickly
- Staying focused

**Advice**

If you're thinking of starting up:
1. Solve a real problem
2. Build an MVP quickly
3. Get customers before investors
4. Learn to sell
5. Be patient but persistent

The journey is hard, but incredibly rewarding. Would I do it again? Absolutely.

*Amit Singh is CTO at RoboLearn Inc, an EdTech startup serving 2M+ students.*''',
            'category': 'Startup',
            'author_id': user_ids['amit.singh@iitkgp.ac.in']
        }
    ]
    
    blog_post_ids = {}
    for post in blog_posts:
        safe_execute('''
            INSERT INTO blog_posts (title, content, category, author_id)
            VALUES (?, ?, ?, ?)
        ''', (post['title'], post['content'], post['category'], post['author_id']))
        blog_post_ids[post['title']] = cursor.lastrowid

    # ----------------- Mentorship Requests -----------------
    mentorship_requests = [
        {'student_id': user_ids['sneha.reddy@iitkgp.ac.in'], 'alumni_id': user_ids['rajesh.kumar@iitkgp.ac.in'], 
         'message': 'Hi Dr. Kumar, I am very interested in AI and healthcare. Your journey from IIT KGP to building MediAI is truly inspiring. I am currently working on a disease prediction project and would love to learn from your experience. Could you guide me on how to approach healthcare AI problems and navigate the regulatory landscape?', 
         'status': 'pending'},
        
        {'student_id': user_ids['karan.malhotra@iitkgp.ac.in'], 'alumni_id': user_ids['priya.sharma@iitkgp.ac.in'], 
         'message': 'Hello Priya, I am passionate about renewable energy and IoT. Your work with GreenGrid Technologies resonates with my interests. I am working on a smart grid optimization project and would appreciate guidance on sustainable energy solutions and how to make impact in this space.', 
         'status': 'accepted'},
        
        {'student_id': user_ids['neha.gupta@iitkgp.ac.in'], 'alumni_id': user_ids['rohan.desai@iitkgp.ac.in'], 
         'message': 'Hi Rohan, I am a biotechnology student interested in growth strategy for AgriTech. Your experience as Growth Advisor is fascinating. I am researching plant disease detection and would love to learn from your experience. How can I transition from research to building real-world solutions?', 
         'status': 'accepted'},
        
        {'student_id': user_ids['arjun.mehta@iitkgp.ac.in'], 'alumni_id': user_ids['amit.singh@iitkgp.ac.in'], 
         'message': 'Hello Amit, I am interested in robotics and automation, especially in manufacturing. As the captain of KGP Robotics Team, I am looking to understand career paths in this field. Your journey from student to CTO is inspiring. Could you mentor me on building autonomous systems and the entrepreneurship journey?', 
         'status': 'pending'},
        
        {'student_id': user_ids['divya.nair@iitkgp.ac.in'], 'alumni_id': user_ids['meera.krishnan@iitkgp.ac.in'], 
         'message': 'Hi Meera, I am a chemical engineering student passionate about sustainable manufacturing and green chemistry. Your work at ChemOptima Solutions perfectly aligns with my interests. I am researching process optimization and would appreciate your guidance on combining AI with chemical engineering.', 
         'status': 'pending'},
        
        {'student_id': user_ids['arjun.mehta@iitkgp.ac.in'], 'alumni_id': user_ids['rohan.desai@iitkgp.ac.in'], 
         'message': 'Hello Rohan, I am interested in growth strategy and scaling startups. Your work at GrowthX is amazing. I am building an autonomous robotics project and would love to understand how to take it to market. Could you share insights on GTM strategy and brand building?', 
         'status': 'accepted'},
        
        {'student_id': user_ids['sneha.reddy@iitkgp.ac.in'], 'alumni_id': user_ids['amit.singh@iitkgp.ac.in'], 
         'message': 'Hi Amit, I am considering entrepreneurship after graduation. Your blog post about lessons from your first year was eye-opening. I have an EdTech idea and would love your advice on getting started, fundraising, and avoiding common pitfalls.', 
         'status': 'accepted'},
    ]
    
    for req in mentorship_requests:
        safe_execute('''
            INSERT INTO mentorship_requests (student_id, alumni_id, message, status)
            VALUES (?, ?, ?, ?)
        ''', (req['student_id'], req['alumni_id'], req['message'], req['status']))
    
    # ----------------- Project Applications -----------------
    project_applications = [
        # AI Healthcare - ML Engineer position
        {'project_id': project_ids['AI-Powered Healthcare Diagnostics'], 
         'position_id': position_ids[f"{project_ids['AI-Powered Healthcare Diagnostics']}_ML Engineer"], 
         'student_id': user_ids['sneha.reddy@iitkgp.ac.in'], 
         'message': 'I have extensive experience with Python and TensorFlow through my coursework and personal projects. I completed Andrew Ng\'s Deep Learning Specialization and built a disease prediction system for my course project that achieved 92% accuracy. I am particularly interested in medical imaging and have been following MediAI\'s research papers. I would love to contribute to this life-saving project and learn from your team.', 
         'status': 'pending'},
        
        {'project_id': project_ids['AI-Powered Healthcare Diagnostics'], 
         'position_id': position_ids[f"{project_ids['AI-Powered Healthcare Diagnostics']}_ML Engineer"], 
         'student_id': user_ids['karan.malhotra@iitkgp.ac.in'], 
         'message': 'I have worked on computer vision projects including a real-time object detection system using YOLO and a facial recognition attendance system. I am passionate about healthcare AI and believe technology can democratize access to quality healthcare. I have strong Python skills and have implemented CNNs from scratch. I would bring dedication and quick learning ability to your team.', 
         'status': 'accepted'},
        
        # AI Healthcare - Backend Developer position
        {'project_id': project_ids['AI-Powered Healthcare Diagnostics'], 
         'position_id': position_ids[f"{project_ids['AI-Powered Healthcare Diagnostics']}_Backend Developer"], 
         'student_id': user_ids['arjun.mehta@iitkgp.ac.in'], 
         'message': 'Strong experience in Flask and PostgreSQL through multiple web development projects. I built a scalable REST API for our college fest registration system that handled 10,000+ concurrent users. I understand the importance of secure and efficient backend systems, especially in healthcare where patient data privacy is critical. Excited to contribute to MediAI\'s mission.', 
         'status': 'pending'},
        
        # Sustainable Energy - IoT Developer position
        {'project_id': project_ids['Sustainable Energy Management System'], 
         'position_id': position_ids[f"{project_ids['Sustainable Energy Management System']}_IoT Developer"], 
         'student_id': user_ids['karan.malhotra@iitkgp.ac.in'], 
         'message': 'I have hands-on experience with IoT and embedded systems. Built an IoT weather station using Arduino and Raspberry Pi that publishes real-time data via MQTT. Also worked on a solar panel monitoring system. I am passionate about renewable energy and would love to contribute to building a sustainable future. Your project aligns perfectly with my interests.', 
         'status': 'pending'},
        
        # Blockchain - Blockchain Developer position
        {'project_id': project_ids['Blockchain Supply Chain Tracker'], 
         'position_id': position_ids[f"{project_ids['Blockchain Supply Chain Tracker']}_Blockchain Developer"], 
         'student_id': user_ids['sneha.reddy@iitkgp.ac.in'], 
         'message': 'I have been learning blockchain and smart contracts through online courses and hackathons. Built a basic supply chain tracker using Ethereum and Solidity as a learning project. I am fascinated by how blockchain can bring transparency and trust to supply chains. This project would be an incredible opportunity to work on production-level blockchain applications.', 
         'status': 'declined'},
        
        # Smart Agriculture - IoT Engineer position (filled)
        {'project_id': project_ids['Smart Agriculture Monitoring'], 
         'position_id': position_ids[f"{project_ids['Smart Agriculture Monitoring']}_IoT Engineer"], 
         'student_id': user_ids['neha.gupta@iitkgp.ac.in'], 
         'message': 'As a biotechnology student, I am very interested in AgriTech. I have experience with IoT sensors from my lab work and built a prototype plant health monitoring system using Arduino and various sensors (soil moisture, pH, temperature). Combining my biotech knowledge with IoT skills, I can contribute unique insights to your project. Agriculture is personal to me as I come from a farming family.', 
         'status': 'accepted'},
        
        # Smart Agriculture - Full Stack Developer position
        {'project_id': project_ids['Smart Agriculture Monitoring'],
         'position_id': position_ids[f"{project_ids['Smart Agriculture Monitoring']}_Full Stack Developer"],
         'student_id': user_ids['sneha.reddy@iitkgp.ac.in'],
         'message': 'Experienced with MERN stack through multiple projects. Built a real-time dashboard for our robotics team that displays sensor data using Chart.js and Socket.io. I am excited about using technology to help farmers. Creating intuitive interfaces that farmers can easily use is a challenge I would love to tackle. Agriculture needs better technology solutions and I want to be part of that change.',
         'status': 'pending',
         'has_team': True},
        
        # Urban Infrastructure - GIS Specialist position
        {'project_id': project_ids['Urban Infrastructure Planning Tool'],
         'position_id': position_ids[f"{project_ids['Urban Infrastructure Planning Tool']}_GIS Specialist"],
         'student_id': user_ids['karan.malhotra@iitkgp.ac.in'],
         'message': 'I am an electrical engineering student with interest in smart cities and GIS. I have worked on IoT-based urban monitoring and traffic flow simulation. I am passionate about smart cities and sustainable urban development. India\'s urbanization presents unique challenges and I want to be part of building cities that are livable, sustainable, and inclusive.',
         'status': 'pending',
         'has_team': False},
        
        # Chemical Process - Process Engineer position (filled)
        {'project_id': project_ids['Chemical Process Optimization Platform'],
         'position_id': position_ids[f"{project_ids['Chemical Process Optimization Platform']}_Process Engineer"],
         'student_id': user_ids['divya.nair@iitkgp.ac.in'],
         'message': 'I have strong background in chemical engineering and Python. Worked with ASPEN for process simulation in multiple course projects. I am passionate about sustainable manufacturing and green chemistry. Built an optimization model for waste water treatment that reduced chemical usage by 25%. Excited about using AI to make chemical processes more efficient and sustainable.',
         'status': 'accepted',
         'has_team': True},
        
        # Robotics - Robotics Engineer position
        {'project_id': project_ids['Robotics for Manufacturing Automation'],
         'position_id': position_ids[f"{project_ids['Robotics for Manufacturing Automation']}_Robotics Engineer"],
         'student_id': user_ids['arjun.mehta@iitkgp.ac.in'],
         'message': 'I have extensive experience with ROS and robotics through KGP Robotics Team (where I am captain). Built multiple autonomous robots including a line-following robot and a 6-DOF robotic arm. I am very passionate about automation and manufacturing. Understanding inverse kinematics, PID control, and sensor integration. This project is exactly what I want to work on.',
         'status': 'pending',
         'has_team': False},
        
        # Robotics - Computer Vision Engineer position
        {'project_id': project_ids['Robotics for Manufacturing Automation'],
         'position_id': position_ids[f"{project_ids['Robotics for Manufacturing Automation']}_Computer Vision Engineer"],
         'student_id': user_ids['sneha.reddy@iitkgp.ac.in'],
         'message': 'Worked on multiple OpenCV projects including object detection, facial recognition, and defect detection systems. Built a quality inspection system for my course project that achieved 97% accuracy in detecting defects. I am excited about applying computer vision to manufacturing and quality control. Manufacturing automation is the future and I want to contribute to building it.',
         'status': 'pending',
         'has_team': True},
        
        # Additional applications for diversity
        {'project_id': project_ids['Sustainable Energy Management System'],
         'position_id': position_ids[f"{project_ids['Sustainable Energy Management System']}_Data Analyst"],
         'student_id': user_ids['divya.nair@iitkgp.ac.in'],
         'message': 'Strong Python and data analytics skills. Built multiple dashboards using Power BI and Python for process data visualization. Interested in renewable energy and sustainability. Would love to analyze energy patterns and help optimize grid performance.',
         'status': 'pending',
         'has_team': False},
    ]
    
    for app in project_applications:
        safe_execute('''
            INSERT INTO project_applications (project_id, position_id, student_id, message, status, has_team, feedback, completed_at, is_completed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (app['project_id'], app['position_id'], app['student_id'], app['message'], app['status'], 
              app.get('has_team', False), app.get('feedback'), app.get('completed_at'), app.get('is_completed', False)))

    # ----------------- Conversations & Messages -----------------
    conversation_pairs = [
        ('sneha.reddy@iitkgp.ac.in', 'rajesh.kumar@iitkgp.ac.in'),
        ('karan.malhotra@iitkgp.ac.in', 'priya.sharma@iitkgp.ac.in'),
        ('neha.gupta@iitkgp.ac.in', 'ananya.iyer@iitkgp.ac.in'),
        ('arjun.mehta@iitkgp.ac.in', 'meera.krishnan@iitkgp.ac.in'),
    ]
    
    message_templates = [
        ["Hi! I hope this message finds you well.", "Hello! Yes, I'm doing great. How can I help you?", "I wanted to discuss the project opportunity.", "Sure! Let's schedule a call.", "That would be great! When are you available?"],
        ["Thank you for accepting my mentorship request!", "You're welcome! I'm happy to help.", "I have some questions about career paths.", "Feel free to ask anything.", "How did you decide to start your own company?"],
        ["I saw your project posting and I'm very interested.", "Great! Tell me about your experience.", "I've worked on similar technologies in my coursework.", "That sounds promising. Let's discuss further.", "Looking forward to working together!"],
        ["Your blog post was really inspiring!", "Thank you! I'm glad it helped.", "The lessons about entrepreneurship were valuable.", "Failure teaches more than success.", "That's so true. Thanks for sharing your journey."]
    ]
    
    for idx, (u1, u2) in enumerate(conversation_pairs):
        user1_id = user_ids[u1]
        user2_id = user_ids[u2]
        
        safe_execute('''
            INSERT INTO conversations (user1_id, user2_id)
            VALUES (?, ?)
        ''', (min(user1_id, user2_id), max(user1_id, user2_id)))
        conv_id = cursor.lastrowid
        
        # Add messages
        messages = message_templates[idx % len(message_templates)]
        for i, msg_content in enumerate(messages):
            sender = user1_id if i % 2 == 0 else user2_id
            receiver = user2_id if i % 2 == 0 else user1_id
            safe_execute('''
                INSERT INTO messages (sender_id, receiver_id, content, is_read)
                VALUES (?, ?, ?, ?)
            ''', (sender, receiver, msg_content, 1 if i < len(messages) - 2 else 0))

    # ----------------- Blog Likes -----------------
    # Students like alumni blog posts
    student_emails = ['sneha.reddy@iitkgp.ac.in', 'karan.malhotra@iitkgp.ac.in', 
                      'neha.gupta@iitkgp.ac.in', 'arjun.mehta@iitkgp.ac.in',
                      'divya.nair@iitkgp.ac.in']
    
    for post_title, post_id in blog_post_ids.items():
        # Each post gets likes from 3-5 random students
        num_likes = random.randint(3, 5)
        liking_students = random.sample(student_emails, num_likes)
        for student_email in liking_students:
            safe_execute('''
                INSERT OR IGNORE INTO blog_likes (blog_post_id, user_id)
                VALUES (?, ?)
            ''', (post_id, user_ids[student_email]))

    # ----------------- Services -----------------
    services_data = [
        {
            'provider_email': 'rajesh.kumar@iitkgp.ac.in',
            'title': 'Web development',
            'description': 'Full-stack web development: responsive sites, SPAs, and backend APIs. We build with modern stacks (React, Node, Python) and deliver scalable, secure applications.',
            'category': 'Web development',
            'price_range': '₹1,50,000 - ₹9,00,000',
            'delivery_time': '3-8 weeks',
            'image_url': 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&q=80&w=2070'
        },
        {
            'provider_email': 'priya.sharma@iitkgp.ac.in',
            'title': 'App development',
            'description': 'Native and cross-platform mobile app development for iOS and Android. From MVP to production: UX, APIs, and app store deployment.',
            'category': 'App development',
            'price_range': '₹2,00,000 - ₹10,00,000',
            'delivery_time': '4-10 weeks',
            'image_url': 'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?auto=format&fit=crop&q=80&w=2070'
        },
        {
            'provider_email': 'amit.singh@iitkgp.ac.in',
            'title': 'UI/UX designing',
            'description': 'User research, wireframes, high-fidelity UI, and design systems. We create intuitive, accessible interfaces that users love.',
            'category': 'UI/UX designing',
            'price_range': '₹1,00,000 - ₹5,50,000',
            'delivery_time': '2-6 weeks',
            'image_url': 'https://images.unsplash.com/photo-1561070791-2526d31d5b35?auto=format&fit=crop&q=80&w=2070'
        },
        {
            'provider_email': 'vikram.patel@iitkgp.ac.in',
            'title': 'Case Studies and Analytics',
            'description': 'Data-driven case studies and analytics: market research, KPI dashboards, and actionable insights for strategy and operations.',
            'category': 'Case Studies and Analytics',
            'price_range': '₹1,75,000 - ₹7,00,000',
            'delivery_time': '3-6 weeks',
            'image_url': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=2070'
        },
        {
            'provider_email': 'meera.krishnan@iitkgp.ac.in',
            'title': 'Rag Implementation',
            'description': 'Retrieval-augmented generation (RAG) implementation for your data and LLMs. We design pipelines for accurate, source-grounded AI responses.',
            'category': 'Rag Implementation',
            'price_range': '₹2,50,000 - ₹14,00,000',
            'delivery_time': '4-10 weeks',
            'image_url': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=2070'
        },
        {
            'provider_email': 'sneha.reddy@iitkgp.ac.in',
            'title': 'Sales AI booster',
            'description': 'AI-powered sales tools: lead scoring, outreach automation, and CRM integration to accelerate pipeline and close more deals.',
            'category': 'Sales AI booster',
            'price_range': '₹2,00,000 - ₹10,00,000',
            'delivery_time': '4-8 weeks',
            'image_url': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&q=80&w=2070'
        }
    ]
    
    for service in services_data:
        if service['provider_email'] in user_ids:
            safe_execute('''
                INSERT INTO services (provider_id, title, description, category, price_range, delivery_time, image_url, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_ids[service['provider_email']],
                service['title'],
                service['description'],
                service['category'],
                service.get('price_range'),
                service.get('delivery_time'),
                service.get('image_url'),
                True
            ))

    # ----------------- Service timeline items (mock "How we do it" for each service) -----------------
    safe_execute('SELECT id FROM services ORDER BY id')
    service_ids = [row[0] for row in cursor.fetchall()]
    timeline_template = [
        {
            'title': 'Discovery call',
            'description': 'We align on your goals, scope, and timeline in a 30-minute call. You share your brief and we outline the approach.',
            'date': '2024-01-15',
            'image': 'https://images.unsplash.com/photo-1551434678-e076c223a692?w=400&auto=format&fit=crop&q=60',
            'status': 'completed',
            'category': 'Kickoff',
            'sort_order': 0,
        },
        {
            'title': 'Proposal & agreement',
            'description': 'You receive a detailed proposal with deliverables, milestones, and pricing. Once approved, we sign and get started.',
            'date': '2024-01-22',
            'image': 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=400&auto=format&fit=crop&q=60',
            'status': 'completed',
            'category': 'Planning',
            'sort_order': 1,
        },
        {
            'title': 'Sprint kickoff',
            'description': 'We set up communication channels, share the project plan, and begin the first sprint with regular check-ins.',
            'date': '2024-02-01',
            'image': 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400&auto=format&fit=crop&q=60',
            'status': 'current',
            'category': 'Execution',
            'sort_order': 2,
        },
        {
            'title': 'Delivery & review',
            'description': 'We deliver milestones on time, incorporate your feedback, and run UAT. Final deliverables are handed over with documentation.',
            'date': '2024-03-01',
            'image': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=400&auto=format&fit=crop&q=60',
            'status': 'upcoming',
            'category': 'Delivery',
            'sort_order': 3,
        },
        {
            'title': 'Handover & support',
            'description': 'We hand over the project, provide a support window, and share knowledge so your team can own it going forward.',
            'date': '2024-03-15',
            'image': 'https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=400&auto=format&fit=crop&q=60',
            'status': 'upcoming',
            'category': 'Closure',
            'sort_order': 4,
        },
    ]
    for service_id in service_ids:
        for item in timeline_template:
            safe_execute('''
                INSERT INTO service_timeline_items (service_id, title, description, date, image, status, category, sort_order)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                service_id,
                item['title'],
                item['description'],
                item['date'],
                item['image'],
                item['status'],
                item['category'],
                item['sort_order'],
            ))
    print("✓ Service timeline items seeded (%d items × %d services)" % (len(timeline_template), len(service_ids)))

    # ----------------- Service reviews (Reviews & Past Work) -----------------
    reviews_template = [
        {'author_name': 'Priya Sharma', 'content': 'Professional delivery and clear communication throughout. Would recommend for similar projects.', 'rating': 5},
        {'author_name': 'Rohan Verma', 'content': 'Great experience. The team understood our requirements quickly and delivered on time. Past work quality was as expected.', 'rating': 5},
        {'author_name': 'Ananya Reddy', 'content': 'Smooth collaboration and solid output. We have engaged them for a follow-up project.', 'rating': 4},
    ]
    for service_id in service_ids:
        for r in reviews_template:
            safe_execute('''
                INSERT INTO service_reviews (service_id, author_name, content, rating, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (service_id, r['author_name'], r['content'], r['rating'], (datetime.now() - timedelta(days=random.randint(5, 60))).strftime('%Y-%m-%d %H:%M:%S')))
    print("✓ Service reviews seeded (%d reviews × %d services)" % (len(reviews_template), len(service_ids)))

    # ----------------- Courses -----------------
    courses = [
        {
            'title': 'Full Stack Web Development',
            'description': 'Master the MERN stack with this comprehensive course. Learn React, Node.js, Express, and MongoDB by building real-world projects.',
            'perks': 'Job assistance, 1-on-1 mentorship, Certification',
            'timeline': 'Week 1-4: Frontend (React)\nWeek 5-8: Backend (Node.js)\nWeek 9-12: Full Stack Project',
            'duration': '12 Weeks',
            'assignments': '5 Major Projects, 10+ Mini Projects',
            'category': 'Development',
            'image_url': 'https://images.unsplash.com/photo-1593720213428-28a5b9e94613?q=80&w=1200&auto=format&fit=crop',
            'price': 4999,
            'start_date': (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
        },
        {
            'title': 'Data Science Bootcamp',
            'description': 'Become a Data Scientist in 16 weeks. Learn Python, SQL, Machine Learning, and Deep Learning.',
            'perks': 'Portfolio reviews, Kaggle competition prep, Industry expert sessions',
            'timeline': 'Month 1: Python & SQL\nMonth 2: ML Algorithms\nMonth 3: Deep Learning\nMonth 4: Final Capstone',
            'duration': '16 Weeks',
            'assignments': '3 Case Studies, 1 Capstone Project',
            'category': 'Data Science',
            'image_url': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=1200&auto=format&fit=crop',
            'price': 6999,
            'start_date': (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d')
        },
        {
            'title': 'UI/UX Design Masterclass',
            'description': 'Learn to design beautiful and functional user interfaces. Master Figma, prototyping, and design systems.',
            'perks': 'Portfolio building, Design critique sessions',
            'timeline': 'Week 1-2: Design Theory\nWeek 3-4: Figma Mastery\nWeek 5-6: Prototyping\nWeek 7-8: Capstone',
            'duration': '8 Weeks',
            'assignments': 'Redesign App, Create Design System',
            'category': 'Design',
            'image_url': 'https://images.unsplash.com/photo-1561070791-2526d30994b5?q=80&w=1200&auto=format&fit=crop',
            'price': 3499,
            'start_date': (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
        }
    ]

    for course in courses:
        safe_execute('''
            INSERT INTO courses (title, description, perks, timeline, duration, assignments, category, image_url, price, start_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (course['title'], course['description'], course['perks'], course['timeline'], 
              course['duration'], course['assignments'], course['category'], course['image_url'], 
              course['price'], course['start_date']))
    
    print("✓ Courses seeded")

    # ----------------- Events -----------------
    events = [
        {
            'title': 'Tech Leaders Podcast: Future of AI',
            'description': 'Join us for an insightful podcast with industry leaders discussing the future of Artificial Intelligence and its impact on the job market.',
            'type': 'Podcast',
            'date': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
            'time': '18:00',
            'location': 'Spotify / Apple Podcasts',
            'image_url': 'https://images.unsplash.com/photo-1478737270239-2f02b77ac6d5?q=80&w=1200&auto=format&fit=crop'
        },
        {
            'title': 'Startup Fundraising Seminar',
            'description': 'Learn the secrets of successful fundraising from founders who have raised millions. Topics include pitch decks, valuation, and investor relations.',
            'type': 'Seminar',
            'date': (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'),
            'time': '10:00',
            'location': 'Netaji Auditorium',
            'image_url': 'https://images.unsplash.com/photo-1515187029135-18ee286d815b?q=80&w=1200&auto=format&fit=crop'
        },
        {
            'title': 'Webinar: Cracking the Product Management Interview',
            'description': 'A comprehensive guide to ace your PM interviews. We will cover case studies, behavioral questions, and mock interviews.',
            'type': 'Webinar',
            'date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'time': '19:00',
            'location': 'Zoom (Link will be shared)',
            'image_url': 'https://images.unsplash.com/photo-1556761175-4b46a572b786?q=80&w=1200&auto=format&fit=crop'
        },
        {
            'title': 'Fundae Session: Campus Life Hacks',
            'description': 'Seniors share their tips and tricks for navigating campus life, from choosing electives to finding the best food spots.',
            'type': 'Fundae Session',
            'date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'time': '20:00',
            'location': 'Old Main Building',
            'image_url': 'https://images.unsplash.com/photo-1523580494863-6f3031224c94?q=80&w=1200&auto=format&fit=crop'
        },
        {
            'title': 'Discussion Circle: Sustainable Development',
            'description': 'An open discussion on sustainable development goals and how students can contribute. Everyone is welcome to share their ideas.',
            'type': 'Meeting',
            'date': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
            'time': '17:00',
            'location': 'TSG Conference Room',
            'image_url': 'https://images.unsplash.com/photo-1573164713988-8665fc963095?q=80&w=1200&auto=format&fit=crop'
        }
    ]

    for event in events:
        safe_execute('''
            INSERT INTO events (title, description, type, date, time, location, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (event['title'], event['description'], event['type'], event['date'], event['time'], event['location'], event['image_url']))
    
    print("✓ Events seeded")

    # ----------------- LaunchDeck: Pitches -----------------
    print("\n🚀 Seeding LaunchDeck data...")
    
    # Get founder and investor IDs for LaunchDeck
    founder_emails = ['rajesh.kumar@iitkgp.ac.in', 'amit.singh@iitkgp.ac.in', 'riya.chakraborty@iitkgp.ac.in', 'siddharth.joshi@iitkgp.ac.in']
    investor_emails = ['ananya.iyer@iitkgp.ac.in', 'vikram.patel@iitkgp.ac.in', 'tanya.bose@iitkgp.ac.in']
    mentor_emails = ['priya.sharma@iitkgp.ac.in', 'meera.krishnan@iitkgp.ac.in', 'rohan.desai@iitkgp.ac.in']
    
    pitches = [
        {
            'founder_id': user_ids['rajesh.kumar@iitkgp.ac.in'],
            'title': 'NeuralMesh AI',
            'tagline': 'Democratizing Machine Learning for Every Business',
            'pitch_overview': 'NeuralMesh AI provides no-code ML tools that enable small and medium businesses to build, deploy, and manage machine learning models without data science expertise. Our platform reduces ML development time by 80% and cost by 60%.',
            'highlights': json.dumps(['$2M ARR', '150+ Enterprise Clients', 'Google AI Partnership', '3x YoY Growth']),
            'team_members': json.dumps([{'name': 'Dr. Rajesh Kumar', 'role': 'CEO & Founder'}, {'name': 'Arun Nair', 'role': 'CTO'}, {'name': 'Deepika Rao', 'role': 'VP Product'}]),
            'pitch_deck_images': json.dumps(['https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800', 'https://images.unsplash.com/photo-1555949963-aa79dcee981d?w=800', 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800']),
            'category': 'AI/ML',
            'website': 'https://neuralmesh.ai',
            'social_links': json.dumps({'linkedin': 'https://linkedin.com/company/neuralmesh', 'twitter': 'https://twitter.com/neuralmesh'}),
            'status': 'published'
        },
        {
            'founder_id': user_ids['amit.singh@iitkgp.ac.in'],
            'title': 'GreenHarvest AgriTech',
            'tagline': 'AI-Powered Precision Agriculture for Indian Farmers',
            'pitch_overview': 'GreenHarvest uses IoT sensors and AI/ML to provide real-time crop health monitoring, smart irrigation, and yield optimization. We help farmers increase yield by 30% while reducing water usage by 40%.',
            'highlights': json.dumps(['500+ Acres Deployed', '40% Water Savings', 'Forbes 30 Under 30', 'ICAR Partnership']),
            'team_members': json.dumps([{'name': 'Amit Singh', 'role': 'Co-founder & CTO'}, {'name': 'Kavya Reddy', 'role': 'Co-founder & CEO'}, {'name': 'Nikhil Sharma', 'role': 'Head of Agronomy'}]),
            'pitch_deck_images': json.dumps(['https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=800', 'https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?w=800', 'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=800']),
            'category': 'AgriTech',
            'website': 'https://greenharvest.in',
            'social_links': json.dumps({'linkedin': 'https://linkedin.com/company/greenharvest'}),
            'status': 'published'
        },
        {
            'founder_id': user_ids['riya.chakraborty@iitkgp.ac.in'],
            'title': 'EduVerse Technologies',
            'tagline': 'Immersive Virtual Campus Experiences for Everyone',
            'pitch_overview': 'EduVerse creates AR/VR-powered virtual campus tours and immersive learning experiences. Students can explore campuses, attend virtual lectures, and collaborate in 3D spaces from anywhere in the world.',
            'highlights': json.dumps(['50+ University Partners', '100K+ Virtual Tours', 'Microsoft for Startups', 'Series A Ready']),
            'team_members': json.dumps([{'name': 'Riya Chakraborty', 'role': 'Founder & CEO'}, {'name': 'Arjun Das', 'role': 'Head of Engineering'}, {'name': 'Pooja Verma', 'role': 'VP Design'}]),
            'pitch_deck_images': json.dumps(['https://images.unsplash.com/photo-1592478411213-6153e4ebc07d?w=800', 'https://images.unsplash.com/photo-1593508512255-86ab42a8e620?w=800', 'https://images.unsplash.com/photo-1531482615713-2afd69097998?w=800']),
            'category': 'EdTech',
            'website': 'https://eduverse.tech',
            'social_links': json.dumps({'linkedin': 'https://linkedin.com/company/eduverse', 'twitter': 'https://twitter.com/eduverse'}),
            'status': 'published'
        },
        {
            'founder_id': user_ids['siddharth.joshi@iitkgp.ac.in'],
            'title': 'PaySwift',
            'tagline': 'Instant Cross-Border Payments for the Global Workforce',
            'pitch_overview': 'PaySwift enables freelancers and remote workers to receive international payments instantly with the lowest fees in the market. Our blockchain-based infrastructure reduces transaction costs by 70% compared to traditional methods.',
            'highlights': json.dumps(['$5M Monthly Volume', '25K Active Users', 'RBI Sandbox Selected', 'Razorpay Alumni Founded']),
            'team_members': json.dumps([{'name': 'Siddharth Joshi', 'role': 'Co-founder'}, {'name': 'Ankita Mishra', 'role': 'Co-founder & CEO'}, {'name': 'Rahul Agarwal', 'role': 'Head of Compliance'}]),
            'pitch_deck_images': json.dumps(['https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800', 'https://images.unsplash.com/photo-1621761191319-c6fb62004040?w=800', 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800']),
            'category': 'FinTech',
            'website': 'https://payswift.io',
            'social_links': json.dumps({'linkedin': 'https://linkedin.com/company/payswift'}),
            'status': 'published'
        },
        {
            'founder_id': user_ids['rajesh.kumar@iitkgp.ac.in'],
            'title': 'MediScan Pro',
            'tagline': 'AI Diagnostics for Rural Healthcare',
            'pitch_overview': 'MediScan Pro brings AI-powered medical diagnostics to rural clinics. Our portable device + AI platform can screen for 15+ conditions from a simple blood sample, providing results in under 10 minutes.',
            'highlights': json.dumps(['95% Diagnostic Accuracy', 'ICMR Partnership', '200+ Rural Clinics', 'WHO Innovation Award']),
            'team_members': json.dumps([{'name': 'Dr. Rajesh Kumar', 'role': 'Founder'}, {'name': 'Dr. Sneha Rao', 'role': 'Chief Medical Officer'}, {'name': 'Vikash Gupta', 'role': 'CTO'}]),
            'pitch_deck_images': json.dumps(['https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=800', 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800', 'https://images.unsplash.com/photo-1581093588401-16f2d7f3d8ac?w=800']),
            'category': 'HealthTech',
            'website': 'https://mediscanpro.in',
            'social_links': json.dumps({'linkedin': 'https://linkedin.com/company/mediscanpro'}),
            'status': 'published'
        },
        {
            'founder_id': user_ids['riya.chakraborty@iitkgp.ac.in'],
            'title': 'SkillBridge',
            'tagline': 'Connecting Campus Talent with Industry Projects',
            'pitch_overview': 'SkillBridge matches university students with real industry projects, providing hands-on experience while companies get quality work done. Think Upwork meets Campus Placement.',
            'highlights': json.dumps(['10K+ Student Profiles', '500+ Company Projects', '85% Placement Rate', 'NIT/IIT Network']),
            'team_members': json.dumps([{'name': 'Riya Chakraborty', 'role': 'Co-founder'}, {'name': 'Manish Kapoor', 'role': 'Co-founder & CTO'}]),
            'pitch_deck_images': json.dumps(['https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800', 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800']),
            'category': 'EdTech',
            'website': 'https://skillbridge.io',
            'social_links': json.dumps({'linkedin': 'https://linkedin.com/company/skillbridge'}),
            'status': 'published'
        }
    ]
    
    pitch_ids = []
    for pitch in pitches:
        safe_execute('''INSERT INTO pitches (founder_id, title, tagline, pitch_overview, highlights,
                          team_members, pitch_deck_images, category, website, social_links, status)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (pitch['founder_id'], pitch['title'], pitch['tagline'], pitch['pitch_overview'],
                        pitch['highlights'], pitch['team_members'], pitch['pitch_deck_images'],
                        pitch['category'], pitch['website'], pitch['social_links'], pitch['status']))
        pitch_ids.append(cursor.lastrowid)
    print(f"✓ LaunchDeck pitches seeded ({len(pitches)} pitches)")
    
    # ----------------- LaunchDeck: Investor Interests -----------------
    # Status values: 'pending', 'admin_notified', 'meeting_setup'
    interests = [
        {'pitch_id': pitch_ids[0], 'investor_id': user_ids['ananya.iyer@iitkgp.ac.in'], 'message': 'Very impressed with NeuralMesh\'s traction. Would love to discuss the enterprise GTM strategy and unit economics. Can we schedule a call?', 'status': 'pending'},
        {'pitch_id': pitch_ids[0], 'investor_id': user_ids['vikram.patel@iitkgp.ac.in'], 'message': 'Interesting approach to democratizing ML. What\'s the competitive moat against larger players like DataRobot?', 'status': 'pending'},
        {'pitch_id': pitch_ids[1], 'investor_id': user_ids['tanya.bose@iitkgp.ac.in'], 'message': 'AgriTech is a focus area for us. The farmer adoption numbers are impressive. What\'s the retention rate?', 'status': 'admin_notified'},
        {'pitch_id': pitch_ids[1], 'investor_id': user_ids['ananya.iyer@iitkgp.ac.in'], 'message': 'Love the impact metrics. How does the unit economics look per acre?', 'status': 'pending'},
        {'pitch_id': pitch_ids[2], 'investor_id': user_ids['vikram.patel@iitkgp.ac.in'], 'message': 'AR/VR in education is a space I believe in strongly. What\'s the revenue model?', 'status': 'meeting_setup'},
        {'pitch_id': pitch_ids[3], 'investor_id': user_ids['ananya.iyer@iitkgp.ac.in'], 'message': 'Cross-border payments is a massive market. How are you handling regulatory compliance across countries?', 'status': 'pending'},
        {'pitch_id': pitch_ids[3], 'investor_id': user_ids['tanya.bose@iitkgp.ac.in'], 'message': 'RBI sandbox selection is a great validation. What\'s the path to full RBI approval?', 'status': 'admin_notified'},
        {'pitch_id': pitch_ids[4], 'investor_id': user_ids['tanya.bose@iitkgp.ac.in'], 'message': 'HealthTech is our core focus. The rural healthcare angle is compelling. What\'s the distribution strategy?', 'status': 'meeting_setup'},
    ]
    
    for interest in interests:
        safe_execute('''INSERT INTO pitch_interests (pitch_id, investor_id, message, status)
                          VALUES (?, ?, ?, ?)''',
                       (interest['pitch_id'], interest['investor_id'], interest['message'], interest['status']))
    print(f"✓ LaunchDeck investor interests seeded ({len(interests)} interests)")
    
    # ----------------- LaunchDeck: Mentorship Requests -----------------
    ld_mentorship = [
        {'founder_id': user_ids['rajesh.kumar@iitkgp.ac.in'], 'mentor_id': user_ids['priya.sharma@iitkgp.ac.in'], 'pitch_id': pitch_ids[0], 'message': 'Would love your guidance on product-market fit for our enterprise ML platform. Your experience with successful exits would be invaluable.', 'status': 'accepted'},
        {'founder_id': user_ids['amit.singh@iitkgp.ac.in'], 'mentor_id': user_ids['rohan.desai@iitkgp.ac.in'], 'pitch_id': pitch_ids[1], 'message': 'Need help with GTM strategy for GreenHarvest. How do we scale farmer acquisition beyond our current network?', 'status': 'accepted'},
        {'founder_id': user_ids['riya.chakraborty@iitkgp.ac.in'], 'mentor_id': user_ids['meera.krishnan@iitkgp.ac.in'], 'pitch_id': pitch_ids[2], 'message': 'Looking for advice on scaling engineering teams as we prepare for Series A. Your experience at Amazon and Netflix would be incredibly helpful.', 'status': 'pending'},
        {'founder_id': user_ids['siddharth.joshi@iitkgp.ac.in'], 'mentor_id': user_ids['priya.sharma@iitkgp.ac.in'], 'pitch_id': pitch_ids[3], 'message': 'Need guidance on navigating regulatory challenges in FinTech. How do we balance innovation with compliance?', 'status': 'pending'},
        {'founder_id': user_ids['rajesh.kumar@iitkgp.ac.in'], 'mentor_id': user_ids['rohan.desai@iitkgp.ac.in'], 'pitch_id': pitch_ids[4], 'message': 'Seeking advice on brand building and marketing strategy for MediScan Pro in the rural healthcare space.', 'status': 'accepted'},
    ]
    
    for req in ld_mentorship:
        safe_execute('''INSERT INTO launchdeck_mentorship_requests (founder_id, mentor_id, pitch_id, message, status)
                          VALUES (?, ?, ?, ?, ?)''',
                       (req['founder_id'], req['mentor_id'], req['pitch_id'], req['message'], req['status']))
    print(f"✓ LaunchDeck mentorship requests seeded ({len(ld_mentorship)} requests)")
    
    # ----------------- LaunchDeck: Admin Notifications -----------------
    now = datetime.now()
    notifications = [
        {'message': 'New pitch submitted: NeuralMesh AI by Dr. Rajesh Kumar', 'type': 'new_pitch', 'reference_id': pitch_ids[0], 'is_read': False, 'created_at': (now - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')},
        {'message': 'New pitch submitted: GreenHarvest AgriTech by Amit Singh', 'type': 'new_pitch', 'reference_id': pitch_ids[1], 'is_read': False, 'created_at': (now - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S')},
        {'message': 'New pitch submitted: EduVerse Technologies by Riya Chakraborty', 'type': 'new_pitch', 'reference_id': pitch_ids[2], 'is_read': True, 'created_at': (now - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')},
        {'message': 'New pitch submitted: PaySwift by Siddharth Joshi', 'type': 'new_pitch', 'reference_id': pitch_ids[3], 'is_read': True, 'created_at': (now - timedelta(days=1, hours=3)).strftime('%Y-%m-%d %H:%M:%S')},
        {'message': 'Investor Ananya Iyer showed interest in NeuralMesh AI', 'type': 'investor_interest', 'reference_id': pitch_ids[0], 'is_read': False, 'created_at': (now - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')},
        {'message': 'Investor Vikram Patel showed interest in NeuralMesh AI', 'type': 'investor_interest', 'reference_id': pitch_ids[0], 'is_read': False, 'created_at': (now - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')},
        {'message': 'Investor Tanya Bose showed interest in GreenHarvest AgriTech', 'type': 'investor_interest', 'reference_id': pitch_ids[1], 'is_read': True, 'created_at': (now - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')},
        {'message': 'Meeting setup: Vikram Patel ↔ EduVerse Technologies', 'type': 'meeting_setup', 'reference_id': pitch_ids[2], 'is_read': False, 'created_at': (now - timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S')},
        {'message': 'Meeting setup: Tanya Bose ↔ MediScan Pro', 'type': 'meeting_setup', 'reference_id': pitch_ids[4], 'is_read': False, 'created_at': (now - timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S')},
        {'message': 'Mentorship request accepted: Priya Sharma will mentor NeuralMesh AI', 'type': 'mentorship_update', 'reference_id': pitch_ids[0], 'is_read': True, 'created_at': (now - timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')},
        {'message': 'Mentorship request accepted: Rohan Desai will mentor GreenHarvest AgriTech', 'type': 'mentorship_update', 'reference_id': pitch_ids[1], 'is_read': True, 'created_at': (now - timedelta(days=2, hours=5)).strftime('%Y-%m-%d %H:%M:%S')},
        {'message': 'New pitch submitted: MediScan Pro by Dr. Rajesh Kumar', 'type': 'new_pitch', 'reference_id': pitch_ids[4], 'is_read': False, 'created_at': (now - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')},
    ]
    
    for notif in notifications:
        safe_execute('''INSERT INTO admin_notifications (type, reference_id, message, is_read, created_at)
                          VALUES (?, ?, ?, ?, ?)''',
                       (notif['type'], notif['reference_id'], notif['message'], notif['is_read'], notif['created_at']))
    print(f"✓ LaunchDeck admin notifications seeded ({len(notifications)} notifications)")

    conn.commit()
    conn.close()
    print("\n✅ Database seeded successfully with comprehensive data!")
    print("\n📊 Summary:")
    print(f"   - Users: {len(users)} (4 Founders, 3 Investors, 3 Mentors, 5 Students)")
    print(f"   - Projects: {len(projects)}")
    print(f"   - Services: {len(services_data)}")
    print(f"   - Project Positions: {len(project_positions)}")
    print(f"   - Blog Posts: {len(blog_posts)}")
    print(f"   - Mentorship Requests: {len(mentorship_requests)}")
    print(f"   - Project Applications: {len(project_applications)}")
    print(f"   - Conversations: {len(conversation_pairs)}")
    print(f"   - LaunchDeck Pitches: {len(pitches)}")
    print(f"   - LaunchDeck Investor Interests: {len(interests)}")
    print(f"   - LaunchDeck Mentorship Requests: {len(ld_mentorship)}")
    print(f"   - LaunchDeck Notifications: {len(notifications)}")
    print(f"   - Skills, Achievements, and Languages added for all users")
    print("\n🔐 Login credentials (all passwords: password123):")
    print("   Admin:    Admin@kgplaunchpad.in / IITKGP2026")
    print("   Founder:  rajesh.kumar@iitkgp.ac.in")
    print("   Investor: ananya.iyer@iitkgp.ac.in")
    print("   Mentor:   priya.sharma@iitkgp.ac.in")
    print("   Student:  sneha.reddy@iitkgp.ac.in")

if __name__ == '__main__':
    seed_database()