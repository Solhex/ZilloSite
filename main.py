from website import create_app  # imports create_app from the folder website 

app = create_app()              # initilizes the create_app

if __name__ == '__main__':      # runs the code if this specific file is executed
    app.run(debug=True)         # runs the website in debug mode, Note: remove debug mode or set it to False when running the site online