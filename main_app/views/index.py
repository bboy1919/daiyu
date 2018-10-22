import os
import uuid
import datetime
import zipfile

from flask import Blueprint, render_template, request, redirect, session

from ..utils import sql_exe

ind = Blueprint('首页', __name__, template_folder='templates')


@ind.before_request
def process_request():
    if not session.get("user_info"):
        return redirect("/login")
    return None


@ind.route('/index')
def index():
    print(session["user_info"]["id"])
    data_list = sql_exe.fetch_all("select id,user,nickname from userinfo", [])

    data_uu = sql_exe.fetch_all(
        "SELECT Sum(record.line) as codesum,userinfo.nickname FROM record "
        "INNER JOIN userinfo WHERE record.user_id = userinfo.id GROUP BY record.user_id", [])
    y = []
    x = []
    for item in data_uu:
        y.append(int(item['codesum']))
        x.append(item['nickname'])

    return render_template('index.html', data_list=data_list, x=x, y=y)


@ind.route('/detail/<int:nid>')
def detail(nid):
    record_list = sql_exe.fetch_all("SELECT id,line,ctime FROM record where user_id=%s", (nid,))

    return render_template('detail.html', record_list=record_list)


@ind.route('/upfile', methods=['GET', 'POST'])
def upload():

    if request.method == "GET":
        return render_template('upcode.html')

    file_obj = request.files.get('codefile')
    # print(file_obj.filename)
    ctime = datetime.date.today()
    data = sql_exe.fetch_one("select id from record where ctime=%s and user_id=%s", (ctime, session['user_info']['id']))
    #
    if data:
        err_msg =  "今天已经上传"
        return render_template('upcode.html', err_msg=err_msg)

    zip_file = zipfile.ZipFile(file_obj.stream)
    target_path = os.path.join('files', str(uuid.uuid4()))

    zip_file.extractall(path=target_path)

    total_num = 0
    for base_path, folder_list, file_list in os.walk(target_path):
        for file_name in file_list:
            file_path = os.path.join(base_path, file_name)
            file_ext = file_path.rsplit('.', maxsplit=1)
            if len(file_ext) != 2:
                continue
            if file_ext[1] != 'py':
                continue
            file_num = 0
            with open(file_path, 'rb') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith(b'#'):
                        continue
                    file_num += 1
            total_num += file_num

    sql_exe.insert("insert into record(line,ctime,user_id) values(%s,%s,%s)", (total_num, ctime, session['user_info']['id']))
    err_msg = "上传成功"
    return render_template('upcode.html', err_msg=err_msg)
