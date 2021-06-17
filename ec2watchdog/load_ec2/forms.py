from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


#EC2 Filter form
class Ec2FilterForm(FlaskForm):
    awsregion = SelectField('Region',choices=[('us-east-1','US East (N. Varginia)'),('us-east-2','US East (Ohio)'),
		('us-west-1','US West (N. California)'),('us-west-2','US West (Oregon)'),('af-south-1','Africa (CapeTown)'),
		('ap-east-1','Asia Pacific (Hong Kong)'),('ap-south-1','Asia Pacific (Mumbai)'),('ap-northeast-2','Asia Pacific (Seoul)'),
		('ap-southeast-1','Asia Pacific (Singapore)'),('ap-southeast-2','Asia Pacific (Sydney)'),
		('ap-northeast-1','Asia Pacific (Tokyo)'),('ca-central-1','Canada (Central)'),('eu-central-1','Europe (Frankfurt)'),
		('eu-west-1','Europe (Irekand)'),('eu-west-2','Europe (London)'),('eu-south-1','Europe (Milan)'),
		('eu-west-3','Europe (Paris)'),('eu-north-1','Europe (Stockholm)'),('me-south-1','Middle East (Bahrin)')])
    submit = SubmitField('Load EC2 instances')