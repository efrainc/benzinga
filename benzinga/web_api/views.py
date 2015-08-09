from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

import urllib2
import json
# Create your views here.


def home(request):
    context = {}

    if 'portfolio' in request.session:
        value = request.session["portfolio"]
    else:
        request.session['portfolio'] = 100000
        value = request.session['portfolio']
    context['current_value'] = value

    if 'purchased' in request.session:
        pass
    else:
        request.session['purchased'] = []

    if request.method == 'POST':
        symbol = request.POST['symbol'].upper()
        api_endpint = 'http://careers-data.benzinga.com/rest/richquote?symbols=%s' \
                      % symbol
        req = urllib2.urlopen(api_endpint)
        data = json.load(req)
        if 'error' in data[symbol]:
            return HttpResponseRedirect(reverse('web_api:whoops'))
        bidprice = data[symbol]['bidPrice']
        context['bidprice'] = bidprice
        askprice = data[symbol]['askPrice']
        context['askprice'] = askprice
        context['symbol'] = symbol
        request.session['symbol'] = symbol
        request.session['bidprice'] = bidprice
        request.session['askprice'] = askprice
    context['purchased'] = request.session['purchased']
    return render(request, 'base.html', context)


def trans(request):
    context = {}

    if 'portfolio' in request.session:
        value = request.session["portfolio"]
    else:
        request.session['portfolio'] = 100000
        value = request.session['portfolio']

    if request.method == 'POST':
        purchased = request.session['purchased']
        quantity = request.POST['quantity']
        ask_price = request.session['askprice']
        if 'buy' in request.POST:
            symbol = request.session['symbol']
            switch = False

            for i in range(len(purchased)):
                if symbol == purchased[i][0]:
                    holder = purchased[i]
                    purchased[i] = (holder[0], (int(holder[1]) + int(quantity)), ask_price)
                    switch = True
            if switch is False:
                purchased.append((symbol, quantity, ask_price))

            cost = int(quantity) * int(ask_price)
            free_funds = value - cost
            context['current_value'] = free_funds
            request.session['portfolio'] = free_funds

        elif 'sell' in request.POST:
            symbol = request.POST['symbol']
            for i in range(len(purchased)):
                if symbol == purchased[i][0]:
                    holder = purchased[i]
                    purchased[i] = (holder[0], (int(holder[1]) - int(quantity)), ask_price)

            cost = int(quantity) * int(ask_price)
            free_funds = value + cost
            context['current_value'] = free_funds
            request.session['portfolio'] = free_funds

        request.session['purchased'] = purchased
        context['purchased'] = purchased
        return HttpResponseRedirect(reverse('web_api:thanks'))


def thanks(request):
    return render(request, 'thanks.html')

def whoops(request):
    return render(request, 'whoops.html')

