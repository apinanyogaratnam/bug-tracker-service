import os

from dotenv import load_dotenv

from views import create_app

load_dotenv()
app = create_app()

debug = os.environ.get('ENVIRONMENT') == 'DEVELOPMENT'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(port), debug=debug)
