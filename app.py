# app.py - Main Flask Application

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta, date
import os
import sqlite3
from database import init_db, get_db_connection
from tasks import DAILY_TASKS, get_task_for_day

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize database on first run
init_db()

# Helper function to check if user is logged in
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Update streak logic
def update_user_streak(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get user's last completion date
    cursor.execute('''
        SELECT completion_date FROM task_completions 
        WHERE user_id = ? 
        ORDER BY completion_date DESC 
        LIMIT 2
    ''', (user_id,))
    
    completions = cursor.fetchall()
    
    if len(completions) >= 2:
        last_date = datetime.strptime(completions[0]['completion_date'], '%Y-%m-%d').date()
        second_last = datetime.strptime(completions[1]['completion_date'], '%Y-%m-%d').date()
        
        # Check if dates are consecutive
        if (last_date - second_last).days == 1:
            # Increment streak
            cursor.execute('UPDATE users SET streak = streak + 1 WHERE id = ?', (user_id,))
        elif (last_date - second_last).days > 1:
            # Reset streak to 1
            cursor.execute('UPDATE users SET streak = 1 WHERE id = ?', (user_id,))
    else:
        # First or second task, set streak to number of completions
        cursor.execute('UPDATE users SET streak = ? WHERE id = ?', (len(completions), user_id))
    
    conn.commit()
    conn.close()

# Clean expired stories
def clean_expired_stories():
    conn = get_db_connection()
    cursor = conn.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('DELETE FROM stories WHERE expires_at < ?', (current_time,))
    conn.commit()
    conn.close()

# Routes

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        name = request.form.get('name', '').strip()
        
        if not all([username, email, password, name]):
            flash('All fields are required!', 'error')
            return render_template('signup.html')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if username or email exists
        cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email))
        if cursor.fetchone():
            flash('Username or email already exists!', 'error')
            conn.close()
            return render_template('signup.html')
        
        # Create user
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, name) 
            VALUES (?, ?, ?, ?)
        ''', (username, email, password_hash, name))
        conn.commit()
        conn.close()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    clean_expired_stories()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    user_id = session['user_id']
    
    # Get user info
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    
    # Get app start date
    cursor.execute('SELECT start_date FROM app_settings WHERE id = 1')
    start_date_str = cursor.fetchone()['start_date']
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    
    # Get today's task
    today = date.today()
    today_task = get_task_for_day(start_date, today)
    
    # Check if today's task is completed
    today_str = today.strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT * FROM task_completions 
        WHERE user_id = ? AND completion_date = ?
    ''', (user_id, today_str))
    task_completed = cursor.fetchone() is not None
    
    # Get all active stories (user's friends + user's own)
    cursor.execute('''
        SELECT s.*, u.username, u.name, u.profile_photo 
        FROM stories s
        JOIN users u ON s.user_id = u.id
        WHERE s.expires_at > datetime('now')
        AND (s.user_id = ? OR s.user_id IN (
            SELECT friend_id FROM friends WHERE user_id = ?
        ))
        ORDER BY s.created_at DESC
    ''', (user_id, user_id))
    stories = cursor.fetchall()
    
    conn.close()
    
    return render_template('home.html', 
                         user=user, 
                         today_task=today_task, 
                         task_completed=task_completed,
                         stories=stories)

@app.route('/complete_task', methods=['POST'])
@login_required
def complete_task():
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get app start date and today's task
    cursor.execute('SELECT start_date FROM app_settings WHERE id = 1')
    start_date_str = cursor.fetchone()['start_date']
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    
    today = date.today()
    today_str = today.strftime('%Y-%m-%d')
    today_task = get_task_for_day(start_date, today)
    
    # Check if already completed today
    cursor.execute('''
        SELECT * FROM task_completions 
        WHERE user_id = ? AND completion_date = ?
    ''', (user_id, today_str))
    
    if cursor.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': 'Task already completed today!'})
    
    # Mark task as completed
    cursor.execute('''
        INSERT INTO task_completions (user_id, task_description, completion_date)
        VALUES (?, ?, ?)
    ''', (user_id, today_task, today_str))
    
    # Increment tasks completed count
    cursor.execute('UPDATE users SET tasks_completed = tasks_completed + 1 WHERE id = ?', (user_id,))
    
    conn.commit()
    conn.close()
    
    # Update streak
    update_user_streak(user_id)
    
    return jsonify({'success': True, 'message': 'Task completed! 🎉'})

@app.route('/create_story', methods=['POST'])
@login_required
def create_story():
    user_id = session['user_id']
    
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image provided!'})
    
    file = request.files['image']
    text_content = request.form.get('text', '')
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected!'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{user_id}_{timestamp}_{filename}"
        
        # Always use forward slashes for static files
        upload_folder = os.path.join(app.root_path, 'static', 'uploads', 'stories')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        # Save only the filename in DB
        # Calculate expiry time (24 hours from now)
        expires_at = datetime.now() + timedelta(hours=24)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO stories (user_id, image_path, text_content, expires_at)
            VALUES (?, ?, ?, ?)
        ''', (user_id, filename, text_content, expires_at.strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Story posted! 📸'})
    
    return jsonify({'success': False, 'message': 'Invalid file type!'})

@app.route('/get_story/<int:story_id>')
@login_required
def get_story(story_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT s.*, u.username, u.name, u.profile_photo 
        FROM stories s
        JOIN users u ON s.user_id = u.id
        WHERE s.id = ? AND s.expires_at > datetime('now')
    ''', (story_id,))
    story = cursor.fetchone()
    
    if not story:
        conn.close()
        return jsonify({'success': False, 'message': 'Story not found or expired!'})
    
    # Get comments
    cursor.execute('''
        SELECT c.*, u.username, u.profile_photo 
        FROM story_comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.story_id = ?
        ORDER BY c.created_at ASC
    ''', (story_id,))
    comments = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'success': True,
        'story': dict(story),
        'comments': [dict(comment) for comment in comments]
    })

