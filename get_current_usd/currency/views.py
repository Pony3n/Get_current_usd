import datetime
import requests
from bs4 import BeautifulSoup

from django.shortcuts import render
from django.utils import timezone

from .models import Currency


def get_current_usd(request):
    url = "https://ru.investing.com/currencies/usd-rub"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    div_tag = soup.find("div", {"class": 'text-5xl/9 font-bold md:text-[42px] md:leading-[60px] text-[#232526]'})
    actual_rate = float(div_tag.text.replace(',',''))


    if request.method == "POST":
        current_rate = Currency(current_rate=actual_rate, time_code=timezone.now())
        current_rate.save()


    if Currency.objects.last().time_code < timezone.now() - datetime.timedelta(days=1):
        initial_rate = Currency(current_rate=actual_rate, time_code=timezone.now())
        initial_rate.save()

    current_rate_obj = Currency.objects.last()

    prev_rate = Currency.objects.order_by("-time_code")[:10]

    data = {
        "current_rate": str(current_rate_obj.current_rate),
        "current_time": str(current_rate_obj.time_code)[:19],
        "last_requests": [prev.time_code for prev in prev_rate]
    }

    return render(request, 'currency/current_rate.html', {'data': data})
