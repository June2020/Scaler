import os
from flask import Flask
from routes.audio import audio_bp

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024
    app.register_blueprint(audio_bp, url_prefix="/api/audio")

    @app.errorhandler(413)
    def too_large(e):
        return {"error": "File too large (max 50MB)"}, 413

    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Endpoint not found"}, 404

    @app.errorhandler(500)
    def server_error(e):
        app.logger.exception(e)
        return {"error": "Internal server error"}, 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true", port=5000)
