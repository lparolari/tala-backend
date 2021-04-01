from myapp.api.app import create_app
from myapp.api.anomalies import bp as anomalies_bp


if __name__ == "__main__":
    app = create_app()

    app.register_blueprint(anomalies_bp)

    app.run()
