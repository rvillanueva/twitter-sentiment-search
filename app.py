from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/posts', methods=['get'])
def getPosts():
    res = {}
    res['posts'] = []
    return jsonify(res)


if __name__ == '__main__':
    app.run()
