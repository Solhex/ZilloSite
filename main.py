from website import create_app  # imports create_app from the folder website 

app = create_app()              # initilizes the create_app

if __name__ == '__main__':      # runs the code if this specific file is executed
    app.run(debug=True)         # runs the website in debug mode, DO NOT ENABLE debug mode POST PRODUCTION as it can allow python code execution with the debugger pin