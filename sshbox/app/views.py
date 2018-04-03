
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from app.forms import AccountForm
import docker
import random
import os

# Create your views here.

def home_view(request, template = 'home.html'):
	return render_to_response(template)

def list_view(request, template = 'list.html'):
	client = docker.from_env()
	account_names = accounts_available(client.images.list())
	accounts_active = accounts_running(client.containers.list(), client)
	return render_to_response(template, {'accounts': account_names, 'container': accounts_active}, context_instance=RequestContext(request))

def launch_view(request, template = 'launch.html'):
	client = docker.from_env()
	container_launch = {}
	msg = []
	host_port = random.randrange(8000,9000)
	accounts_active = accounts_running(client.containers.list(), client)
	if request.method == 'POST':
		form = AccountForm(request.POST)
		if form.is_valid():
			image = form.cleaned_data['account']
			if accounts_active.has_key(image):
				msg.append('account is already active')
				container_launch [image] = accounts_active[image]
			else:
				#cmd = "docker run -d -p %s:8443 sshbox:%s" %(host_port, image)
				cmd = "docker run -v /logvol:/logvol -d -p %s:8443 -h %s sshbox:%s" %(host_port, image, image)
				run_cmd = os.system(cmd)
				if run_cmd == 0:
					container_launch [str(image)] = host_port
					msg.append('account activated click below link to access account')
				else:
					msg.append('sorry the account name is not valid')
			form = AccountForm()
	else:
		form = AccountForm()
	return render_to_response(template, {'form':form, 'container':container_launch, 'msg':msg}, context_instance = RequestContext(request))

def accounts_available(images):
	list = []
	accounts = []
	for i in images:
		a,b,c = str(i).split('\'')
		list.append(b)
	#filter the sshbox repository images        
	for i in (filter(lambda k: 'sshbox' in k, list)):
		a,b = str(i).split(':')
		accounts.append(b)
	return accounts

def accounts_running(docker, client):
	docker_running = {}
	for i in docker:
		a,b = str(i).split(':')
		container = client.containers.get((b.strip()).strip('>'))
		if (str(container.attrs['State']['Status'])) == 'running':
			a,b = str(container.attrs['Config']['Image']).split(':')
			docker_running [b]  = str(container.attrs['HostConfig']['PortBindings']['8443/tcp'][0]['HostPort'])
	return docker_running
