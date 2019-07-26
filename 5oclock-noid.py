#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import math
import numpy
import twitter
import email
import datetime

clock_char='🕔'
target_users=('inferist', 'yamaken37', 'tonets', 'csemitovt')


numpy.random.seed(math.ceil(1000*time.time()) % (2**32))
delay_sec = abs(30*numpy.random.standard_cauchy())
current_sec = time.localtime().tm_sec
today_yday = time.localtime().tm_yday
if delay_sec > current_sec:
    time.sleep(delay_sec-current_sec)
else:
    delay_sec=current_sec
    
api = twitter.Api(
    consumer_key='',
    consumer_secret='',
    access_token_key='',
    access_token_secret='',
    sleep_on_rate_limit=True
)
clock_status = api.PostUpdate(clock_char)
current_time = time.time()

ranking = 1
for target_user in target_users:
    tweets = api.GetUserTimeline(screen_name=target_user, include_rts=False, exclude_replies=True)

    for s in tweets:
        if s.text==clock_char:
            tweet_tm = time.localtime(email.utils.mktime_tz(email.utils.parsedate_tz(s.created_at)))
            if tweet_tm.tm_hour == 16 and tweet_tm.tm_yday == today_yday:
                api.PostUpdate("フライング❣\nm9(^Д^)ﾌﾟｹﾞﾗ", in_reply_to_status_id=s.id, auto_populate_reply_metadata=True)
            elif tweet_tm.tm_yday == today_yday:
                ranking += 1
                api.PostUpdate("敗北 orz\n時間差 {:.2f} 秒".format(
                    ((int(clock_status.id)>>22)-(int(s.id)>>22))/1000.0), in_reply_to_status_id=s.id, auto_populate_reply_metadata=True)
                
true_ojisan_utc_epoch = datetime.datetime.fromtimestamp((clock_status.id >> 22) + 1288834974657) / 1000.0)
true_delay = true_ojisan_utc_epoch - datetime.datetime(tweet_tm.tm_year, tweet_tm.tm_month, tweet_tm.tm_day, 8)

api.PostUpdate("{:d} 人中 ".format(1+len(target_users))+"{:d} 位❣".format(ranking)
               +"\n遅延 {:.2f} 秒".format(true_delay), in_reply_to_status_id=clock_status.id)
