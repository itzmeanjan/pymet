#!/usr/bin/python3

try:
    from requests import get
    from bs4 import BeautifulSoup
    from dateutil.parser import isoparse
    from time import localtime, asctime
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


def __convert_date_time_2_local__(dt_str):
    '''
        Converts YYYY-MM-DDTHH:MM:SSZ, formatted date string to local date_time string.
    '''
    try:
        return asctime(localtime(isoparse(dt_str.upper()).timestamp()))
    except Exception:
        return ''


def __parse_response__(content, dt_2_local):
    '''
        Parsing of XML document is performed here and returns python dict.
    '''
    data = {}
    try:
        handle = BeautifulSoup(content, features='xml')
        if(handle.meta and handle.meta.model):
            data.update({handle.meta.name: handle.meta.model.attrs})
        if(handle.product):
            for i, j in enumerate(handle.product.findAll('time')):
                if((not i) and j.location):
                    data.update({j.location.name: j.location.attrs})
                if(dt_2_local):
                    dt_from = __convert_date_time_2_local__(j.attrs.get('from'))
                    dt_to = __convert_date_time_2_local__(j.attrs.get('to'))
                    if(dt_from and dt_to):
                        key = '{};{}'.format(dt_from, dt_to)
                    else:
                        key = '{};{}'.format(j.attrs.get('from'), j.attrs.get('to'))
                else:
                    key = '{};{}'.format(j.attrs.get('from'), j.attrs.get('to'))
                tmp = {}
                if(j.location):
                    for k in j.location.findChildren():
                        tmp.update({k.name: k.attrs})
                if(tmp):
                    data.update({key: tmp})
    except Exception as e:
        data = {'error': str(e)}
    return data


def __perform_query__(url, data, dt_2_local, parse):
    '''
        Performs get query at provided url and returns parsed response.
    '''
    try:
        resp = get(url, params=data, headers={'User-Agent': 'pymetv1.0'})
        if(resp.ok):
            if(parse):
                return __parse_response__(resp.content, dt_2_local)
            return {'response': resp.content.decode('utf-8')}
        raise Exception('received {} from server'.format(resp.status_code))
    except Exception as e:
        return {'error': str(e)}


def fetch(lat, lon, msl=None, base_url='https://api.met.no/weatherapi/locationforecast/1.9/', dt_2_local=True, parse=True):
    '''
        Fetches forecast data from MET Norway, for a certain location, denoted by Latitude, Longitude and Meters above Sea Level(optional).
        Date time is by default converted to your local timezone. If you don't want this to happen, set dt_2_local = False, while calling this function.
        If you don't want it to parse XML response to python dict, set parse=False while invoking this function. By default it'll return parsed response as python dict, which might be eventually converted to JSON using json.dumps().
    '''
    if(msl):
        return __perform_query__(base_url, [('lat', lat), ('lon', lon), ('msl', msl)], dt_2_local, parse)
    else:
        return __perform_query__(base_url, [('lat', lat), ('lon', lon)], dt_2_local, parse)


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
