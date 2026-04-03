"""
Sitemap controller for generating XML sitemap for SEO
"""
from flask import Blueprint, Response, current_app
from database import get_db_connection
from datetime import datetime
import sqlite3

sitemap_bp = Blueprint('sitemap', __name__)

def build_sitemap_xml():
    """Build complete sitemap XML for the application"""
    
    # Get database connection
    db_path = None
    try:
        # This will get the db_path, adjust based on your database module
        from database import get_db_path
        db_path = get_db_path()
    except:
        pass
    
    if not db_path:
        return generate_static_sitemap()
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        sitemap_entries = []
        current_date = datetime.now().isoformat()
        base_url = 'https://kgplaunchpad.com'  # Change to your domain
        
        # Add static pages
        static_pages = [
            ('/', 'daily', 1.0),
            ('/about', 'weekly', 0.8),
            ('/team', 'monthly', 0.7),
            ('/privacy-policy', 'yearly', 0.5),
            ('/terms-of-service', 'yearly', 0.5),
            ('/login', 'weekly', 0.6),
            ('/register', 'weekly', 0.6),
            ('/projects', 'daily', 0.9),
            ('/launchpad', 'daily', 0.9),
            ('/launchdeck', 'daily', 0.9),
            ('/blog', 'daily', 0.9),
            ('/courses', 'weekly', 0.8),
            ('/events', 'weekly', 0.8),
            ('/mentors', 'weekly', 0.8),
            ('/alumni-connect', 'weekly', 0.8),
            ('/resources', 'weekly', 0.7),
            ('/admin/login', 'never', 0.3),
        ]
        
        for path, changefreq, priority in static_pages:
            sitemap_entries.append({
                'loc': f'{base_url}{path}',
                'lastmod': current_date,
                'changefreq': changefreq,
                'priority': priority,
            })
        
        # Add dynamic projects
        cursor.execute('''
            SELECT id, updated_at FROM launchpad_projects 
            WHERE is_deleted = 0 ORDER BY updated_at DESC
        ''')
        projects = cursor.fetchall()
        for project in projects:
            sitemap_entries.append({
                'loc': f'{base_url}/projects/{project["id"]}',
                'lastmod': project['updated_at'] or current_date,
                'changefreq': 'weekly',
                'priority': 0.8,
            })
        
        # Add dynamic blog posts
        cursor.execute('''
            SELECT id, updated_at FROM blogs 
            WHERE is_deleted = 0 ORDER BY updated_at DESC
        ''')
        blogs = cursor.fetchall()
        for blog in blogs:
            sitemap_entries.append({
                'loc': f'{base_url}/blog/{blog["id"]}',
                'lastmod': blog['updated_at'] or current_date,
                'changefreq': 'weekly',
                'priority': 0.8,
            })
        
        # Add dynamic courses
        cursor.execute('''
            SELECT id, updated_at FROM courses 
            WHERE is_deleted = 0 ORDER BY updated_at DESC
        ''')
        courses = cursor.fetchall()
        for course in courses:
            sitemap_entries.append({
                'loc': f'{base_url}/courses/{course["id"]}',
                'lastmod': course['updated_at'] or current_date,
                'changefreq': 'weekly',
                'priority': 0.8,
            })
        
        # Add dynamic events
        cursor.execute('''
            SELECT id, updated_at FROM events 
            WHERE is_deleted = 0 ORDER BY updated_at DESC
        ''')
        events = cursor.fetchall()
        for event in events:
            sitemap_entries.append({
                'loc': f'{base_url}/events/{event["id"]}',
                'lastmod': event['updated_at'] or current_date,
                'changefreq': 'weekly',
                'priority': 0.8,
            })
        
        # Add dynamic pitches (LaunchDeck)
        cursor.execute('''
            SELECT id, updated_at FROM launchdeck_pitches 
            WHERE is_deleted = 0 ORDER BY updated_at DESC
        ''')
        pitches = cursor.fetchall()
        for pitch in pitches:
            sitemap_entries.append({
                'loc': f'{base_url}/launchdeck/pitch/{pitch["id"]}',
                'lastmod': pitch['updated_at'] or current_date,
                'changefreq': 'weekly',
                'priority': 0.8,
            })
        
        # Add user profiles (if public)
        cursor.execute('''
            SELECT id, updated_at FROM users 
            WHERE role IN ('alumni', 'mentor') AND is_approved = 1
            ORDER BY updated_at DESC LIMIT 1000
        ''')
        users = cursor.fetchall()
        for user in users:
            sitemap_entries.append({
                'loc': f'{base_url}/profile/{user["id"]}',
                'lastmod': user['updated_at'] or current_date,
                'changefreq': 'monthly',
                'priority': 0.6,
            })
        
        conn.close()
        
        return generate_sitemap_xml(sitemap_entries)
    
    except Exception as e:
        print(f"Error generating dynamic sitemap: {e}")
        return generate_static_sitemap()


