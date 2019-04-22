import pdb

from Pattern.Counter import Counter
from OandaAPI import OandaAPI


class CounterDbTp(Counter):
    '''
    This class represents a trade showing Counter doubletop pattern (inherits from Counter)

    Class variables
    ---------------

    start: datetime, Required
           Time/date when the trade was taken. i.e. 20-03-2017 08:20:00s
    pair: str, Required
          Currency pair used in the trade. i.e. AUD_USD
    timeframe: str, Required
               Timeframe used for the trade. Possible values are: D,H12,H10,H8,H4
    entry: float, Optional
           entry price
    trend_i: datetime, Required
             start of the trend
    type: str, Optional
          What is the type of the trade (long,short)
    SL:  float, Optional
         Stop/Loss price
    TP:  float, Optional
         Take profit price
    SR:  float, Optional
         Support/Resistance area
    bounce_1st : with tuple (datetime,price) containing the datetime
                 and price for this bounce
    bounce_2nd : with tuple (datetime,price) containing the datetime
                 and price for this bounce
    rsi_1st : bool, Optional
              Is price in overbought/oversold
              area in first peak
    rsi_2nd : bool, Optional
              Is price in overbought/oversold
              area in second peak
    diff : float. Optional
           Variable containing the difference between rsi_1st and rsi_2nd
    valley : int Optional
             Length in number of candles between  bounce_1st and bounce_2nd
    n_rsibounces : int, Optional
                  Number of rsi bounces for trend conducting to 1st bounce
    slope: float, Optional
           Float with the slope of trend conducting to 1st bounce
    '''

    def __init__(self, pair, start, **kwargs):

        self.start = start
        allowed_keys = ['timeframe','entry','period', 'trend_i', 'type', 'SL',
                        'TP', 'SR', 'RR']
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)
        super().__init__(pair)

    def set_1stbounce(self):
        '''
        Function to set bounce_1st (the one that is before the most recent)
        and rsi_1st class attributes

        Returns
        -------
        Nothing
        '''

        pdb.set_trace()
        self.set_bounces(part='openAsk',pips=100)
        if len(self.bounces)<2: raise Exception("Less than 2 bounces were found for this trade")
        self.bounce_1st=self.bounces[-2]
        if self.trend_i>self.bounce_1st[0]:
            raise Exception("Error in the definition of the 1st bounce, it is older than the trend_start")

        # now check rsi for this bounce
        candle = self.clist_period.fetch_by_time(self.bounce_1st[0])

        isonrsi = False

        if candle.rsi >= 70 or candle.rsi <= 30:
            isonrsi = True

        self.rsi_1st = isonrsi

    def set_2ndbounce(self):
        '''
        Function to set bounce_2nd (the one that is the most recent)
        and rsi_2nd class attributes

        Returns
        -------
        Nothing
        '''

        self.bounce_2nd=self.bounces[-1]

        # now check rsi for this bounce
        candle = self.clist_period.fetch_by_time(self.bounce_2nd[0])

        isonrsi = False

        if candle.rsi >= 70 or candle.rsi <= 30:
            isonrsi = True

        self.rsi_2nd = isonrsi

    def init_feats(self):
        '''
        Function to initialise all object features

        Returns
        -------
        It will initialise all object's features
        '''

        self.set_lasttime()
        self.set_entry_onrsi()
        self.set_1stbounce()
        self.set_2ndbounce()
        self.bounces_fromlasttime()
        self.set_diff()
        self.set_valley()

    def init_trend_feats(self):
        '''
        Function to initialize the features for
        trend going from 'trend_i' to 'bounce_1st'

        Returns
        -------
        Nothing
        '''

        c = Counter(
            start=str(self.bounce_1st[0]),
            pair=self.pair,
            timeframe=self.timeframe,
            type=self.type,
            period=1000,
            SR=self.SR,
            SL=self.SL,
            TP=self.TP,
            trend_i=str(self.trend_i))

        c.init_feats()

        self.slope=c.slope
        self.n_rsibounces = c.n_rsibounces
        self.rsibounces_lengths=c.rsibounces_lengths
        self.divergence=c.divergence
        self.length_candles=c.length_candles
        self.length_pips=c.length_pips

    def set_diff(self):
        '''
        Function to calculate the diff between rsi_1st & rsi_2nd

        Returns
        -------
        It will set the 'diff' attribute of the class
        '''

        rsi1st_val = self.clist_period.fetch_by_time(self.bounce_1st[0]).rsi
        rsi2nd_val = self.clist_period.fetch_by_time(self.bounce_2nd[0]).rsi

        self.diff=rsi1st_val-rsi2nd_val

    def set_valley(self):
        '''
        Function to calculate the length of the valley
        between bounce_1st & bounce_2nd

        Returns
        -------
        It will set the 'valley' attribute of the class
        '''

        oanda = OandaAPI(url='https://api-fxtrade.oanda.com/v1/candles?',
                         instrument=self.pair,
                         granularity=self.timeframe,
                         alignmentTimezone='Europe/London',
                         dailyAlignment=22,
                         start=self.bounce_1st[0].isoformat(),
                         end=self.bounce_2nd[0].isoformat())

        candle_list = oanda.fetch_candleset()

        self.valley=len(candle_list)