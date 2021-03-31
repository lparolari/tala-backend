from .api.app import create_app
from .api.anomalies import bp as anomalies_bp


app = create_app()


app.register_blueprint(anomalies_bp)
