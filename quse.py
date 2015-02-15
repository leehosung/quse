#!/usr/bin/env python
import sys
from misfit import Misfit
from datetime import datetime
from datetime import timedelta
import configparser
from isoweek import Week


class Quse(object):

    def __init__(self, config_file='misfit.cfg'):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.read_config()
        self.misfit = Misfit(
            self.client_id, self.client_secret, self.access_token
        )

    def read_config(self):
        """ Read credentials from the config file """
        with open(self.config_file) as cfg:
            self.config.readfp(cfg)
        self.client_id = self.config.get('misfit', 'client_id')
        self.client_secret = self.config.get('misfit', 'client_secret')
        self.access_token = self.config.get('misfit', 'access_token')

    def get_sleep(self, start_date, end_date):
        return self.misfit.sleep(start_date, end_date)

    def get_oneday_sleep_stat(self, date):
        sleep_session = self.misfit.sleep(date, date)[0]
        details = sleep_session.sleepDetails
        deep_sleep_duration = 0
        for i in range(len(details) - 1):
            if details[i].value == 3:
                diff = details[i + 1].datetime - details[i].datetime
                deep_sleep_duration += diff.seconds
        return (sleep_session.duration, deep_sleep_duration)
    
    def seconds_to_hourform(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)

    def print_weekly_stat(self, year, week):
        week_total_sleep = 0
        week_total_deep_sleep = 0
        for d in  Week(year, week).days():
            (total_sleep_duration, deep_sleep_duration) =\
                self.get_oneday_sleep_stat(d)
            week_total_sleep += total_sleep_duration
            week_total_deep_sleep += deep_sleep_duration
        print("total average sleep : %s" %\
            self.seconds_to_hourform(week_total_sleep/7))
        print("total average deep sleep : %s" %\
            self.seconds_to_hourform(week_total_deep_sleep/7))


if __name__ == "__main__":
    quse = Quse()
    week = int(sys.argv[1])
    quse.print_weekly_stat(2015, week=week)
