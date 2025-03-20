from flask import Flask, render_template, Response, request


app = Flask(__name__)
app.url = '../sample/video/road.hevc'

@app.route('/', methods=['GET'])
def index():
    """Video streaming home page."""
    if request.args.get("url") is not None:
        app.url = request.args.get("url")

    return render_template('index.html')

@app.route('/base', methods=['GET'])
def base():
    """Video streaming home page."""
    if request.args.get("url") is not None:
        app.url = request.args.get("url")

    return render_template('base.html')

@app.route('/hls', methods=['GET'])
def hls():
    """Video streaming home page."""
    if request.args.get("url") is not None:
        app.url = request.args.get("url")

    return render_template('hls.html')


if __name__ == '__main__':
    app.run(debug=True)