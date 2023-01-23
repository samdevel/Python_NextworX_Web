from flask import Flask, flash, render_template, request, redirect
import pandas as pd
import csv
from netmiko import ConnectHandler
from netmiko import Netmiko
import time
import os
#from ssh import connect_sw,send_cli
from credentials import switch_credentials

app = Flask(__name__)


#################################################################################################
# Arch/Developer: sm@Devel                                                                      #
# This software released mainly for education and You may distribute and develop it             #
# Activities other than copying, distribution and modification are not covered by this License  #
# You may accept at your own risks for using this app                                           #
#################################################################################################

#################################################
            # Flask Routes #
#################################################


################## MAIN MENU ####################
@app.route("/")
def home():
  # send variable user to local html, This is for a testing page only
  user = {'username': 'sm@devel'}

  comments = [
        {
            'learning': {'subject': 'Switching'},
            'content': 'Learning Switching and Services!'
        },
        {
            'learning': {'subject': 'Routing'},
            'content': 'Learning Routing and Services!'
        }
    ]
  comment2 = {'content2': 'It is just a comment for testing variable'}
  return render_template('index.html', title='Home', user=user, comments=comments, comment2=comment2)


@app.route("/uat")
def uat():
  return render_template("uat.html")

@app.route("/custom")
def custom():
  return render_template("custom.html")

@app.route("/monitoring")
def monitoring():
  return render_template("monitoring.html")

@app.route("/filedir")
def filedir():
  return render_template("filedir.html")


@app.route("/about")
def about():
  return render_template("about.html")

##############################################################


##############################################################
############### TOOLs for CLI (Quick Test) ###################
##############################################################

@app.route('/cli',methods = ['POST'])
def cli():
  if request.method == 'POST':
    try:
	pass

        show_cmd = request.form['web_show_cmd']

	# Netmiko
	'''
	# Init test #
	cisco_rtr = {
    		'device_type': 'cisco_ios',
    		'host': '10.1.1.1',
    		'username': 'admin',
    		'password': 'cisco',
		'secret': 'cisco',
	}

	net_connect = ConnectHandler(**cisco_rtr)
	net_connect.enable()
	
	output_cli = net_connect.send_command(show_cli)
	'''

	cisco_rtr = {
		'device_type':'cisco_ios',
		'ip':'10.1.1.1',
		'username':switch_credentials['username'],
		'password':switch_credentials['password'],
                'secret':switch_credentials['secret'],
	}

	net_connect = ConnectHandler(**cisco_rtr)
	net_connect.enable()

	output = net_connect.send_command(show_cmd)

	'''
	#print(output)
	with open ('%s.txt' % show_cmd, 'w') as wf:
	    wf.write(output)
	'''

	#################### Logging output to a file #####################

	curr_date = time.strftime('%Y-%m-%d_%H%M%S')
	file_cmd = (show_cmd) + "_" + (curr_date) + '.txt'
	dir_path = 'output/show_command'
	#Read dir > dir_path = '/home/sams/Desktop/Flask_Projects/PB21/output/show_command'
	file_name = os.path.join(dir_path, file_cmd)

	with open ('%s' %file_name, 'w') as wf:
	    wf.write(output)

	################## End of Logging output to a file #################

	        
    finally:
         return render_template('show_output.html', web_cli_list=show_cmd, web_print=output) 

##############################################################
##################### CLI read input IP ######################
##############################################################

