import sqlite3
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def home():
   #Connect to db
    con = sqlite3.connect("testDB.db")
    con.row_factory = sqlite3.Row

    #SELECT command
    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM users")

    #fetchall
    rows = cur.fetchall()
    con.close()
    #display
    return render_template("list.html",rows=rows)

@app.route("/searchuser")
def searchuser():
  return render_template("search_user.html")

@app.route("/usersearch", methods = ['POST', 'GET'])
def usersearch():
  if request.method == 'POST':
    nm = request.form['name']
    con = sqlite3.connect('testDB.db') #connect to database
    con.row_factory = sqlite3.Row

    #select row
    try:
      cur = con.cursor()
      cur.execute("SELECT rowid, * FROM users WHERE one = ?", (nm,)) #select a specific rowid

      rows = cur.fetchall()

      #go to list page with selection
      con.close()
      return render_template("list.html", rows=rows)
    except:
      return render_template("bad_request.html")

@app.route("/enternew")
def enternew():
  return render_template("new_user.html")

@app.route("/addrec", methods = ['POST', 'GET'])
def addrec():
  if request.method == 'POST':
      #gather information from form
      nm = request.form['name']
      user_id = request.form['id']
      score = request.form['score']

      #insert new entry into user
      with sqlite3.connect('testDB.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO users (one, two, three) VALUES (?,?,?)",(nm, user_id, score))
        con.commit()

      #render and return to list
      con.row_factory = sqlite3.Row
      cur = con.cursor()
      cur.execute("SELECT rowid, * FROM users")
      rows = cur.fetchall()
      con.close()
      return render_template('list.html', rows=rows)

@app.route('/edit', methods=['POST','GET'])
def edit():
  if request.method == 'POST':
      id = request.form['id'] #get the id of selected row
      con = sqlite3.connect('testDB.db') #connect to database
      con.row_factory = sqlite3.Row

      #select row
      cur = con.cursor()
      cur.execute("SELECT rowid, * FROM users WHERE rowid = " + id) #select a specific rowid

      rows = cur.fetchall()

      #go to edit page
      con.close()
      return render_template("edit.html", rows=rows)

@app.route("/editrec", methods=['POST','GET'])
def editrec():
  if request.method == 'POST':
      #gather information from form
      rowid = request.form['rowid']
      nm = request.form['nm']
      user_id = request.form['user_id']
      score = request.form['score']

      #update user
      with sqlite3.connect('testDB.db') as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET one='"+nm+"', two='"+user_id+"', three='"+score+"' WHERE rowid="+rowid)
        con.commit()
    
      #render and return to list
      con.row_factory = sqlite3.Row
      cur = con.cursor()
      cur.execute("SELECT rowid, * FROM users")
      rows = cur.fetchall()
      con.close()
      return render_template('list.html', rows=rows)

@app.route("/delete", methods=['POST','GET'])
def delete():
  if request.method == 'POST':
      rowid = request.form['id'] #get id

      #delete user
      with sqlite3.connect('testDB.db') as con:
        cur = con.cursor()
        cur.execute("DELETE FROM users WHERE rowid="+rowid)
        con.commit()

      #render and return to list
      con.row_factory = sqlite3.Row
      cur = con.cursor()
      cur.execute("SELECT rowid, * FROM users")
      rows = cur.fetchall()
      con.close()
      return render_template('list.html', rows=rows)

if __name__ == "__main__":
  app.run()