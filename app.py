from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Dummy in-memory users for demonstration (replace with actual user management logic)
users = {'testuser': 'testpassword'}  # Replace with actual user management (e.g., database)

# LinkedIn OAuth Credentials
CLIENT_ID = '86sj54i09odtrh'
CLIENT_SECRET = 'WPL_AP1.HOjCrpkLrg9FRGli.f8dw+g==' 
REDIRECT_URI = 'http://localhost:5000/linkedin/callback'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
SCOPE = 'r_liteprofile r_emailaddress'


# Home route (login page)
@app.route('/')
def home():
    return render_template('index.html') 

# Handle login form submission
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Simple login check (replace with actual authentication logic)
    if username in users and users[username] == password:
        return "Logged in successfully!"  # Redirect to a dashboard or homepage here
    else:
        return "Invalid credentials, please try again."


# LinkedIn OAuth login
@app.route('/login/linkedin')
def login_linkedin():
    linkedin_auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}&scope={SCOPE}"
    )
    return redirect(linkedin_auth_url)


# Callback route for LinkedIn OAuth
@app.route('/callback')
def callback():
    code = request.args.get('code')

    # Exchange the authorization code for an access token
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=token_data)
    response_json = response.json()

    access_token = response_json.get('access_token')
    if access_token:
        # Use the access token to fetch user profile data
        user_profile = fetch_linkedin_profile(access_token)
        return f'User Profile: {user_profile}'
    else:
        return 'Error: Unable to get access token'


def fetch_linkedin_profile(access_token):
    profile_url = 'https://api.linkedin.com/v2/me'
    headers = {'Authorization': f'Bearer {access_token}'}
    profile_response = requests.get(profile_url, headers=headers)
    return profile_response.json()


@app.route('/login/unt-email')
def login_unt_email():
    # Add UNT email authentication logic here (e.g., OAuth for UNT emails)
    return "Redirecting to UNT email login..."  # Replace with actual UNT email login logic


# New user registration page
@app.route('/register')
def register():
    # Render a registration page or implement the registration logic here
    return "New user registration page"  # Replace with actual registration logic


if __name__ == '__main__':
    app.run(debug=True)
