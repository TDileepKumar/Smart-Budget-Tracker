from flask import Flask
from routes.main_routes import main
from database import init_db
from dotenv import load_dotenv
import os
os.environ["OPENAI_API_KEY"] = "your_api_key_here"

load_dotenv()

app = Flask(__name__)
app.secret_key = "super_secret_key"

init_db()
app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)