@app.route('/cli_cust',methods = ['POST'])
def cli_cust():
  if request.method == 'POST':
    try:
	pass

        show_cmd = request.form['web_show_cmd']

	### Netmiko ###
	cisco_rtr = {
		'device_type':'cisco_ios',
		'ip':ip_add,
		'username':switch_credentials['username'],
		'password':switch_credentials['password'],
                'secret':switch_credentials['secret'],
	}

	net_connect = ConnectHandler(**cisco_rtr)
	net_connect.enable()

	output = net_connect.send_command(show_cmd)

	#################### Logging output to a file #####################

	curr_date = time.strftime('%Y-%m-%d_%H%M%S')
	file_cmd = (show_cmd) + "_" + (curr_date) + '.txt'
	dir_path = 'output/show_command'
	#Read dir > dir_path = '/home/sams/Desktop/Flask_Projects/PB21/output/show_command'
	file_name = os.path.join(dir_path, file_cmd)

	with open ('%s' %file_name, 'w') as wf:
	    wf.write(output)

	################## End of Logging output to a file #################

	        
    finally:
         return render_template('show_output.html', web_cli_list=show_cmd, web_print=output) 

##############################################################
################## UAT Menu - READ Files #####################
##############################################################

@app.route('/cli_file',methods = ['POST'])
def cli_file():
  if request.method == 'POST':
    try:
        
        ip_list = request.form['web_ip_list']
	upload_ip_file = ip_list
	upload_dir_path = 'transfer/upload/uat'
	upload_fipname = os.path.join(upload_dir_path, upload_ip_file)

        with open ('%s' %upload_fipname, 'r') as ipf:
	      for y in ipf:
		ip = y.strip()
		print(ip)

	        ### Netmiko
	        cisco_rtr = {
		   'device_type':'cisco_ios',
		   'ip':ip,
		   'username':switch_credentials['username'],
		   'password':switch_credentials['password'],
               	   'secret':switch_credentials['secret'],
	        }
		
	        net_connect = ConnectHandler(**cisco_rtr)
                net_connect.enable()
		
		# cmd file
		cmd_list = request.form['web_cmd_list']
	        upload_file = cmd_list
		upload_dir_path = 'transfer/upload/uat'
		upload_fname = os.path.join(upload_dir_path, upload_file)

        	with open ('%s' %upload_fname, 'r') as f:

	             for x in f:
                        
			show_read_file = x.strip()
			print(show_read_file)
		   	output_read_file = net_connect.send_command(show_read_file)
			time.sleep(5)

			#################### Logging output to a file #####################

			curr_date = time.strftime('%Y-%m-%d_%H%M%S')
			file_cmd = ip + "_" + (show_read_file) + "_" + (curr_date) + '.txt'
			dir_path = 'output/uat'
			#Read dir > dir_path = '/home/sams/Desktop/Flask_Projects/PB21/output/show_command'
			file_name = os.path.join(dir_path, file_cmd)

			with open ('%s' %file_name, 'w') as wf:
			    wf.write(output_read_file)

			################## End of Logging output to a file #################
		        
    finally:
         return render_template('uat_output.html', web_read_file=show_read_file, web_print=output_read_file)          
         #return render_template('uat_output.html', web_read_file=show_read_file)        



##############################################################
############# Custom Menu > CLI using Pick List ##############
##############################################################


@app.route('/cust_pick_cli',methods = ['POST'])
def cust_pick_cli():
  if request.method == 'POST':
    try:
        
        	ip_add = request.form['web_ip_add']
	
		### Netmiko
	        cisco_rtr = {
		   'device_type':'cisco_ios',
		   'ip':ip_add,
		   'username':switch_credentials['username'],
		   'password':switch_credentials['password'],
               	   'secret':switch_credentials['secret'],
	        }
		
	        net_connect = ConnectHandler(**cisco_rtr)
                net_connect.enable()
		
		# cmd file
		show_cmd_cust = request.form['web_cmd_pick']
	        output_cmd_cust = net_connect.send_command(show_cmd_cust)
		time.sleep(5)

		#################### Logging output to a file #####################

		curr_date = time.strftime('%Y-%m-%d_%H%M%S')
		file_cmd = ip_add + "_" + (show_cmd_cust)+ "_" + (curr_date) + '.txt'
		dir_path = 'output/custom'
		#Read dir > dir_path = '/home/sams/Desktop/Flask_Projects/PB21/output/show_command'
		file_name = os.path.join(dir_path, file_cmd)

		with open ('%s' %file_name, 'w') as wf:
		    wf.write(output_cmd_cust)

		################## End of Logging output to a file #################
		        
    finally:
         return render_template('custom_output.html', web_cmd_cust=show_cmd_cust, web_print=output_cmd_cust)          
         #return render_template('custom_output.html', web_read_file=show_read_file)        