@app.route('/add_comment', methods=['POST'])
@login_required
def add_comment():
    user_id = session['user_id']
    story_id = request.form.get('story_id')
    comment_text = request.form.get('comment', '').strip()
    
    if not comment_text:
        return jsonify({'success': False, 'message': 'Comment cannot be empty!'})
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO story_comments (story_id, user_id, comment_text)
        VALUES (?, ?, ?)
    ''', (story_id, user_id, comment_text))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Comment added!'})

@app.route('/friends')
@login_required
def friends():
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get user info
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    
    # Get friends list with their stats
    cursor.execute('''
        SELECT u.*, 
               (SELECT COUNT(*) FROM task_completions WHERE user_id = u.id) as friend_tasks_completed
        FROM users u
        JOIN friends f ON (f.friend_id = u.id AND f.user_id = ?)
        ORDER BY u.username
    ''', (user_id,))
    friends_list = cursor.fetchall()
    
    # Get pending friend requests received
    cursor.execute('''
        SELECT u.id, u.username, u.name, u.profile_photo 
        FROM users u
        JOIN friend_requests fr ON fr.sender_id = u.id
        WHERE fr.receiver_id = ? AND fr.status = 'pending'
    ''', (user_id,))
    pending_requests = cursor.fetchall()
    
    conn.close()
    
    return render_template('friends.html', 
                         user=user, 
                         friends=friends_list, 
                         pending_requests=pending_requests)

@app.route('/search_user', methods=['POST'])
@login_required
def search_user():
    search_username = request.form.get('username', '').strip()
    user_id = session['user_id']
    
    if not search_username:
        return jsonify({'success': False, 'message': 'Enter a username!'})
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Find user
    cursor.execute('SELECT id, username, name, profile_photo FROM users WHERE username = ?', (search_username,))
    found_user = cursor.fetchone()
    
    if not found_user:
        conn.close()
        return jsonify({'success': False, 'message': 'User not found!'})
    
    if found_user['id'] == user_id:
        conn.close()
        return jsonify({'success': False, 'message': 'Cannot add yourself!'})
    
    # Check if already friends
    cursor.execute('''
        SELECT * FROM friends 
        WHERE user_id = ? AND friend_id = ?
    ''', (user_id, found_user['id']))
    
    if cursor.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': 'Already friends!'})
    
    # Check if request already sent
    cursor.execute('''
        SELECT * FROM friend_requests 
        WHERE sender_id = ? AND receiver_id = ? AND status = 'pending'
    ''', (user_id, found_user['id']))
    
    if cursor.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': 'Request already sent!'})
    
    conn.close()
    
    return jsonify({
        'success': True, 
        'user': dict(found_user)
    })

@app.route('/send_friend_request', methods=['POST'])
@login_required
def send_friend_request():
    user_id = session['user_id']
    friend_id = request.form.get('friend_id')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO friend_requests (sender_id, receiver_id, status)
            VALUES (?, ?, 'pending')
        ''', (user_id, friend_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Friend request sent!'})
    except:
        conn.close()
        return jsonify({'success': False, 'message': 'Failed to send request!'})

@app.route('/accept_request/<int:sender_id>', methods=['POST'])
@login_required
def accept_request(sender_id):
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Update request status
    cursor.execute('''
        UPDATE friend_requests 
        SET status = 'accepted' 
        WHERE sender_id = ? AND receiver_id = ?
    ''', (sender_id, user_id))
    
    # Add to friends (mutual)
    cursor.execute('INSERT INTO friends (user_id, friend_id) VALUES (?, ?)', (user_id, sender_id))
    cursor.execute('INSERT INTO friends (user_id, friend_id) VALUES (?, ?)', (sender_id, user_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Friend request accepted!'})

@app.route('/reject_request/<int:sender_id>', methods=['POST'])
@login_required
def reject_request(sender_id):
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE friend_requests 
        SET status = 'rejected' 
        WHERE sender_id = ? AND receiver_id = ?
    ''', (sender_id, user_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Request rejected!'})

@app.route('/remove_friend/<int:friend_id>', methods=['POST'])
@login_required
def remove_friend(friend_id):
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Remove from both sides
    cursor.execute('DELETE FROM friends WHERE user_id = ? AND friend_id = ?', (user_id, friend_id))
    cursor.execute('DELETE FROM friends WHERE user_id = ? AND friend_id = ?', (friend_id, user_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Friend removed!'})

@app.route('/profile')
@login_required
def profile():
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    
    conn.close()
    
    return render_template('profile.html', user=user)

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    user_id = session['user_id']
    name = request.form.get('name', '').strip()
    bio = request.form.get('bio', '').strip()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE users SET name = ?, bio = ? WHERE id = ?', (name, bio, user_id))
    conn.commit()
    conn.close()
    
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))

@app.route('/upload_profile_photo', methods=['POST'])
@login_required
def upload_profile_photo():
    user_id = session['user_id']
    
    if 'profile_photo' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided!'})
    
    file = request.files['profile_photo']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected!'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"profile_{user_id}_{timestamp}_{filename}"
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'profiles', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET profile_photo = ? WHERE id = ?', (filename, user_id))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Profile photo updated!', 'filename': filename})
    
    return jsonify({'success': False, 'message': 'Invalid file type!'})

if __name__ == '__main__':
    # Create upload directories
    os.makedirs('static/uploads/profiles', exist_ok=True)
    os.makedirs('static/uploads/stories', exist_ok=True)
    
    app.run(debug=True)