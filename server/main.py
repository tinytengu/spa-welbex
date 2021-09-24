from dotenv import load_dotenv

from app import init_app

if __name__ == '__main__':
    load_dotenv()
    app = init_app()
    app.run(host='127.0.0.1', port=5000, debug=True)