##############################################################
########## Custom Menu - using a CLI as input text ###########
##############################################################

@app.route('/cust_cli',methods = ['POST'])
def cust_cli():
  if request.method == 'POST':
    try:
        
        	ip_add = request.form['web_ip_add2']
	
		### Netmiko
	        cisco_rtr = {
		   'device_type':'cisco_ios',
		   'ip':ip_add,
		   'username':switch_credentials['username'],
		   'password':switch_credentials['password'],
               	   'secret':switch_credentials['secret'],
	        }
		
	        net_connect = ConnectHandler(**cisco_rtr)
                net_connect.enable()
		
		# cmd file
		show_cmd_cust2 = request.form['web_cmd']
		#output_cmd_cust2 = net_connect.send_command(show_cmd_cust2)
	        output_cmd_cust2 = net_connect.send_config_set(show_cmd_cust2)
		time.sleep(5)

		#################### Logging output to a file #####################

		curr_date = time.strftime('%Y-%m-%d_%H%M%S')
		file_cmd = ip_add + "_" + (show_cmd_cust)+ "_" + (curr_date) + '.txt'
		dir_path = 'output/custom'
		#Read dir > dir_path = '/home/sams/Desktop/Flask_Projects/PB21/output/show_command'
		file_name = os.path.join(dir_path, file_cmd)

		with open ('%s' %file_name, 'w') as wf:
		    wf.write(output_cmd_cust2)

		################## End of Logging output to a file #################
		        
    finally:
         return render_template('custom_output.html', web_cmd_cust=show_cmd_cust2, web_print=output_cmd_cust2)          
         #return render_template('custom_output.html', web_read_file=show_read_file)        




########## TOOLs for CLI (NOT Ready) ###########
@app.route('/clix',methods = ['POST'])
def clix():
  if request.method == 'POST':
    try:

        show_cli = request.form['web_show_cli']

	# Netmiko
	device = connect_sw('device_type','ip','username','password','secret')
	output_cli = send_cli('show_cli')


	################## Logging output to a file #################
	curr_date = time.strftime('%Y-%m-%d_%H%M%S')
	file_cmd = (show_cli) + "_" + (curr_date) + '.txt'
	dir_path = 'output/show_command'
	#Read dir > dir_path = '/home/sams/Desktop/Flask_Projects/PB21/output/show_command'

	file_name = os.path.join(dir_path, file_cmd)

	with open ('%s' %file_name, 'w') as wf:
	    wf.write(output_cli)

	############## End of Logging output to a file ##############

		        
    finally:
         #return render_template('show_cli.html', web_show_cli=show_cli, web_print=connect_ssh(device)) 
         return render_template('show_cli.html', web_show_cli=show_cli, web_print=send_cli(show_cli)) 

##############################################################
######################### UPLOAD File ########################
##############################################################
#ALLOWED_EXTENSIONS = {'txt'}

#UPLOAD_FOLDER = 'transfer/upload'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["UPLOAD_FOLDER"] = "/home/sams/Documents/Flask_Projects/UAT/transfer/upload/uat"
#app.config["UPLOAD_FOLDER"] = "/home/sams/flask/UAT/transfer/upload/uat"
#~/flask/UAT/transfer/upload

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if request.files:

            upload_file = request.files['web_upload_file']
	    print(upload_file)
	    upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'], upload_file.filename))
	    return redirect(request.url)

    return render_template('uat.html')


  
if __name__ == "__main__":
  #app.run(debug=True)
  app.run(host='0.0.0.0', debug=True, port=5000)

