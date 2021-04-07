import os

from myapp.api.app import create_app
from myapp.api.anomalies import bp as anomalies_bp
from myapp.api.hello import bp as hello_bp


app = create_app()

app.register_blueprint(anomalies_bp)
app.register_blueprint(hello_bp)


if __name__ == "__main__":
    app.run(port=os.environ.get("PORT", 5000), host='0.0.0.0', debug=False)
