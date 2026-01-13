import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import json
import random
from app import init_db

def seed_database():
    # Initialize database tables first
    init_db()
    
    conn = sqlite3.connect('launchpad.db')
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute('DELETE FROM project_applications')
    cursor.execute('DELETE FROM project_positions')
    cursor.execute('DELETE FROM conversations')
    cursor.execute('DELETE FROM messages')
    cursor.execute('DELETE FROM blog_likes')
    cursor.execute('DELETE FROM user_skills')
    cursor.execute('DELETE FROM user_achievements')
    cursor.execute('DELETE FROM user_languages')
    cursor.execute('DELETE FROM mentorship_requests')
    cursor.execute('DELETE FROM blog_posts')
    cursor.execute('DELETE FROM projects')
    cursor.execute('DELETE FROM users')
    
    # ----------------- Users with Complete Profiles -----------------
    users = [
        # Alumni with complete profiles
        {
            'name': 'Dr. Rajesh Kumar',
            'email': 'rajesh.kumar@iitkgp.ac.in',
            'password': 'password123',
            'role': 'alumni',
            'graduation_year': 2010,
            'department': 'Computer Science and Engineering',
            'hall': 'Nehru Hall',
            'branch': 'B.Tech CSE',
            'bio': 'Healthcare AI entrepreneur and researcher with 13+ years of experience. Founded MediAI Solutions, a $50M healthcare diagnostics startup. Passionate about using ML to solve real-world healthcare problems.',
            'current_company': 'MediAI Solutions',
            'current_position': 'Founder & CEO',
            'location': 'Bangalore, Karnataka',
            'work_preference': 'hybrid',
            'phone': '+91-9876543210',
            'website': 'https://mediaisolutions.com',
            'linkedin': 'https://linkedin.com/in/rajeshkumar',
            'github': 'https://github.com/rajeshkumar',
            'avatar': 'https://randomuser.me/api/portraits/men/1.jpg',
            'years_of_experience': 13,
            'domain': 'Healthcare AI, Machine Learning',
            'tech_skills': json.dumps(['Python', 'TensorFlow', 'PyTorch', 'Computer Vision', 'AWS', 'Docker']),
            'program': 'B.Tech',
            'joining_year': 2006,
            'institute': 'IIT Kharagpur',
            'specialization': 'Artificial Intelligence and Machine Learning'
        },
        {
            'name': 'Priya Sharma',
            'email': 'priya.sharma@iitkgp.ac.in',
            'password': 'password123',
            'role': 'alumni',
            'graduation_year': 2012,
            'department': 'Electrical Engineering',
            'hall': 'Sarojini Naidu Hall',
            'branch': 'B.Tech EE',
            'bio': 'Clean energy advocate and IoT specialist. Leading sustainable energy projects across India. Former Tesla engineer, now building smart grid solutions for rural electrification.',
            'current_company': 'GreenGrid Technologies',
            'current_position': 'VP Engineering',
            'location': 'Pune, Maharashtra',
            'work_preference': 'remote',
            'phone': '+91-9876543211',
            'website': 'https://greengridtech.com',
            'linkedin': 'https://linkedin.com/in/priyasharma',
            'github': 'https://github.com/priyasharma',
            'avatar': 'https://randomuser.me/api/portraits/women/2.jpg',
            'years_of_experience': 11,
            'domain': 'IoT, Renewable Energy, Smart Grid',
            'tech_skills': json.dumps(['IoT', 'Embedded Systems', 'Python', 'MQTT', 'Node.js', 'React']),
            'program': 'B.Tech',
            'joining_year': 2008,
            'institute': 'IIT Kharagpur',
            'specialization': 'Power Electronics and Drives'
        },
        {
            'name': 'Amit Singh',
            'email': 'amit.singh@iitkgp.ac.in',
            'password': 'password123',
            'role': 'alumni',
            'graduation_year': 2015,
            'department': 'Mechanical Engineering',
            'hall': 'Patel Hall',
            'branch': 'B.Tech ME',
            'bio': 'Robotics engineer and entrepreneur. Built EdTech platform serving 2M+ students. Currently working on autonomous manufacturing systems. IIT KGP robotics team captain.',
            'current_company': 'RoboLearn Inc',
            'current_position': 'CTO',
            'location': 'Hyderabad, Telangana',
            'work_preference': 'onsite',
            'phone': '+91-9876543212',
            'website': 'https://robolearn.io',
            'linkedin': 'https://linkedin.com/in/amitsingh',
            'github': 'https://github.com/amitsingh',
            'avatar': 'https://randomuser.me/api/portraits/men/3.jpg',
            'years_of_experience': 8,
            'domain': 'Robotics, Automation, EdTech',
            'tech_skills': json.dumps(['ROS', 'Python', 'C++', 'Computer Vision', 'React', 'Node.js']),
            'program': 'B.Tech',
            'joining_year': 2011,
            'institute': 'IIT Kharagpur',
            'specialization': 'Manufacturing and Automation'
        },
        {
            'name': 'Ananya Iyer',
            'email': 'ananya.iyer@iitkgp.ac.in',
            'password': 'password123',
            'role': 'alumni',
            'graduation_year': 2013,
            'department': 'Biotechnology',
            'hall': 'Indira Gandhi Hall',
            'branch': 'B.Tech BT',
            'bio': 'AgriTech innovator combining biotechnology with IoT. Working on precision agriculture solutions. Published researcher with 15+ papers in plant genomics and smart farming.',
            'current_company': 'FarmTech Innovations',
            'current_position': 'Chief Science Officer',
            'location': 'Pune, Maharashtra',
            'work_preference': 'hybrid',
            'phone': '+91-9876543213',
            'website': 'https://farmtechinnovations.com',
            'linkedin': 'https://linkedin.com/in/ananyaiyer',
            'github': 'https://github.com/ananyaiyer',
            'avatar': 'https://randomuser.me/api/portraits/women/4.jpg',
            'years_of_experience': 10,
            'domain': 'AgriTech, Biotechnology, IoT',
            'tech_skills': json.dumps(['Python', 'R', 'IoT', 'Data Science', 'Bioinformatics']),
            'program': 'B.Tech',
            'joining_year': 2009,
            'institute': 'IIT Kharagpur',
            'specialization': 'Agricultural Biotechnology'
        },
        {
            'name': 'Vikram Patel',
            'email': 'vikram.patel@iitkgp.ac.in',
            'password': 'password123',
            'role': 'alumni',
            'graduation_year': 2014,
            'department': 'Civil Engineering',
            'hall': 'Azad Hall',
            'branch': 'B.Tech CE',
            'bio': 'Urban planning expert and smart city consultant. Led infrastructure projects worth $500M+. Passionate about sustainable urban development and green buildings.',
            'current_company': 'SmartCity Consulting',
            'current_position': 'Senior Partner',
            'location': 'Delhi, NCR',
            'work_preference': 'onsite',
            'phone': '+91-9876543214',
            'website': 'https://smartcityconsulting.in',
            'linkedin': 'https://linkedin.com/in/vikrampatel',
            'github': 'https://github.com/vikrampatel',
            'avatar': 'https://randomuser.me/api/portraits/men/5.jpg',
            'years_of_experience': 9,
            'domain': 'Urban Planning, GIS, Infrastructure',
            'tech_skills': json.dumps(['GIS', 'AutoCAD', 'Python', 'ArcGIS', 'BIM', '3D Modeling']),
            'program': 'B.Tech',
            'joining_year': 2010,
            'institute': 'IIT Kharagpur',
            'specialization': 'Structural Engineering'
        },
        {
            'name': 'Meera Krishnan',
            'email': 'meera.krishnan@iitkgp.ac.in',
            'password': 'password123',
            'role': 'alumni',
            'graduation_year': 2011,
            'department': 'Chemical Engineering',
            'hall': 'Sarojini Naidu Hall',
            'branch': 'B.Tech ChE',
            'bio': 'Green chemistry advocate and process optimization expert. Leading sustainability initiatives in manufacturing. Former Shell engineer, now consulting for Fortune 500 companies.',
            'current_company': 'ChemOptima Solutions',
            'current_position': 'Director of Sustainability',
            'location': 'Chennai, Tamil Nadu',
            'work_preference': 'hybrid',
            'phone': '+91-9876543215',
            'website': 'https://chemoptima.com',
            'linkedin': 'https://linkedin.com/in/meerakrishnan',
            'github': 'https://github.com/meerakrishnan',
            'avatar': 'https://randomuser.me/api/portraits/women/6.jpg',
            'years_of_experience': 12,
            'domain': 'Chemical Engineering, Sustainability, Process Optimization',
            'tech_skills': json.dumps(['ASPEN', 'MATLAB', 'Python', 'Process Simulation', 'Machine Learning']),
            'program': 'B.Tech',
            'joining_year': 2007,
            'institute': 'IIT Kharagpur',
            'specialization': 'Process Systems Engineering'
        },
        
        # Students with complete profiles
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
            'bio': 'Mechanical engineering student passionate about robotics and automation. Building autonomous robots. Captain of IIT KGP Robotics Team. Interested in manufacturing automation.',
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
        },
        {
            'name': 'Rohan Desai',
            'email': 'rohan.desai@iitkgp.ac.in',
            'password': 'password123',
            'role': 'student',
            'graduation_year': None,
            'department': 'Civil Engineering',
            'hall': 'Azad Hall',
            'branch': 'B.Tech CE',
            'bio': 'Civil engineering student interested in smart cities and sustainable infrastructure. Learning GIS and urban planning. Active member of Civil Engineering Society.',
            'current_company': None,
            'current_position': 'Student',
            'location': 'Kharagpur, West Bengal',
            'work_preference': 'onsite',
            'phone': '+91-9876543221',
            'website': None,
            'linkedin': 'https://linkedin.com/in/rohandesai',
            'github': 'https://github.com/rohandesai',
            'avatar': 'https://randomuser.me/api/portraits/men/12.jpg',
            'program': 'B.Tech',
            'joining_year': 2022,
            'institute': 'IIT Kharagpur',
            'specialization': 'Infrastructure Engineering',
            'past_projects': json.dumps([
                {'title': 'Traffic Flow Simulation', 'description': 'Simulating urban traffic patterns', 'tech': ['Python', 'SUMO', 'GIS']},
                {'title': 'Bridge Design Tool', 'description': 'Structural analysis tool for bridge design', 'tech': ['AutoCAD', 'STAAD Pro']}
            ])
        }
    ]
    
    user_ids = {}
    for user in users:
        password_hash = generate_password_hash(user['password'])
        cursor.execute('''
            INSERT INTO users (name, email, password_hash, role, graduation_year, department, hall, branch, bio,
                               current_company, current_position, location, work_preference, phone, website,
                               linkedin, github, avatar, years_of_experience, domain, tech_skills, program,
                               joining_year, institute, specialization, past_projects, is_available)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user['name'], user['email'], password_hash, user['role'], user['graduation_year'], 
              user['department'], user.get('hall'), user.get('branch'), user.get('bio'),
              user.get('current_company'), user.get('current_position'), user.get('location'),
              user.get('work_preference'), user.get('phone'), user.get('website'),
              user.get('linkedin'), user.get('github'), user.get('avatar'),
              user.get('years_of_experience'), user.get('domain'), user.get('tech_skills'),
              user.get('program'), user.get('joining_year'), user.get('institute'),
              user.get('specialization'), user.get('past_projects'), 
              1 if user['role'] == 'alumni' else None))
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
                cursor.execute('''
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
                cursor.execute('''
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
                cursor.execute('''
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
            'images': json.dumps(placeholder_imgs[:3]),
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
            'images': json.dumps(placeholder_imgs[1:4]),
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
            'images': json.dumps(placeholder_imgs[:2]),
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
            'images': json.dumps(placeholder_imgs[::2]),
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
            'images': json.dumps(placeholder_imgs[:3]),
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
            'images': json.dumps(placeholder_imgs[1:4]),
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
        cursor.execute('''
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
        cursor.execute('''
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
        cursor.execute('''
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
        
        {'student_id': user_ids['neha.gupta@iitkgp.ac.in'], 'alumni_id': user_ids['ananya.iyer@iitkgp.ac.in'], 
         'message': 'Hi Ananya, I am a biotechnology student interested in AgriTech. Your work combining biotech with IoT is fascinating. I am researching plant disease detection and would love to learn from your experience at FarmTech Innovations. How can I transition from research to building real-world solutions?', 
         'status': 'accepted'},
        
        {'student_id': user_ids['arjun.mehta@iitkgp.ac.in'], 'alumni_id': user_ids['amit.singh@iitkgp.ac.in'], 
         'message': 'Hello Amit, I am interested in robotics and automation, especially in manufacturing. As the captain of KGP Robotics Team, I am looking to understand career paths in this field. Your journey from student to CTO is inspiring. Could you mentor me on building autonomous systems and the entrepreneurship journey?', 
         'status': 'pending'},
        
        {'student_id': user_ids['divya.nair@iitkgp.ac.in'], 'alumni_id': user_ids['meera.krishnan@iitkgp.ac.in'], 
         'message': 'Hi Meera, I am a chemical engineering student passionate about sustainable manufacturing and green chemistry. Your work at ChemOptima Solutions perfectly aligns with my interests. I am researching process optimization and would appreciate your guidance on combining AI with chemical engineering.', 
         'status': 'pending'},
        
        {'student_id': user_ids['rohan.desai@iitkgp.ac.in'], 'alumni_id': user_ids['vikram.patel@iitkgp.ac.in'], 
         'message': 'Hello Vikram, I am interested in urban planning and smart cities. Your work on infrastructure projects is amazing. I am learning GIS and would love to understand how to transition from academia to real-world urban planning. Could you share insights on working with government and building smart city solutions?', 
         'status': 'accepted'},
        
        {'student_id': user_ids['sneha.reddy@iitkgp.ac.in'], 'alumni_id': user_ids['amit.singh@iitkgp.ac.in'], 
         'message': 'Hi Amit, I am considering entrepreneurship after graduation. Your blog post about lessons from your first year was eye-opening. I have an EdTech idea and would love your advice on getting started, fundraising, and avoiding common pitfalls.', 
         'status': 'accepted'},
    ]
    
    for req in mentorship_requests:
        cursor.execute('''
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
         'student_id': user_ids['rohan.desai@iitkgp.ac.in'],
         'message': 'I am a civil engineering student with experience in GIS and AutoCAD from my coursework. I have worked on urban traffic flow simulation using SUMO and GIS tools. I am passionate about smart cities and sustainable urban development. India\'s urbanization presents unique challenges and I want to be part of building cities that are livable, sustainable, and inclusive.',
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
        cursor.execute('''
            INSERT INTO project_applications (project_id, position_id, student_id, message, status, has_team)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (app['project_id'], app['position_id'], app['student_id'], app['message'], app['status'], app.get('has_team', False)))

    # ----------------- Conversations & Messages -----------------
    conversation_pairs = [
        ('sneha.reddy@iitkgp.ac.in', 'rajesh.kumar@iitkgp.ac.in'),
        ('karan.malhotra@iitkgp.ac.in', 'priya.sharma@iitkgp.ac.in'),
        ('neha.gupta@iitkgp.ac.in', 'ananya.iyer@iitkgp.ac.in'),
        ('rohan.desai@iitkgp.ac.in', 'vikram.patel@iitkgp.ac.in'),
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
        
        cursor.execute('''
            INSERT INTO conversations (user1_id, user2_id)
            VALUES (?, ?)
        ''', (min(user1_id, user2_id), max(user1_id, user2_id)))
        conv_id = cursor.lastrowid
        
        # Add messages
        messages = message_templates[idx % len(message_templates)]
        for i, msg_content in enumerate(messages):
            sender = user1_id if i % 2 == 0 else user2_id
            receiver = user2_id if i % 2 == 0 else user1_id
            cursor.execute('''
                INSERT INTO messages (sender_id, receiver_id, content, is_read)
                VALUES (?, ?, ?, ?)
            ''', (sender, receiver, msg_content, 1 if i < len(messages) - 2 else 0))

    # ----------------- Blog Likes -----------------
    # Students like alumni blog posts
    student_emails = ['sneha.reddy@iitkgp.ac.in', 'karan.malhotra@iitkgp.ac.in', 
                      'neha.gupta@iitkgp.ac.in', 'arjun.mehta@iitkgp.ac.in',
                      'divya.nair@iitkgp.ac.in', 'rohan.desai@iitkgp.ac.in']
    
    for post_title, post_id in blog_post_ids.items():
        # Each post gets likes from 3-5 random students
        num_likes = random.randint(3, 5)
        liking_students = random.sample(student_emails, num_likes)
        for student_email in liking_students:
            cursor.execute('''
                INSERT OR IGNORE INTO blog_likes (blog_post_id, user_id)
                VALUES (?, ?)
            ''', (post_id, user_ids[student_email]))

    conn.commit()
    conn.close()
    print("✅ Database seeded successfully with comprehensive data!")
    print("\n📊 Summary:")
    print(f"   - Users: {len(users)} (6 Alumni, 6 Students)")
    print(f"   - Projects: {len(projects)}")
    print(f"   - Project Positions: {len(project_positions)}")
    print(f"   - Blog Posts: {len(blog_posts)}")
    print(f"   - Mentorship Requests: {len(mentorship_requests)}")
    print(f"   - Project Applications: {len(project_applications)}")
    print(f"   - Conversations: {len(conversation_pairs)}")
    print(f"   - Skills, Achievements, and Languages added for all users")
    print("\n🔐 Login credentials:")
    print("   Alumni: rajesh.kumar@iitkgp.ac.in / password123")
    print("   Student: sneha.reddy@iitkgp.ac.in / password123")

if __name__ == '__main__':
    seed_database()