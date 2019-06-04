from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
import ibm_db
import base64

app = Flask(__name__)
conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=bvc79655;PWD=cx5cdbtw^x41cjgf;",
                      "", "")

if conn:
    print("Yes")
    quer = "SELECT * FROM BVC79655.TBPEOPLE1 WHERE \"Name\"='Abhishek'"
    
    stmt = ibm_db.prepare(conn,quer)
    #ibm_db.bind_param(stmt, 1, name)
    ibm_db.execute(stmt)
    rows=[]
    # fetch the result
    result = ibm_db.fetch_assoc(stmt)
    while result != False:
        rows.append(result.copy())
        result = ibm_db.fetch_assoc(stmt)
    # close database connection
    ibm_db.close(conn)
    print(rows)

@app.route("/hello")
def hello():
    my_dir = 'orig'
    myTable = "<table border=5><tr><th>FileName</th><th>FileSize(Bytes)</th></tr>"
    for f in os.listdir(my_dir):
        path = os.path.join(my_dir, f)
        if os.path.isfile(path):
            print(f,os.path.getsize(path))
            #myTable = myTable+"<tr><td><a href=\"C:\Study\Spring 2019\Cloud\Webapp with flask\orig\\"+f+"\">"+f+"</a></td><td>"+str(os.path.getsize(path))+"</td></tr>"
            myTable = myTable+"<tr><td><a href=\"./hello/"+f+"\">"+f+"</a></td><td>"+str(os.path.getsize(path))+"</td></tr>"
    print(myTable)
    return "<h1>Ajinkya Vadane,1001657016</h1>"+myTable+"</table>"

@app.route('/')
def myfun():
    return render_template('findmyfile.html')

@app.route('/findMyFile', methods=['POST'])
def findMyFile():
    file_name = request.form['file_name']
    return searchindir(file_name)

def searchindir(fnam):
    my_dir = 'orig'
    myTable = "<table border=5><tr><th>FileName</th><th>FileSize(Bytes)</th></tr>"
    for f in os.listdir(my_dir):
        path = os.path.join(my_dir, f)
        if os.path.isfile(path):
            print(f,os.path.getsize(path))
            #myTable = myTable+"<tr><td><a href=\"C:\Study\Spring 2019\Cloud\Webapp with flask\orig\\"+f+"\">"+f+"</a></td><td>"+str(os.path.getsize(path))+"</td></tr>"
            if f == fnam:
                myTable = myTable+"<tr><td><a href=\"./hello/"+f+"\">"+f+"</a></td><td>"+str(os.path.getsize(path))+"</td></tr>"
    print(myTable)
    return "<h1>Ajinkya Vadane,1001657016</h1>"+myTable+"</table>"

@app.route("/hello/<string:name>/")
def getMember(name):
    print("<img src=\"C:\Study\Spring 2019\Cloud\Webapp with flask\orig\\"+name+"\">")
    print("<img src=\"{{ url_for('static', filename='"+name+"') }}\">")
    #{{ url_for('static', filename='inner_banner5.jpg') }}
    with open('orig/'+name,"rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return "<h1>Ajinkya Vadane,1001657016</h1><img src=\"data:image/jpg;base64," + str(encoded_string,"utf-8") + "\">"

@app.route("/test")
def test():
    return render_template('test.html')

@app.route("/hi")
def hi():
    return "Hi World!"

if __name__ == "__main__":
    app.run()