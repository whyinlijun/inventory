from inventory import app

@app.route('/')
def index():
    return "The word is OK,OKOK"