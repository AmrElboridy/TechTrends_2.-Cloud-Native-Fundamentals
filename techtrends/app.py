import sqlite3
import logging
import sys
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
count = 0

# Function to get a database connection.
def get_db_connection():
    """This function connects to database with the name database.db."""
    global count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    count += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['count'] = 0
# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      return render_template('404.html'), 404
    else:
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            return redirect(url_for('index'))

    return render_template('create.html')

#Define the metrics endpoint
@app.route('/metrics')
def metrics():
    response = app.response_class(
        response=json.dumps({"data": {
                            "db_connection_count": count, "post_count": len(get_db_connection().execute('SELECT * FROM posts').fetchall())}}),
        status=200,
        mimetype='application/json'
    )
    app.logger.info('Metrics successfully requested')
    return response

# Define the health status
@app.route('/healthz')
def status():
    response = app.response_class(
        response = json.dumps({"result":"OK - healthy"}),
        status = 200,
        mimetype = 'application/json'
    )
    app.logger.info('Healthz successfully requested')
    return response

# start the application on port 3111
 # set logger to handle STDOUT and STDERR 

 # format output
 #format_output = # formating output here
if __name__ == "__main__":
   stdout_handler = logging.StreamHandler(stream=sys.stdout)
   stderr_handler = logging.StreamHandler(stream=sys.stderr)
   handlers = [stderr_handler, stdout_handler]
   logging.basicConfig(filename='app.log', level=logging.DEBUG, handlers=handlers)
   app.run(host='0.0.0.0', port='3111')