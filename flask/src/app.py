from src.api.analytics_api import bp as analytics_bp

from flask import Flask

app = Flask(__name__)

app.register_blueprint(analytics_bp)

if __name__ == "__main__":
    app.run()
