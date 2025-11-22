from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from app.honeypot import honeypot_bp
    from app.dashboard import dashboard_bp
    
    app.register_blueprint(honeypot_bp)
    app.register_blueprint(dashboard_bp)
    
    return app