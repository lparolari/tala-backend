import os

from myapp.api.app import create_app


if __name__ == '__main__':
    # For development purposes only
    app = create_app()
    app.run(port=os.environ.get('PORT', 5000),
            host=os.environ.get('HOST', '0.0.0.0'), debug=False)
