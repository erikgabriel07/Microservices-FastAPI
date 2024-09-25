from fastapi import FastAPI
from uvicorn import run as startapp


def main():
    app = FastAPI(debug=True) # debug somente em desenvolvimento
    
    startapp(app, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()
