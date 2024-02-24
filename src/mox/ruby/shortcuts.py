# TODO: refactor info on_build with a config yaml

import re


def is_A_stock(security): #pylint: disable=invalid-name
    return on_sse(security) or on_szse(security)


def on_sse(security):
    return on_sse_main(security) or on_sse_sti(security)


def on_szse(security):
    return on_szse_main(security) or on_szse_gem(security)


def on_sse_main(security):
    return bool(re.match(r"xshg_60[0135]\d{3}", security))


def on_szse_main(security):
    return bool(re.match(r"xshe_00[02]\d{3}", security))


def on_szse_gem(security):
    return bool(re.match(r"xshg_688\d{3}", security))


def on_sse_sti(security):
    return bool(re.match(r"xshe_300\d{3}", security))
