from flask import Blueprint, render_template, request, redirect, url_for, flash
import datetime

from flask_login import login_required

# Define the blueprint
settings_bp = Blueprint('settings', __name__, template_folder='templates')

# Simulated storage (replace with database in production)
user_settings = {
    'profile': {'name': 'John Doe', 'email': 'john.doe@example.com', 'profile_picture': None},
    'notifications': {'email_notifications': True, 'system_alerts': True},
    'theme': {'mode': 'light'},
    'language': {'language': 'English', 'timezone': 'UTC'},
    'privacy': {'public_profile': True},
    'security': {'2fa_enabled': False, 'active_sessions': []},
    'integrations': {'api_keys': []},
}

# Main settings page
@login_required
@settings_bp.route('/settings/')
def index():
    return render_template('settings/index.html', user_settings=user_settings)

# Profile settings
@login_required
@settings_bp.route('/settings/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        # Process profile updates
        user_settings['profile']['name'] = request.form.get('name')
        user_settings['profile']['email'] = request.form.get('email')
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('settings.profile'))
    return render_template('settings/profile.html', profile=user_settings['profile'])

# Notification settings
@login_required
@settings_bp.route('/settings/notifications', methods=['GET', 'POST'])
def notifications():
    if request.method == 'POST':
        # Process notification preferences
        user_settings['notifications']['email_notifications'] = 'email_notifications' in request.form
        user_settings['notifications']['system_alerts'] = 'system_alerts' in request.form
        flash('Notification preferences updated successfully!', 'success')
        return redirect(url_for('settings.notifications'))
    return render_template('settings/notifications.html', notifications=user_settings['notifications'])

# Theme settings
@login_required
@settings_bp.route('/settings/theme', methods=['GET', 'POST'])
def theme():
    if request.method == 'POST':
        # Save theme preference
        user_settings['theme']['mode'] = request.form.get('mode')
        flash('Theme preference updated successfully!', 'success')
        return redirect(url_for('settings.theme'))
    return render_template('settings/theme.html', theme=user_settings['theme'])

# Security settings
@settings_bp.route('/settings/security', methods=['GET', 'POST'])
def security():
    if request.method == 'POST':
        # Enable/disable 2FA
        user_settings['security']['2fa_enabled'] = '2fa_enabled' in request.form
        flash('Security settings updated successfully!', 'success')
        return redirect(url_for('settings.security'))
    return render_template('settings/security.html', security=user_settings['security'])