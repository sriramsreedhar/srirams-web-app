from flask import Flask, render_template, request, Response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    content = request.form['content']
    filename = "note.txt"
    with open(filename, 'w') as f:
        f.write(content)
    return Response(
        content,
        mimetype="text/plain",
        headers={"Content-disposition":
                 "attachment; filename=" + filename})

if __name__ == '__main__':
    app.run(debug=True)
