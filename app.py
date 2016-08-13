from flask import Flask, render_template, session, url_for, redirect, request
import os, subprocess

USERID = ''
USERPW = ''

def getCPU_Temperature():
    if os.name != 'nt':
        temp = subprocess.check_output('vcgencmd measure_temp', shell=True)
        temp = temp.split('=')
        return temp[1]
    return "0'C"

app = Flask(__name__)

@app.route('/')
def index():
    cpu_temp = getCPU_Temperature()
    return render_template('index.html', cpu_temp=cpu_temp)

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

@app.route('/restart')
def restart():
    if session['login_ok']:
        if os.name != 'nt':
            os.system('sudo reboot now')
        return 'Now rebooting at Server!'
    return redirect(url_for('login'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run('0.0.0.0', 4293)
