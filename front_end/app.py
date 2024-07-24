#app_consumer.py
from flask import render_template, request, session
from init_app import app


#Render the assigned template file
@app.route("/", methods=['GET'])
def index():
    return render_template('consumer.html')


#Run using port 5000
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)