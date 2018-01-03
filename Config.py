import logging


# Config for logger
class Config:
    base_url = "wss://api.bale.ai/v1/bots/"
    request_timeout = 5

    use_graylog = False
    graylog_host = "127.0.01"
    graylog_port = 12201
    log_level = logging.DEBUG  # DEBUG | INFO | ERROR | WARNING | CRITICAL
    log_facility_name = "python_bale_bot"
    source = "bot_name"
