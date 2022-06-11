import os
import warnings

from dotenv import load_dotenv

from views import create_app

load_dotenv()
warnings.filterwarnings('ignore')
app = create_app()

debug = os.environ.get('ENVIRONMENT') == 'DEVELOPMENT'
port = 8000

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=debug)
