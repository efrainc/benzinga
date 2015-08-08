from django.shortcuts import render
from django.http import HttpResponse

import urllib2
import json
# Create your views here.

def home(request):
    context = {}

    if 'portfolio' in request.session:
        value = request.session["portfolio"]
    else:
        request.session['portfolio'] = 10000
        value = request.session['portfolio']
    context['current_value'] = value

    # symbol = 'AAPL'

    if request.method == 'POST':
        symbol = request.POST['symbol']
        api_endpint = 'http://careers-data.benzinga.com/rest/richquote?symbols=%s' \
                      % symbol
        req = urllib2.urlopen(api_endpint)
        data = json.load(req)
        bidprice = data[symbol]['bidPrice']
        context['bidprice'] = bidprice
        askprice = data[symbol]['askPrice']
        context['askprice'] = askprice
        context['symbol'] = symbol
    # context['purchased'] = [('AAPL', 20, 12), ]
    return render(request, 'base.html', context)
