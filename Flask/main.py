from routes.routes import app


def main():
    app.run(host='0.0.0.0', port=5000, debug=True) # Debug somente em desenvolvimento


if __name__ == '__main__':
    main()