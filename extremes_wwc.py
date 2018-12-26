#!/usr/bin/python3

try:
    from forecast import get, BeautifulSoup, __convert_date_time_2_local__
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


def __parse_response__(content, dt_2_local):
    '''
        Extracts data from XML document and returns them as python dict.
    '''
    data = {}
    try:
        handle = BeautifulSoup(content, features='xml')
        if(handle.product):
            for i in handle.product.findAll('time'):
                if(dt_2_local):
                    dt_from = __convert_date_time_2_local__(i.attrs.get('from'))
                    dt_to = __convert_date_time_2_local__(i.attrs.get('to'))
                    if(dt_from and dt_to):
                        key = '{};{}'.format(dt_from, dt_to)
                    else:
                        key = '{};{}'.format(i.attrs.get('from'), i.attrs.get('to'))
                else:
                    key = '{};{}'.format(i.attrs.get('from'), i.attrs.get('to'))
                tmp = {}
                if(i.maximumPrecipitations):
                    tmp_list = []
                    for j in i.maximumPrecipitations.findAll('location'):
                        tmp_dict = {}
                        tmp_dict.update(j.attrs)
                        if(j.maximumPrecipitation):
                            tmp_dict.update(j.maximumPrecipitation.attrs)
                        tmp_list.append(tmp_dict)
                    if(tmp_list):
                        tmp.update({i.maximumPrecipitations.name: tmp_list})
                if(i.lowestTemperatures):
                    tmp_list = []
                    for j in i.lowestTemperatures.findAll('location'):
                        tmp_dict = {}
                        tmp_dict.update(j.attrs)
                        if(j.lowestTemperature):
                            tmp_dict.update(j.lowestTemperature.attrs)
                        tmp_list.append(tmp_dict)
                    if(tmp_list):
                        tmp.update({i.lowestTemperatures.name: tmp_list})
                if(i.highestTemperatures):
                    tmp_list = []
                    for j in i.highestTemperatures.findAll('location'):
                        tmp_dict = {}
                        tmp_dict.update(j.attrs)
                        if(j.highestTemperature):
                            tmp_dict.update(j.highestTemperature.attrs)
                        tmp_list.append(tmp_dict)
                    if(tmp_list):
                        tmp.update({i.highestTemperatures.name: tmp_list})
                if(tmp):
                    data.update({key: tmp})
    except Exception as e:
        data = {'error': str(e)}
    return data


def __get_response__(url, dt_2_local, parse):
    '''
        Performs get request and returns parsed response.
    '''
    try:
        resp = get(url, headers={'User-Agent': 'pymetv1.0'})
        if(resp.ok):
            if(parse):
                return __parse_response__(resp.content, dt_2_local)
            return {'response': resp.content.decode('utf-8')}
        raise Exception('received {} from server'.format(resp.status_code))
    except Exception as e:
        return {'error': str(e)}


def fetch(base_url='https://api.met.no/weatherapi/extremeswwc/1.2/', dt_2_local=True, parse=True):
    '''
        Returns the WWC-data for the two last periodes of time in Norway. WWC means Warmest, Wettest and Coldest.
        Date time is by default converted to your local timezone. If you don't want this to happen, set dt_2_local = False, while calling this function.
        If you don't want it to parse XML response to python dict, set parse=False while invoking this function. By default it'll return parsed response as python dict, which might be eventually converted to JSON using json.dumps().
    '''
    return __get_response__(base_url, dt_2_local, parse)


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
