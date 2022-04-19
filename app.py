import os
import sys
import select
import paramiko
import time
import smtplib
import platform
import subprocess
from flask import Flask, jsonify, request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from waitress import serve

app = Flask(__name__)


@app.route('/')
def apiCheck():
    return "Message : Remote VM Execution!"


@app.route('/checkVMStatus')
@app.route('/verifyVMStatus')
def vmStatus():
    try:
        command = "nc -w 5 -z ***REMOVED*** *****"
        response = os.system(command)
        retval = "False"
        if response == 0:
            retval = "UP"
        else:
            retVal = "DOWN"
    except Exception as ex:
        print("Error: ping exception = ", ex)
    return jsonify({"retval": retval})
    # return retval


@app.route('/isVMUp')
def isvmup():
    try:
        command = "nc -w 5 -z ***REMOVED*** *****"
        response = os.system(command)
        retval = "False"
        if response == 0:
            retval = "True"
        else:
            retVal = "False"
    except Exception as ex:
        print("Error: ping exception = ", ex)
    return jsonify({"retval": retval})
    # return retval


@app.route('/isVMDown')
def isvmdown():
    try:
        command = "nc -w 5 -z ***REMOVED*** *****"
        response = os.system(command)
        retval = "False"
        if response == 0:
            retval = "False"
        else:
            retVal = "True"
    except Exception as ex:
        print("Error: ping exception = ", ex)
    return jsonify({"retval": retval})
    # return retval


@app.route('/df')
def dfExec():
    # return "Message : Sent SSH df -H to remote server : ***REMOVED***!"
    return jsonify({"Message": "Sent SSH df -H to remote server : ***REMOVED***!"})


@app.route('/restart')
def restartVM():
    sshclnt = utils.getSSHClient()
    s = sshclnt.get_transport().open_session()
    paramiko.agent.AgentRequestHandler(s)
    sshclnt.exec_command("sudo /sbin/reboot", get_pty=True)
    # return "Message : Sent Restart remote server : ***REMOVED***!"
    return jsonify({"Message": "Sent Restart remote server : ***REMOVED***!"})


@app.route('/ping')
def ping():
    try:
        timeout = 1
        host = "10.0.0.1"
        retval = "True"
        if platform.system() == "Windows":
            command = "ping "+host+" -n 1 -w "+str(timeout*1000)
        else:
            command = "ping -i "+str(timeout)+" -c 1 " + host
        response = os.system(command)
        if response == 0:
            retval = "True"
        else:
            retVal = "False"
    except Exception as ex:
        print("Error: ping exception = ", ex)
    return retval


@app.route('/postmsg', methods=['POST'])
def post_msg():
    log = "in postmsg \n"
    data = request.get_json()

    instanceId, alarmName = data.get("instanceId")
    alarmName = data.get("alarmName")
    slog = send_email(instanceId, alarmName)

    log = log + " " + slog + "  message : Completed Send Email"
    return jsonify({log: log})


def send_email(instanceId, alarmName):
    # def send_email(toaddrs, email_subj, email_msg):
    # The mail addresses and password

    workplace_url = "https://cpd-cp4ba.itzroks-6620022x67-2q1yiu-4b4a324f027aea19c5cbc0c3275c4656-0000.us-south.containers.appdomain.cloud/bas/Workplace"
    sender_address = 'testibmvz@gmail.com'
    sender_passcode = '***REMOVED***'
    receiver_address = 'testibmvz@gmail.com'

    #mail_content = " Hello,  This is a simple mail -- WfPs Test Email to verify Notifications are working -- sent using Python SMTP library. Thank You"
    mail_content = "You have a task assigned awaiting approval. Please approve  Closed Loop Automation:" + \
        instanceId + " for Alarm" + alarmName
    mail_content = mail_content + workplace_url
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address

    fromaddr = "some.body@ibm.com"
    #toaddrs  = ["some.body@ibm.com;some.body@ibm.com"]

   # msg = MIMEText(email_msg)
    #msg['Subject'] = "Approval Tasks Assigned"

    try:
        #server = smtplib.SMTP( ============, 25)
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        # The subject line
        message['Subject'] = '"Approval Tasks Assigned" !!!.'

        message.attach(MIMEText(mail_content, 'plain'))
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()  # enable security
        # login with mail_id and password
        session.login(sender_address, sender_passcode)
        session.set_debuglevel(1)
        text = message.as_string()
        log = "calling send email"
        session.sendmail(sender_address, receiver_address, text)
        log = log + "\n done send email"
        session.quit()
        log = log + "\n Successfully sent email"
    except Exception as ex:
        print("Error: unable to send email", ex)
        log = log + "Error: unable to send email" + str(ex)

    return jsonify({log: log})
    # return log
    # -----------------------------------------------------------------------------------------------------------------------
# Utils class
# getSSHClient : Obtains SSHClient to execute command over SSH
# execCommand : function to execute command over SSH, which also closes connection after command execution
# -----------------------------------------------------------------------------------------------------------------------


class utils():
    def getSSHClient():
        sshclnt = paramiko.SSHClient()
        sshclnt.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #sshclnt.connect(=======", port=****, username=******, password=********)
        #sshclnt.connect(=======", port=****, username=******, password=============)
        sshclnt.connect(=======",
                        port=*****, username=******, password=============)
        return sshclnt

    def execCommand(command):
        try:
            sshclnt = utils.getSSHClient()
            stdin, stdout, stderr = sshclnt.exec_command(command)
            print("stdin", file=sys.stdin)
            print("stdout", file=sys.stdout)
            print("stderr=", file=sys.stderr)
            opt = stdout.readlines()
            opt = "".join(opt)
            print(opt)
        except Exception as ex:
            print("Authentication failed, please verify your credentials: %s" % ex)
        finally:
            sshclnt.close()


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
