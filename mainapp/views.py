from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import unquote
from . import forms

# Create your views here.
def index(request):
    return render(request,'index.html')


def search(request):
    list = RozetkaParser('видеокарта')
    context = {
        "data": list
        }
    return render(request, 'results.html', context)

def search1(request):
    list = [{'name' : 'qwe', 'price' : 'qwe', 'eveilable' : 'True'}, {'name' : 'asd', 'price' : 'qwe', 'eveilable' : 'True'}, {'name' : 'zxc', 'price' : 'qwe', 'eveilable' : 'True'}]
    context = {
        "data": list
        }
    return render(request, 'results.html', context)


def rozetka_search(request):
    form = forms.RozetkaForm(request.POST or None)
    if form.is_valid():
        context = {
            'Form' : form,
            "data": RozetkaParser( form.cleaned_data['searchField'])
            }
        print()
        return render(request, 'search_in_rozetka.html', context)
    context = {
        'Form' : form,
        }
    return render(request, 'search_in_rozetka.html', context)

def foxtrot_search(request):
    form = forms.RozetkaForm(request.POST or None)
    if form.is_valid():
        context = {
            'Form' : form,
            "data": FoxtrotParser( form.cleaned_data['searchField'])
            }
        print()
        return render(request, 'search_in_foxtrot.html', context)
    context = {
        'Form' : form,
        }
    return render(request, 'search_in_foxtrot.html', context)

def RozetkaParser(searchQuery):
    url = 'https://rozetka.com.ua/search/?text='+searchQuery
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
               'Connection': 'keep-alive',
               'DNT': '1',
               'Host': 'rozetka.com.ua',
               'Referer': 'https://rozetka.com.ua/',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
    r = requests.get(url, headers=headers)

    text = r.text
    soup = BeautifulSoup(text, 'html.parser')
    searchList = soup.find('div', {'class': 'g-i-tile-l'})
    items = searchList.find_all('div', {'class': 'g-i-tile-i-box-desc'})
    searchData = []
    for item in items:

        name = item.find(
            'div', {'class': 'g-i-tile-i-title clearfix'}).find('a').text

        priceDiv = item.find('div', {'class': 'g-price-uah'})
        if not priceDiv:
            priceDiv = item.find(
                'div', {'name': 'prices_active_element_original'})
            js = re.search('%7B\S*%7D', str(priceDiv)).group()
            js = unquote(unquote(js))
            price = json.loads(js)['price']
        else:
            price = priceDiv
        price = price.text

        reviews = item.find(
            'span', {'class': 'g-rating-reviews'}).text
        img = item.find('img')

        if not img['src']:
            img['src'] = img['data-rz-lazy-load-src']
        src = img['src']

        link = item.find(
            'div', {'class': 'g-i-tile-i-image'}).find('a').get('href')
        reviewsLink = item.find(
            'div', {'class': 'g-rating'}).find('a').get('href')
        status = item.find('div', {'class': 'g-i-status'})

        if not status or status.text.strip() == '':
            status = 'В наличии'
        else:
            status = status.text
        searchData.append({
            'name': name.strip(),
            'price': price.strip(),
            'reviews': reviews.strip(),
            'src': src.strip(),
            'link': link.strip(),
            'reviewsLink': reviewsLink.strip(),
            'status': status.strip()
        })
    return searchData


def FoxtrotParser(searchQuery):
    url = 'https://www.foxtrot.com.ua/ru/search?query='+searchQuery
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
               'Connection': 'keep-alive',
               'DNT': '1',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
    r = requests.get(url, headers=headers)
    text = r.text
    soup = BeautifulSoup(text, 'html.parser')
    searchList = soup.find('div', {'class': 'listing-container'})
    items = searchList.find_all('div', {'class': 'listing-item'})
    searchData = []
    for item in items:

        name = item.find(
            'p', {'class': 'info'}).text

        price = item.find('span', {'class': 'numb'}).text

        reviewsCount = item.find(
            'span', {'class': 'review-number'}).text
        reviewsWord = item.find(
            'span', {'class': 'review-text'}).text
        reviews = reviewsCount+' '+reviewsWord

        img = item.find('img')
        src = img['src']

        link = item.find(
            'a', {'class': 'detail-link'}).get('href')
        link = 'https://www.foxtrot.com.ua'+link

        reviewsLink = item.find(
            'a', {'class': 'reviews-link'}).get('href')
        reviewsLink = 'https://www.foxtrot.com.ua'+reviewsLink

        status = item.find('span', {'class': 'able-text'}).text

        searchData.append({
            'name': name.strip(),
            'price': price.strip(),
            'reviews': reviews.strip(),
            'src': src.strip(),
            'link': link.strip(),
            'reviewsLink': reviewsLink.strip(),
            'status': status.strip()
        })
    return searchData
