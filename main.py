from website import create_app
# import webview

app = create_app()
# window = webview.create_window('Open Film', app)

if __name__ == '__main__':
    app.run(debug=True)
    # webview.start()
