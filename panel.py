import flask
from flask_cors import CORS
import pymysql

host = '81.68.245.129'
user = 'MisakaNetwork'
password = 'MisakaNetwork'
database = 'MisakaNetwork'
charset = 'utf8'
def read(SQL):
    conn = pymysql.connect(host=host, user=user,password=password,database=database,charset=charset)
    cursor = conn.cursor()
    cursor.execute(SQL)
    ret = cursor.fetchall()
    cursor.close()
    conn.close()
    return(ret)
def write(sql):
    conn = pymysql.connect(host=host, user=user,password=password,database=database,charset=charset)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

app = flask.Flask(__name__)

@app.route('/')
def root():
  return '''
  <!DOCTYPE html>
  <html>
    <head>
      <script>
      function httpGet(theUrl)
      {
      var xmlHttp = new XMLHttpRequest();
      xmlHttp.open( "GET", theUrl, false );
      xmlHttp.send( null );
      return xmlHttp.responseText;
      }
      function add_check(evt){
      if (!evt) {evt = window.event;}
      var charCode = (evt.which) ? evt.which : evt.keyCode
      if (!((charCode > 95 && charCode < 106)
      || (charCode > 47 && charCode < 58) 
      || charCode == 8))
        return false;
      return true;
      }
      function add_submit(){
        document.getElementById('err_rm').innerHTML = "<font color=\'orange\'>请稍候</font>";
        var stt = document.getElementById('add').value;
        var ress = (httpGet("https://panel.motszhin.repl.co/exists?qq="+stt));
        console.log(ress);
        if (ress == "nil"){
          console.log('Err1');
          document.getElementById('err_rm').innerHTML = "<font color=\'red\'>无效输入!</font>";
          loop();
          return false;
        }
        else if (ress == "true"){
          console.log('Err2');
          document.getElementById('err_mg').innerHTML = "<font color=\'red\'>已存在!</font>";
          loop();
          return false;
        }
        else{
          console.log('Suc1');
          navigator.sendBeacon("/add?qq="+stt);
          document.getElementById('err_mg').innerHTML = "<font color=\'green\'>成功添加!</font>";
          loop();
          return false;
        }
        return false;
      }
      function rem(){
        if (document.getElementById('adlist').selectedIndex < 0){
          document.getElementById('err_rm').innerHTML = "<font color=\'red\'>无选择!</font>";
          loop();
          return false;
        }
        document.getElementById('err_rm').innerHTML = "<font color=\'orange\'>请稍候</font>";
        var selq = document.getElementById('adlist').value
        if (httpGet("https://panel.motszhin.repl.co/exists?qq="+selq) == "true"){
          navigator.sendBeacon("https://panel.motszhin.repl.co/remove?qq="+selq);
          document.getElementById('err_rm').innerHTML = "<font color=\'green\'>已移除!</font>";
          loop();
          return false;
        }
        else{
          document.getElementById('err_rm').innerHTML = "<font color=\'red\'>用户不存在, 请刷新页面!</font>";
          loop();
          return false;
        }
      }
      </script>
      <title>Control Panel</title>
    </head>
    <body>
    管理员权限名单:<br>
    <div id=adl onload="adl();"></div>
    <script>
    var oldarray;
    var osel;
    if (!osel && osel!=''){
      osel = '';
    }
    if (!oldarray){
      oldarray = [];
    }
    var arraysMatch = function (arr1, arr2) {
	  if (arr1.length !== arr2.length) return false;
	  for (var i = 0; i < arr1.length; i++) {
		if (arr1[i] !== arr2[i]) return false;
	  }
	  return true;
    };
    function sortcp(a,b){
      return parseInt(a)-parseInt(b);
    }
    function loop(){
      var newarray=JSON.parse(httpGet("./list"));
      var sl = httpGet("./sl")
      document.getElementById('adl').innerHTML = sl;
      document.getElementById('adlist').selectedIndex = newarray.indexOf(osel);
    }
    loop();
    </script>
    <p>
    <form action="/add" onsubmit="return add_submit();"><label for="add">加入账号:</label><input name="add" id="add" type="number" min="0" onkeypress="return add_check();"></input><input type="submit">&nbsp;&nbsp;&nbsp;<label id='err_mg'></label></form><br><form onsubmit="return rem();"><input id="remove_button" type="submit" value="移除所选账号"></input>&nbsp;&nbsp;&nbsp;<label id='err_rm'></label></form>
  </html>'''

@app.route('/add', methods=['GET', 'POST'])
def add():
  qq = flask.request.args.get('qq')
  write(f'INSERT INTO Admin VALUE ("{qq}")')
  return ''
@app.route('/exists', methods=['GET', 'POST'])
def exists():
  qq = flask.request.args.get('qq')
  try:
    int(qq)
    if len(read('SELECT * FROM Admin WHERE QQ='+str(qq)))>0:
      return 'true'
    else:
      return 'false'
  except:
    return 'nil'
@app.route('/list', methods=['GET', 'POST'])
def lst():
  res = read('SELECT * FROM Admin')
  retl = []
  for x in res:
    retl.append(x[0])
  return flask.jsonify(retl)
@app.route('/remove', methods=['GET', 'POST'])
def remove():
  qq = flask.request.args.get('qq')
  try:
    int(qq)
    write('DELETE FROM Admin WHERE QQ='+qq)
    return 'true'
  except:
    return 'false'
@app.route('/sl', methods = ['GET', 'POST'])
def sl():
  res = read('SELECT * FROM Admin')
  retl = "<select id=\'adlist\' size=\'15\'>"
  retl+=''.join(["<option value=\'"+x[0]+"\'> "+x[0]+" </option>" for x in res])
  retl += '</select>'
  return retl
hostweb = '127.0.0.1'
port = '80'
app.run(host=hostweb, port=port)
