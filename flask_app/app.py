from website import create_app

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
