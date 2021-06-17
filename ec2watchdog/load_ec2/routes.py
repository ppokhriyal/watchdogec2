from os import access
from flask import Blueprint,render_template,url_for, flash, redirect, request,jsonify
from ec2watchdog import app,db
from ec2watchdog.models import AccessKey
from ec2watchdog.load_ec2.forms import Ec2FilterForm
import datetime
import boto3
import botocore

#Blueprint object
blue = Blueprint('load_ec2',__name__,template_folder='templates')

#Load EC2
@blue.route('/loadec2/<string:rowinfo>',methods=['GET','POST'])
def loadec2(rowinfo):
    rowid = rowinfo.split(":")[0]
    region = rowinfo.split(":")[1]

    #get access info
    get_access_info = AccessKey.query.get(rowid)
    
    #get accesskey and secretkey
    accesskey = get_access_info.accesskeyid
    secretkey = get_access_info.secretkeyid
    
    # connect to boto3 ec2
    client = boto3.client('ec2',region_name=region,aws_access_key_id=accesskey,aws_secret_access_key=secretkey)
    instance_load = client.describe_instances()
    instance_load_length = len(instance_load['Reservations'])
    instance_data = instance_load['Reservations']
    #for i in instance_data:
    #    print(i['Instances'])
    return render_template('load_ec2/load_ec2.html',title="Load EC2",instance_data=instance_data,instance_load_length=instance_load_length,row=rowid,awsregion=region)

#Filter EC2
@blue.route('/ec2/<int:rowid>',methods=['POST','GET'])
def ec2(rowid):
    form = Ec2FilterForm()
    if form.validate_on_submit():
        return redirect(url_for('load_ec2.loadec2',rowinfo=str(rowid)+":"+form.awsregion.data))
    return render_template('load_ec2/ec2.html',title="EC2",form=form,row=rowid)

#Start ec2 instance
@blue.route('/startec2/<string:idinstance>',methods=['GET','POST'])
def startec2(idinstance):
    # Get instance info
    instance_id = idinstance.split('_')[0]
    row_id = idinstance.split('_')[1].split(':')[0]
    region = idinstance.split('_')[1].split(':')[1]

    #get access info
    get_access_info = AccessKey.query.get(row_id)

    #get accesskey and secretkey
    accesskey = get_access_info.accesskeyid
    secretkey = get_access_info.secretkeyid

    # check the status of instance
    client = boto3.client('ec2',region_name=region,aws_access_key_id=accesskey,aws_secret_access_key=secretkey)
    response = client.describe_instances(InstanceIds=[instance_id])
    status = ['running','pending','terminated']

    if response['Reservations'][0]['Instances'][0]['State']['Name'] in status:
        return jsonify({'result':'fail'})
    else:
        ec2_start_response = client.start_instances(InstanceIds=[instance_id])
        return jsonify({'result':'pass'})

#Stop ec2 instance
@blue.route('/stopec2/<string:idinstance>',methods=['GET','POST'])
def stopec2(idinstance):
    # Get instance info
    instance_id = idinstance.split('_')[0]
    row_id = idinstance.split('_')[1].split(':')[0]
    region = idinstance.split('_')[1].split(':')[1]

    #get access info
    get_access_info = AccessKey.query.get(row_id)

    #get accesskey and secretkey
    accesskey = get_access_info.accesskeyid
    secretkey = get_access_info.secretkeyid

    # check the status of instance
    client = boto3.client('ec2',region_name=region,aws_access_key_id=accesskey,aws_secret_access_key=secretkey)
    response = client.describe_instances(InstanceIds=[instance_id])
    status = ['pending','terminated','stopping','stopped','shutting-down']
   
    if response['Reservations'][0]['Instances'][0]['State']['Name'] in status:
        return jsonify({'result':'fail'})
    else:
        ec2_stop_response = client.stop_instances(InstanceIds=[instance_id])
        return jsonify({'result':'pass'})

# Reboot ec2 instance
# @blue.route('/rebootec2/<string:idinstance>',methods=['GET','POST'])
# def rebootec2(idinstance):
#     # Get instance info
#     instance_id = idinstance.split('_')[0]
#     row_id = idinstance.split('_')[1].split(':')[0]
#     region = idinstance.split('_')[1].split(':')[1]

#     #get access info
#     get_access_info = AccessKey.query.get(row_id)

#     #get accesskey and secretkey
#     accesskey = get_access_info.accesskeyid
#     secretkey = get_access_info.secretkeyid

#     # check the status of instance
#     client = boto3.client('ec2',region_name=region,aws_access_key_id=accesskey,aws_secret_access_key=secretkey)
#     response = client.describe_instances(InstanceIds=[instance_id])
#     status = ['terminated','pending','stopping','shutting-down']
#     print(response)
#     if response['Reservations'][0]['Instances'][0]['State']['Name'] in status:
#         return jsonify({'result':'fail'})
#     else:
#         print ("REBOOTING ...SS")
#         ec2_restart_response = client.reboot_instances(InstanceIds=[instance_id])
#         print(ec2_restart_response)
#         return jsonify({'result':'pass'})


#Terminate ec2 instance
@blue.route('/terminatec2/<string:idinstance>',methods=['GET','POST'])
def terminatec2(idinstance):
    # Get instance info
    instance_id = idinstance.split('_')[0]
    row_id = idinstance.split('_')[1].split(':')[0]
    region = idinstance.split('_')[1].split(':')[1]

    #get access info
    get_access_info = AccessKey.query.get(row_id)

    #get accesskey and secretkey
    accesskey = get_access_info.accesskeyid
    secretkey = get_access_info.secretkeyid

    # check the status of instance
    client = boto3.client('ec2',region_name=region,aws_access_key_id=accesskey,aws_secret_access_key=secretkey)
    response = client.describe_instances(InstanceIds=[instance_id])
    #terminate status
    status = ['terminated','pending']
    print(response)
    if response['Reservations'][0]['Instances'][0]['State']['Name'] in status:
        return jsonify({'result':'fail'})
    else:
        ec2_terminate_response = client.terminate_instances(InstanceIds=[instance_id])
        return jsonify({'result':'pass'})
