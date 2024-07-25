import aioredis
from quart import Quart, request, jsonify, redirect, url_for, render_template_string
from quart_auth import AuthManager, AuthUser, login_user, logout_user, current_user, login_required
from quart_auth import exceptions as auth_exceptions

app = Quart(__name__)
app.secret_key = 'supersecretkey'
AuthManager(app)

# Initialize Redis
redis = None

async def init_redis():
    global redis
    redis = await aioredis.create_redis_pool('redis://localhost')

@app.before_serving
async def startup():
    await init_redis()

@app.after_serving
async def shutdown():
    redis.close()
    await redis.wait_closed()

# Exception handling
@app.errorhandler(auth_exceptions.Unauthorized)
async def handle_unauthorized(e):
    return jsonify({"error": "Unauthorized access"}), 401

@app.errorhandler(auth_exceptions.AuthMissing)
async def handle_auth_missing(e):
    return jsonify({"error": "Authentication required"}), 401

@app.errorhandler(auth_exceptions.AuthFailure)
async def handle_auth_failure(e):
    return jsonify({"error": "Authentication failure"}), 403

@app.errorhandler(404)
async def handle_not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
async def handle_internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

# HTML template for login form
login_form = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <form action="/login" method="post">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username"><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password"><br><br>
        <input type="submit" value="Login">
    </form>
</body>
</html>
"""

@app.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'GET':
        return await render_template_string(login_form)
    elif request.method == 'POST':
        form = await request.form
        username = form.get('username')
        password = form.get('password')
        
        stored_password = await redis.get(username)
        if stored_password and stored_password.decode('utf-8') == password:
            user = AuthUser(username)
            login_user(user)
            return redirect(url_for('private'))
        else:
            return jsonify({"error": "Invalid username or password"}), 401

@app.route('/logout', methods=['POST'])
async def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/private')
@login_required
async def private():
    return jsonify({"message": f"Hello, {current_user.auth_id}. This is a private endpoint."}), 200

if __name__ == '__main__':
    app.run()
