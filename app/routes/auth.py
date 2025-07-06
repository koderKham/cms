from flask import Blueprint, request, jsonify, current_app, session, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import uuid

from app import db
from app.models.user import User
from config import Config

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login via form or API"""
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    # Handle API request (JSON)
    if request.is_json:
        data = request.get_json()

        # Find user by email
        user = User.query.filter_by(email=data.get('email')).first()

        # Check user and password
        if not user or not user.check_password(data.get('password')):
            return jsonify({'error': 'Invalid email or password'}), 401

        # Log in user (for session-based auth)
        login_user(user, remember=data.get('rememberMe', False))

        # Update last login time
        user.last_login = datetime.utcnow()
        db.session.commit()

        # Generate JWT token with expiry time
        token_expiry = datetime.utcnow() + timedelta(days=30)
        token = jwt.encode({
            'user_id': user.id,
            'exp': token_expiry,
            'jti': str(uuid.uuid4())  # Add unique token ID to prevent replay attacks
        }, Config.SECRET_KEY, algorithm='HS256')

        # Log successful login
        current_app.logger.info(f"User {user.email} logged in at {datetime.utcnow()}")

        return jsonify({
            'token': token,
            'user': user.to_dict(),
            'expires': token_expiry.isoformat(),
            'redirect': url_for('main.dashboard')
        }), 200

    # Handle form submission or render login page
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = 'rememberMe' in request.form

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return render_template('login.html', error='Invalid email or password', now=datetime.utcnow())

        login_user(user, remember=remember)

        # Update last login time
        user.last_login = datetime.utcnow()
        db.session.commit()

        return redirect(url_for('main.dashboard'))

    # GET request - show login form
    return render_template('login.html', now=datetime.utcnow())


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration via form or API"""
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    # Handle API request (JSON)
    if request.is_json:
        data = request.get_json()

        # Validate required fields
        required_fields = ['email', 'password', 'name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400

        # Validate password
        if len(data['password']) < 8:
            return jsonify({'error': 'Password must be at least 8 characters long'}), 400

        # Create new user
        try:
            user = User(
                name=data['name'],
                email=data['email'],
                role=data.get('role', 'attorney')
            )
            user.set_password(data['password'])

            db.session.add(user)
            db.session.commit()

            # Log in the new user
            login_user(user)

            # Set last login time for new user
            user.last_login = datetime.utcnow()
            db.session.commit()

            # Generate JWT token
            token_expiry = datetime.utcnow() + timedelta(days=30)
            token = jwt.encode({
                'user_id': user.id,
                'exp': token_expiry,
                'jti': str(uuid.uuid4())
            }, Config.SECRET_KEY, algorithm='HS256')

            # Log successful registration
            current_app.logger.info(f"New user registered: {user.email} at {datetime.utcnow()}")

            return jsonify({
                'token': token,
                'user': user.to_dict(),
                'expires': token_expiry.isoformat(),
                'redirect': url_for('main.dashboard')
            }), 201

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Registration error: {str(e)}")
            return jsonify({'error': 'Registration failed. Please try again.'}), 500

    # Handle form submission
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        role = request.form.get('role', 'attorney')

        # Validate input
        if not all([name, email, password, confirm_password]):
            return render_template('login.html', reg_error='All fields are required', active_tab='register',
                                   now=datetime.utcnow())

        if password != confirm_password:
            return render_template('login.html', reg_error='Passwords do not match', active_tab='register',
                                   now=datetime.utcnow())

        if User.query.filter_by(email=email).first():
            return render_template('login.html', reg_error='Email already registered', active_tab='register',
                                   now=datetime.utcnow())

        # Validate password length
        if len(password) < 8:
            return render_template('login.html', reg_error='Password must be at least 8 characters long',
                                   active_tab='register', now=datetime.utcnow())

        # Create user
        try:
            user = User(name=name, email=email, role=role)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            # Log in the user
            login_user(user)

            # Set initial login time
            user.last_login = datetime.utcnow()
            db.session.commit()

            # Log the registration
            current_app.logger.info(f"User {email} registered successfully at {datetime.utcnow()}")
            flash(f'Welcome, {name}! Your account has been created.', 'success')

            return redirect(url_for('main.dashboard'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Registration error: {str(e)}")
            return render_template('login.html', reg_error='Registration failed. Please try again.',
                                   active_tab='register', now=datetime.utcnow())

    # GET request - show registration form (redirect to login page with register tab active)
    return render_template('login.html', active_tab='register', now=datetime.utcnow())


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'message': 'Logged out successfully'}), 200
    return redirect(url_for('auth.login'))


@auth.route('/profile', methods=['GET'])
@login_required
def profile():
    """Get current user profile"""
    return jsonify(current_user.to_dict())


@auth.route('/check-auth', methods=['GET'])
def check_auth():
    """Check if the current user is authenticated"""
    if current_user.is_authenticated:
        return jsonify({'authenticated': True, 'user': current_user.to_dict()}), 200
    return jsonify({'authenticated': False}), 401


# Token validation middleware that can be used in other routes
def token_required(f):
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Look for token in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])

            if not current_user:
                return jsonify({'error': 'User not found'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(current_user, *args, **kwargs)

    return decorated