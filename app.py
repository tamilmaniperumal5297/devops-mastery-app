import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    env_name = os.getenv('APP_ENV', 'Local')
    db_password = os.getenv('DB_PASSWORD', 'Not-Set')
    return f"<h1>🚀 App Running in {env_name}!</h1><p>DB Password Secret Loaded: {db_password != 'Not-Set'}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)