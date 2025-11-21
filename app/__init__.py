from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from app.honeypot import honeypot_bp
    app.register_blueprint(honeypot_bp)
    
    return app