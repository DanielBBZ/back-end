import logging
from logging.handlers import TimedRotatingFileHandler
import pathlib
import os
import sys
from decouple import config
import tweepy

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent.parent

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s —" "%(funcName)s:%(lineno)d — %(message)s"
)

LOG_DIR = PACKAGE_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "api.log"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    console_handler.setLevel(logging.DEBUG)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when="midnight")
    file_handler.setFormatter(FORMATTER)
    file_handler.setLevel(logging.WARNING)
    return file_handler


def get_logger(*, logger_name):
    """
    Get logger with prepared handlers.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SERVER_PORT = 8000
    COLLECTION_STATE = "state"
    COLLECTION_COUNTY = "county"
    COLLECTION_TWITTER = "twitter"
    # JHU CSSE Daily Reports
    BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"
    # JHU CSSE time series reports
    TIME_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
    # Tweepy
    TWITTER_AUTH = tweepy.OAuthHandler(
        config("TWITTER_CONSUMER_KEY"), config("TWITTER_CONSUMER_SECRET_KEY")
    )
    TWITTER_AUTH.set_access_token(
        config("TWITTER_ACCESS_TOKEN"), config("TWITTER_ACCESS_TOKEN_SECRET")
    )
    TWITTER = tweepy.API(TWITTER_AUTH)


class ProductionConfig(Config):
    DEBUG = False
    DB_NAME = "covid"


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    DB_NAME = "covid-staging"