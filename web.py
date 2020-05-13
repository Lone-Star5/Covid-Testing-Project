from flask import Flask
from flask import render_template, redirect, request, session
from twilio.rest import Client 
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy as np
import pandas as pd
import tkinter
from operator import itemgetter
import csv
import smtplib
from email.mime.text import MIMEText
from prettytable import from_csv


# SocketServer.TCPServer.allow_reuse_address = True


# open file
def tkn():
	root = tkinter.Tk()
	with open("Warddetails.csv", newline = "") as file:
	   reader = csv.reader(file)

	   # r and c tell us where to grid the labels
	   r = 0
	   for col in reader:
	      c = 0
	      for row in col:
	         # i've added some styling
	         label = tkinter.Label(root, width = 20, height = 2, \
	                               text = row, relief = tkinter.RIDGE)
	         label.grid(row = r, column = c)
	         c += 1
	      r += 1
	root.mainloop()



app = Flask(__name__)

# data = [
# 		{'wardId' : '1', 'wardName' : 'Kormangala', 'com' : '25'},
# 		{'wardId' : '2', 'wardName' : 'Indiranagar', 'com' : '25'},
# 		{'wardId' : '3', 'wardName' : 'Whitefield', 'com' : '25'},
# 		{'wardId' : '4', 'wardName' : 'Brookefield', 'com' : '25'}
		
# ]
data =[]
df = pd.read_csv("Warddetails.csv")
containmentZone = []
for i in range(198):
	a = {"wardNo": df["WardNo"][i],
       "wardName": df["WardName"][i],
       "com": df["Comorbidities"][i],
       "red zone": df["ContainmentZone"][i],
       "pos":df["ProbableCases"][i]}
	data.append(a)

test = []
def func1(data):
	temp = sorted(data, key=itemgetter('com'))
	temp.reverse()
	bus = []
	rem = []
   	# flag = 0
	van = 0
	n = len(temp)
	for i in range(3):
		flag = 0
		Bus = []
		remTest = 100
		for j in range(n):
			if (temp[j]['red zone'] == 'Yes'):
				continue
			Busi = {}
			if (remTest <= 0):
			 	break
			if (temp[j]['com'] == 0):
			 	continue;
			if (temp[j]['com'] >= 100):
				temp[j]['com'] -= remTest
				Busi['wardName'] = temp[j]['wardName']
				Busi['com'] = remTest
				remTest = 0
				flag = 1
				Bus.append(Busi);
				break
			else:
				if (remTest >= temp[j]['com']):
					Busi['wardName'] = temp[j]['wardName']
					Busi['com'] = temp[j]['com']
					remTest -= temp[j]['com']
					temp[j]['com'] = 0
					flag = 1
					Bus.append(Busi)
				else:
					temp[j]['com'] -= remTest
					Busi['wardName'] = temp[j]['wardName']
					Busi['com'] = remTest
					Bus.append(Busi)
					flag = 1
					remTest = 0;
					break
		if (flag == 1):
			van += 1
			bus.append(Bus)

	if (van < 3):
		while (van < 3):
			flag = 0
			Bus = []
			remTest = 100
			for j in range(n):
				if (temp[j]['red zone'] == 'yes'):
					continue
				Busi = {}
				if (remTest <= 0):
					break
				if (temp[j]['pos'] == 0):
					continue;
				if (temp[j]['pos'] >= 100):
					temp[j]['pos'] -= remTest
					Busi['ward name'] = temp[j]['ward name']
					Busi['com'] = remTest
					remTest = 0
					flag = 1
					Bus.append(Busi);
					break
				else:
					if (remTest >= temp[j]['pos']):
						Busi['wardName'] = temp[j]['wardName']
						Busi['com'] = temp[j]['pos']
						remTest -= temp[j]['pos']
						temp[j]['pos'] = 0
						flag = 1
						Bus.append(Busi)
					else:
						temp[j]['pos'] -= remTest
						Busi['wardName'] = temp[j]['wardName']
						Busi['com'] = remTest
						Bus.append(Busi)
						flag = 1
						remTest = 0;
						break
			van += 1;
			bus.append(Bus)

	if (van == 3):
		for i in range(n):
			remi = {}
			remi['wardName'] = temp[i]['wardName']
			remi['Total remaining Tests to be performed'] = temp[i]['com'] + temp[i]['pos']
			rem.append(remi)
	# OUTPUT
	data = rem
	test = bus
	return test

def warddet():
	columns = ['WardNo','WardName','ContainmentZone','Comorbidities','ProbableCases','CompletelyVerified']
	df = pd.read_csv('Warddetails.csv', names=columns)

	return df

def persondet():
	columns = ['Member Id','Ward No','Ward Name','Age','Gender','Symptoms']
	df = pd.read_csv('PersonData.csv', names=columns)

	return df


def message(number):
	account_sid = 'Account_ID'
	auth_token = 'Auth_token'
	  
	client = Client(account_sid, auth_token) 

	message = client.messages.create( 
	                              from_='Number', 
	                              body ='Hi, Testing team will arrive in 1-2 working days', 
	                              to = number
	                          ) 
	  
	print(message.sid)

def email(em):

	fromx = 'Email_ID'
	to  = em
	msg = MIMEText('HI! Your Appointment for Covid-19 Testing is Scheduled')
	msg['Subject'] = 'Covid-19 Testing'
	msg['From'] = fromx
	msg['To'] = to

	server = smtplib.SMTP('smtp.gmail.com:Number')
	server.starttls()
	server.ehlo()
	server.login('Email_ID', 'Password')
	server.sendmail(fromx, to, msg.as_string())
	server.quit()




@app.route('/')
def index(test = test,rem = data):
	test = func1(data)
	print(test)
	return render_template('index.html',test = test,rem = rem)

@app.route('/message')
def msg():
	return render_template('message.html')

@app.route('/sendmessage',methods = ['GET','POST'])
def msg1():
	if(request.method == 'POST'):
		number = str(request.form['number'])
	message(number)
	return redirect('/')

@app.route('/sendemail', methods = ['GET', 'POST'])
def msg2():
	if(request.method == 'POST'):
		em = str(request.form['email'])
	email(em)
	return redirect('/')


@app.route('/display1')
def dis():
	df = warddet()
	df = df.to_html()
	print(type(df))
	return render_template('display.html',df = df)

@app.route('/display2')
def dis2():
	df = persondet()
	df = df.to_html()
	print(type(df))
	return render_template('display.html',df = df)


@app.route('/update')
def update():
	return redirect('/')

