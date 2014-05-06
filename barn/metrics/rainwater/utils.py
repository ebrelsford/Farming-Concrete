import requests

from django.conf import settings


base_url = 'http://api.wunderground.com/api/%(api_key)s/history_%(date)s/q/%(lat)f,%(lng)f.json'


def get_rainwater_history(latlng, date):
    data = requests.get(base_url % {
        'api_key': settings.WUNDERGROUND_API_KEY,
        'date': date.strftime('%Y%m%d'),
        'lat': latlng[0],
        'lng': latlng[1],
    })
    return float(data.json()['history']['dailysummary'][0]['precipi'])


#
# eg
# from datetime import date
# get_rainwater_history([40.680020,-73.963308], date.today())
#
