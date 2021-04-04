from myapp.api.app import create_app
from myapp.api.anomalies import bp as anomalies_bp
from myapp.api.hello import bp as hello_bp


if __name__ == "__main__":
    app = create_app()

    app.register_blueprint(anomalies_bp)
    app.register_blueprint(hello_bp)

    app.run()
