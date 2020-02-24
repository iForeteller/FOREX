import pytest
import pdb

from oanda_api import OandaAPI
from candlelist import CandleList
import datetime

def test_CandleList():
    '''
    Test the creation of a CandleList object

    '''
    # time must be in a valid datetime format
    oanda=OandaAPI(instrument='AUD_USD',
                   granularity='D',
                   settingf='data/settings.ini')

    oanda.run(start='2015-01-25T22:00:00',
             end='2015-01-26T22:00:00')

    candle_list=oanda.fetch_candleset()

    cl=CandleList(candle_list,
                  settingf='data/settings.ini',
                  type='long')

    one_c=cl.next()
    assert one_c.highBid == 0.79329
    assert one_c.openBid == 0.7873
    assert one_c.lowBid == 0.7857
    assert one_c.representation == 'bidask'
    assert one_c.lowAsk == 0.786
    assert one_c.complete is True
    assert one_c.openAsk == 0.7889
    assert one_c.highAsk == 0.79347
    assert one_c.highBid == 0.79329
    assert one_c.volume == 12619
    assert one_c.closeBid == 0.79204
    assert one_c.closeAsk == 0.79258
    assert one_c.openBid == 0.7873

def test_calc_rsi():

    oanda = OandaAPI(instrument='AUD_USD',
                     granularity='D',
                     settingf='data/settings.ini')

    oanda.run(start='2015-01-20T22:00:00',
              end='2015-01-29T22:00:00')

    candle_list = oanda.fetch_candleset()

    cl = CandleList(candle_list,
                    instrument='AUD_USD',
                    granularity='D',
                    settingf='data/settings.ini')

    cl.calc_rsi()

    assert cl.clist[4].rsi == 29.756531523276152

def test_rsibounces():


    oanda = OandaAPI(instrument='CAD_JPY',
                     granularity='D',
                     settingf='data/settings.ini')

    oanda.run(start='2012-01-31T23:00:00',
              end='2012-03-23T23:00:00')

    candle_list = oanda.fetch_candleset()

    cl = CandleList(candle_list,
                    instrument='CAD_JPY',
                    granularity='D',
                    settingf='data/settings.ini')

    cl.calc_rsi()
    dict1 = cl.calc_rsi_bounces()

    dict2 = {'number': 0,
             'lengths': []}

    assert dict1 == dict2

def test_get_length_functions():
    '''
    This test check the functions for getting the length of
    the CandleList in number of pips and candles
    '''

    oanda = OandaAPI(instrument='USD_CAD',
                     granularity='D',
                     settingf='data/settings.ini')

    oanda.run(start='2018-02-01T23:00:00',
              end='2018-03-12T23:00:00')

    candle_list = oanda.fetch_candleset()

    cl = CandleList(candle_list,
                    instrument='USD_CAD',
                    granularity='D',
                    settingf='data/settings.ini')

    assert cl.get_length_candles() == 28
    assert cl.get_length_pips() == 532

def test_fit_reg_line():

    oanda = OandaAPI(instrument='EUR_AUD',
                     granularity='D',
                     settingf='data/settings.ini')

    oanda.run(start='2016-05-23T23:00:00',
              end='2016-07-19T23:00:00')

    candle_list = oanda.fetch_candleset()

    cl = CandleList(candle_list,
                    instrument='AUD_USD',
                    granularity='D',
                    settingf='data/settings.ini')

    (fitted_model, regression_model_mse) = cl.fit_reg_line()

    assert regression_model_mse==5.70224448953761e-06

def test_fetch_by_time():

    oanda = OandaAPI(instrument='EUR_AUD',
                     granularity='D',
                     settingf='data/settings.ini')

    oanda.run(start='2016-05-23T23:00:00',
              end='2016-07-19T23:00:00')

    candle_list = oanda.fetch_candleset()

    cl = CandleList(candle_list,
                    instrument='AUD_USD',
                    granularity='D',
                    settingf='data/settings.ini')

    adatetime = datetime.datetime(2016, 6, 1, 22, 0)

    c=cl.fetch_by_time(adatetime)

    assert c.openAsk == 1.54196
    assert c.highAsk == 1.55438

def test_slice_with_start():

    oanda = OandaAPI(instrument='EUR_AUD',
                     granularity='D',
                     settingf='data/settings.ini')

    oanda.run(start='2016-05-23T23:00:00',
              end='2016-07-19T23:00:00')

    candle_list = oanda.fetch_candleset()

    cl = CandleList(candle_list,
                    instrument='EUR_AUD',
                    granularity='D',
                    settingf='data/settings.ini')

    adatetime = datetime.datetime(2016, 6, 19, 22, 0)

    new_cl=cl.slice(start=adatetime)

    assert len(new_cl.clist) == 22

def test_slice_with_start_end():

    oanda = OandaAPI(instrument='AUD_USD',
                     granularity='D',
                     settingf='data/settings.ini')

    oanda.run(start='2016-05-23T23:00:00',
              end='2016-07-19T23:00:00')

    candle_list = oanda.fetch_candleset()

    cl = CandleList(candle_list,
                    instrument='AUD_USD',
                    granularity='D',
                    settingf='data/settings.ini')

    startdatetime = datetime.datetime(2016, 6, 20, 22, 0)
    endatetime = datetime.datetime(2016, 7, 1, 22, 0)

    cl.slice(start=startdatetime,
             end=endatetime)

    assert len(cl.clist) == 42

