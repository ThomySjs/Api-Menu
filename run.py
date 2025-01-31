from myapp import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='192.168.0.11', port=5000)