def generate_sitemap_xml(entries):
    """Generate XML sitemap from entries"""
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for entry in entries:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{entry["loc"]}</loc>\n'
        xml_content += f'    <lastmod>{entry["lastmod"]}</lastmod>\n'
        xml_content += f'    <changefreq>{entry["changefreq"]}</changefreq>\n'
        xml_content += f'    <priority>{entry["priority"]}</priority>\n'
        xml_content += '  </url>\n'
    
    xml_content += '</urlset>'
    return xml_content


def generate_static_sitemap():
    """Fallback: Generate sitemap with only static pages"""
    base_url = 'https://kgplaunchpad.com'
    current_date = datetime.now().isoformat()
    
    static_pages = [
        ('/', 'daily', 1.0),
        ('/about', 'weekly', 0.8),
        ('/team', 'monthly', 0.7),
        ('/privacy-policy', 'yearly', 0.5),
        ('/terms-of-service', 'yearly', 0.5),
        ('/login', 'weekly', 0.6),
        ('/register', 'weekly', 0.6),
        ('/projects', 'daily', 0.9),
        ('/launchpad', 'daily', 0.9),
        ('/launchdeck', 'daily', 0.9),
        ('/blog', 'daily', 0.9),
        ('/courses', 'weekly', 0.8),
        ('/events', 'weekly', 0.8),
        ('/mentors', 'weekly', 0.8),
        ('/alumni-connect', 'weekly', 0.8),
        ('/resources', 'weekly', 0.7),
    ]
    
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for path, changefreq, priority in static_pages:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{base_url}{path}</loc>\n'
        xml_content += f'    <lastmod>{current_date}</lastmod>\n'
        xml_content += f'    <changefreq>{changefreq}</changefreq>\n'
        xml_content += f'    <priority>{priority}</priority>\n'
        xml_content += '  </url>\n'
    
    xml_content += '</urlset>'
    return xml_content


@sitemap_bp.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generate and return XML sitemap"""
    xml_content = build_sitemap_xml()
    return Response(xml_content, mimetype='application/xml')


@sitemap_bp.route('/robots.txt', methods=['GET'])
def robots():
    """Generate and return robots.txt"""
    robots_content = """# KG Launchpad - Robots.txt

# Allow all crawlers
User-agent: *
Allow: /

# Disallow admin pages and private routes
Disallow: /admin/
Disallow: /dashboard
Disallow: /student-dashboard
Disallow: /founders-dashboard
Disallow: /alumni/
Disallow: /profile (authenticated user profiles)
Disallow: /messages
Disallow: /my-

# Point to sitemap
Sitemap: https://kgplaunchpad.com/sitemap.xml

# Crawl delay for all bots
Crawl-delay: 1

# Allow Google and Bing to crawl everything
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# Block spam bots
User-agent: MJ12bot
Disallow: /

User-agent: AhrefsBot
Disallow: /

User-agent: SemrushBot
Disallow: /
"""
    return Response(robots_content, mimetype='text/plain')
