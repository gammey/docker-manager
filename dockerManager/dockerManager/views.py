#!/usr/bin/python
from django.http import HttpResponseRedirect
import json
def index(request):
	return HttpResponseRedirect("/static/docker.html");

		
