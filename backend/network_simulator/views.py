from django.shortcuts import render
from django.http import HttpResponse
from . import business_logic
#from restframework import viewset

# Create your views here.

def init_sim(req):
    print('init sys')
    return HttpResponse('init system')
    
def route_data(req):
    print('route data')
    return HttpResponse('route data')
    
def collect_stats(req):
    print('collect stats')
    return HttpResponse('collect stats')