def test_get_pivots():

    oanda = OandaAPI(instrument='AUD_USD',
                     granularity='D',
                     settingf='data/settings.ini')

    oanda.run(start='2016-05-23T23:00:00',
              end='2016-07-19T23:00:00')

    candle_list = oanda.fetch_candleset()

    cl = CandleList(candle_list,
                    instrument='AUD_USD',
                    granularity='D',
                    settingf='data/settings.ini')

    pivots = cl.get_pivotlist()
    assert pivots.plist[0].type == -1


"""
def test_check_if_divergence():

    oanda = OandaAPI(instrument='EUR_AUD',
                     granularity='D',
                     settingf='data/settings.ini')

    oanda.run(start='2016-05-23T23:00:00',
              end='2016-07-19T23:00:00')

    candle_list = oanda.fetch_candleset()

    cl = CandleList(candle_list,
                    instrument='CAD_JPY',
                    granularity='D',
                    settingf='data/settings.ini')

    cl.calc_rsi()

    (model, outfile) = cl.fit_reg_line()

    direction = None
    if model.coef_[0, 0] > 0:
        direction = 'up'
    else:
        direction = 'down'

    assert cl.check_if_divergence(direction=direction) == True

def get_dictionary(k, v):
    d = dict([x, ord(x)] for x in  string.printable)
    d[k] = v
    return d

def test_calc_binary_seq(oanda_object):
    
    candle_list=oanda_object.fetch_candleset()

    cl=CandleList(candle_list, type='short')

    cl.calc_binary_seq(merge=False)
    dict1=cl.seq
    dict2={'open': '01', 'colour': '011', 'high': '01', 'close': '11', 'low': '11'}

    shared_items = set(dict1.items()) & set(dict2.items())

    assert len(shared_items) == 5

def test_calc_binary_seq_withmerge(oanda_object):
    '''
    Test the calc_binary_seq function with the merge=True option
    '''

    candle_list=oanda_object.fetch_candleset()

    cl=CandleList(candle_list, type='short')

    cl.calc_binary_seq(merge=True)
    dict1=cl.seq
    dict2={'close': '11', 'colour': '011', 'merge': '01110111011', 'open': '01', 'high': '01', 'low': '11'}

    shared_items = set(dict1.items()) & set(dict2.items())

    assert len(shared_items) == 6

def test_number_of_0s(oanda_object):
  
    candle_list=oanda_object.fetch_candleset()
    
    cl=CandleList(candle_list, type='short')

    cl.calc_binary_seq()

    cl.calc_number_of_0s(norm=True)

    dict1=cl.number_of_0s
    dict2={'open': 0.5, 'close': 0.0, 'colour': 0.3333333333333333, 'low': 0.0, 'high': 0.5, 'merge':0.2727272727272727}

    shared_items = set(dict1.items()) & set(dict2.items())

    assert len(shared_items) == 6

def test_calc_number_of_doubles0s(oanda_object):
    
    candle_list=oanda_object.fetch_candleset()

    cl=CandleList(candle_list, type='short')

    cl.calc_binary_seq()

    cl.calc_number_of_doubles0s(norm=True)

    assert cl.highlow_double0s==0.0
    assert cl.openclose_double0s==0.0

def test_longest_stretch(oanda_object):

    candle_list=oanda_object.fetch_candleset()

    cl=CandleList(candle_list, type='short')

    cl.calc_binary_seq()

    cl.calc_longest_stretch()

    dict1=cl.longest_stretch
    dict2={'close': 0, 'high': 0, 'open': 0, 'low': 0, 'colour': 0}

    shared_items = set(dict1.items()) & set(dict2.items())

    assert len(shared_items) == 5

def test_get_entropy(oanda_object):
    
    candle_list=oanda_object.fetch_candleset()

    cl=CandleList(candle_list, type='short')

    cl.calc_binary_seq()

    cl.get_entropy()

    dict1=cl.entropy
    dict2={'open': 0.34657359027997264, 'colour': 0.21217138943160427, 'high': 0.34657359027997264, 'close': 0.0, 'low': 0.0}

    shared_items = set(dict1.items()) & set(dict2.items())

    assert len(shared_items) == 5

def test_check_if_divergence():

    oanda = OandaAPI(url='https://api-fxtrade.oanda.com/v1/candles?',
                     instrument='EUR_AUD',
                     granularity='D',
                     alignmentTimezone='Europe/London',
                     dailyAlignment=22,
                     start='2016-05-23T23:00:00',
                     end='2016-07-19T23:00:00')

    candle_list = oanda.fetch_candleset()

    cl = CandleList(candle_list, instrument='CAD_JPY', granularity='D')

    cl.calc_rsi(period=1000)

    (model,outfile)=cl.fit_reg_line()

    direction=None
    if model.coef_[0, 0]>0:
        direction='up'
    else:
        direction='down'

    assert cl.check_if_divergence(direction=direction)==True

"""
