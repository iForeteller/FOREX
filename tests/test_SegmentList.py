from pivotlist  import PivotList
from oanda_api import OandaAPI
from candlelist import CandleList

import pytest
import pdb


@pytest.fixture
def pl_object():
    '''Returns PivotList object'''

    oanda = OandaAPI(url='https://api-fxtrade.oanda.com/v1/candles?',
                     instrument='AUD_USD',
                     granularity='D',
                     alignmentTimezone='Europe/London',
                     dailyAlignment=22)

    oanda.run(start='2019-03-08T22:00:00',
              end='2019-08-09T22:00:00',
              roll=True)

    candle_list = oanda.fetch_candleset()

    cl = CandleList(candle_list, instrument='AUD_USD', type='long')

    pl = cl.get_pivotlist(outfile='test.png', th_up=0.02, th_down=-0.02)

    return pl

def test_merge_segments(pl_object):
    '''Test merge_segments method'''

    slist=pl_object.slist

    slist.merge_segments(outfile="test1.png")
