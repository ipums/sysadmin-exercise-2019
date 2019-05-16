from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config.from_object('config')
mysql.init_app(app)

@app.route("/")
def home():
    return "<a href='/count'>Case Count</a><br><a href='/ids'>First 50 Unique IDs</a>"

@app.route("/count")
def count():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM persons")
    count = cur.fetchone()[0]
    return str(count) + " records."

@app.route("/ids")
def ids():
    cur = mysql.connection.cursor()
    cur.execute("SELECT unique_id FROM persons LIMIT 50")
    ids = cur.fetchall()
    return "<br/>".join('%s' % (id) for (id) in ids)

if __name__ == "__main__":
    app.run(debug=True)
