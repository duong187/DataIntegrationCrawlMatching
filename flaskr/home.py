import json
from math import ceil
import functools
#from flask import current_app, g
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


def load_data():
    f_itviec = open("data/Itviec.txt", "r", encoding="utf8")
    itviec = f_itviec.read()
    json_itviec = json.loads(itviec)
    f_itviec.close()
    f_vietnamwork = open(
        "data/vietnamwork_data_hanoi_json.txt", "r", encoding="utf8")
    vietnamwork = f_vietnamwork.read()
    f_vietnamwork.close()
    itviec_last_update_f = open(
        "data/Itviec_lastUpdate.txt", "r", encoding="utf8")
    itviec_last_update = itviec_last_update_f.read()
    itviec_last_update_f.close()
    VietnamWork_last_update_f = open(
        "data/VietnamWork_lastUpdate.txt", "r", encoding="utf8")
    VietnamWork_last_update = VietnamWork_last_update_f.read()
    VietnamWork_last_update_f.close()
    json_vietnamwork = json.loads(vietnamwork)
    all_data = json_itviec + json_vietnamwork

    return {
        "data": all_data,
        "data_count": len(all_data),
        'demo_data_itviec': json_itviec[0],
        'demo_data_vietnamwork': json_vietnamwork[34],
        'last_update': {
            'vietnamwork': VietnamWork_last_update,
            'itviec': itviec_last_update
        }}
