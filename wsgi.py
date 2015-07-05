from pyhaukka.app import app

# Run a test server if called as main
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
