from dotenv import load_dotenv
import os

load_dotenv()

from flask import Flask
from routes.main_routes import main
from database import init_db

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-secret-key")

init_db()
app.register_blueprint(main)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)