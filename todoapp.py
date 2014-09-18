from datetime import datetime
import happybase
import json
import time
import calendar
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort

app = Flask(__name__)
app.config.from_pyfile('todoapp.cfg')
time_format = "%Y-%m-%d %H:%M:%S"
time_format_w_ms = "%Y-%m-%d %H:%M:%S.%f"

connection = happybase.Connection(app.config['HBASE_HOST'], app.config['HBASE_PORT'])
column_and_key = app.config['HBASE_TABLE']+":"+app.config['HBASE_TABLE']

@app.route('/')
def index():
    return render_template('index.html', todos=getTasks())

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['title']:
            flash('you must provide a basic description', 'error')
        elif not request.form['text']:
            flash('additional notes are required', 'error')
        else:
            saveTask({"title": request.form['title'], "text":request.form['text'], "pub_date": str(datetime.now()), "done": "False" })
            flash(u'Todo item was successfully created')
            return redirect(url_for('index'))
    return render_template('new.html')

@app.route('/todos/<int:id>', methods = ['GET' , 'POST'])
def show_or_update(id):
    item = getTask(id)
    if request.method == 'GET':
        return render_template('view.html',todo=item)
    item['title'] = request.form['title'] 
    item['pub_date'] = item['pub_date'].strftime(time_format_w_ms)
    item['text']  = request.form['text']
    item['done']  = str(('done.%d' % id) in request.form)
    if request.method == 'POST':
        saveTask(item)
    return redirect(url_for('index'))

def getTasks():
    hbase = connection.table(app.config['HBASE_TABLE'])
    print "get all"
    results = []
    for key, data in hbase.scan():
        print key, data
        results.append(_decode(data))
    return results

def getTask(id):
    print "get "+str(id)
    #timestmp = _unix_to_datetime(id)
    hbase = connection.table(app.config['HBASE_TABLE'])
    #return _decode(hbase.row(timestmp))
    return _decode(hbase.row(str(id)))
    
def saveTask(task):
    item = _encode(task)
    pub_date = datetime.strptime(task['pub_date'], time_format)
    id = str(_datetime_to_unix(pub_date))
    hbase = connection.table(app.config['HBASE_TABLE'])
    hbase.put(id, {column_and_key: str(item)})

def delTask(id):
    hbase = connection.table(app.config['HBASE_TABLE'])
    table.delete(str(id))
    print "deleting: "+str(id)

def resetTable():
    dropTable()
    createTable()

def dropTable():
    print "dropping our table..."
    if( app.config['HBASE_TABLE'] in connection.tables()):
        connection.delete_table( app.config['HBASE_TABLE'], True)

def createTable():
    a = {app.config['HBASE_TABLE']: dict()}
    print a
    if( app.config['HBASE_TABLE'] not in connection.tables()):
        print "creating a table schema..."
        connection.create_table( app.config['HBASE_TABLE'], a)

def _encode(item):
    pub_date = datetime.strptime(item['pub_date'], time_format_w_ms)
    item['pub_date'] = pub_date.strftime(time_format)
    item['done'] = str(item['done'])
    return json.dumps(item)

def _decode(item):
    task = json.loads(item[column_and_key])
    pub_date = datetime.strptime(task['pub_date'], time_format)
    done = True if task['done'] == 'True' else False
    id = _datetime_to_unix(pub_date)
    return {"title": str(task['title']), "text": str(task['text']), "pub_date": pub_date, "done": done, "id": id }

def _unix_to_datetime(id):
    return datetime.fromtimestamp(int(id)+25200).strftime(time_format)

def _datetime_to_unix(date):
    return calendar.timegm(date.timetuple())


if __name__ == '__main__':
    print connection.tables()
    #createTable()
    resetTable()
    app.run()
