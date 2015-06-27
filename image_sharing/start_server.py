from image_sharing import app

app.secret_key = 'simple_key'
app.run(host='0.0.0.0', port=8000, debug=True)
