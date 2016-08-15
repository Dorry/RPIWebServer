from flask import Flask, render_template, session, url_for, redirect, request
import os, subprocess

USERID = ''
USERPW = ''

def getCPU_Temperature():
    if os.name != 'nt':
        temp = subprocess.check_output('vcgencmd measure_temp', shell=True)
        temp = str(temp).split('=')[1]
        temp = temp.replace('\\n"', '')
        return temp
    return "0'C"

def isCameraOn():
    camon_list = subprocess.check_output("ps -ef | egrep 'raspivid|exam' | grep -v grep", shell=True)
    if len(camon_list) > 0:
        return True
    return False

app = Flask(__name__)

@app.route('/')
def index():
    context = {'cpu_temp': getCPU_Temperature(),
               'isoff': not isCameraOn()}
    return render_template('index.html', context)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == USERID and request.form['userpass'] == USERPW:
            session['login_ok'] = True
        else:
            session['login_ok'] = False
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('login_ok', None)
    return redirect(url_for('index'))

@app.route('/camon')
def camon():
    subprocess.call("nohup /home/pi/pi_cam.sh &")
    context = {'isoff': True,
               'msg': "카메라가 실행되지 않았습니다"}
    if isCameraOn():
        context['isoff'] = False
        context['msg'] = "카메라가 정상실행되었습니다"
    return render_template('cam_status.html', context)


@app.route('/camoff')
def camoff():
    result = subprocess.call("kill -9 `ps -ef | egrep 'raspivid|exam' | grep -v grep | awk 'print $2'`")
    context = {'isoff': False,
               'msg': "카메라가 종료되지 않았습니다"}
    if not result:
        if not isCameraOn():
            context['isoff'] = True
            context['msg'] = "카메라가 정상종료 되었습니다"
    return render_template('cam_status.html', context)

@app.route('/restart')
def restart():
    if session['login_ok']:
        if os.name != 'nt':
            session.pop('login_ok', None)
            os.system('sudo reboot now')
        return 'Now rebooting at Server!'
    return redirect(url_for('login'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run('0.0.0.0', 4293)
