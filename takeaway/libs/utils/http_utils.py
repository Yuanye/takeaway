# -*- coding: utf-8 -*- 

try:
    from httplib import responses  # py2
except ImportError:
    from http.client import responses  # py3

responses[422] = "Unprocessable Entity"
responses[429] = "Too Many Requests" 

_error_codes = [(status_code, status.replace(" ", "-").lower()) for (status_code, status) in responses.iteritems()]
error_codes = dict(_error_codes)

error_codes[422] = "invalid_params"
error_codes[429] = "rate_limit"

if __name__ == "__main__":
    pass
