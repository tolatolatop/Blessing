#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/7 5:44
# @Author  : tolatolatop
# @File    : common.py
import pathlib
import re
import tarfile

import requests as rq
import pandas as pd
from django.conf import settings
from sqlalchemy import create_engine


def get_db():
    db_type = settings.DATABASES['default']['ENGINE']
    db_info = settings.DATABASES['default']['NAME']
    return create_engine(db_info)


def get_jenkins_log(url):
    resp = rq.get(url)
    return resp.text


def get_task_info(url):
    resp = rq.get(url)
    params = resp.json()
    return params


def catch_ftp_url_from_jenkins_log(log_text):
    regex = ""
    data = re.search(regex, log_text)
    if data:
        return data.group()
    else:
        raise ValueError("no found %s in %s" % (regex, log_text.replace("\n", "\\n")))


def download_from_ftp(url):
    file_path = pathlib.Path(".")
    return file_path


def un_tar_report(tar_path):
    tarfile.open(tar_path, 'r')
    output_path = pathlib.Path(".")
    return output_path


def load_data_from_excel_report(excel_dir: pathlib.Path, glob_regex):
    df = pd.DataFrame()
    for excel_path in excel_dir.glob(glob_regex):
        pass
    return df


def clean_data(data_frame: pd.DataFrame, task_name, ):
    data_frame = data_frame.drop_duplicates()
    return data_frame


def get_owner_info(file_path: pathlib.Path):
    data = pd.read_csv(file_path)
    return data


def set_owner_info(data_frame: pd.DataFrame, owner_info):
    data_frame = data_frame.merge(owner_info, on="data")
    return data_frame


def set_order_info(data_frame: pd.DataFrame):
    data_frame = data_frame
    return data_frame


def submit_data(data_frame: pd.DataFrame, task_info):
    db = get_db()
    db_table = task_info['table']
    data_frame.to_sql(db_table, db, if_exists='append')
    return data_frame


def load_report_data_from_jenkins(jenkins_url):
    ftp_url = get_jenkins_log(jenkins_url)
    tar_path = download_from_ftp(ftp_url)
    report_path = un_tar_report(tar_path)
    task_info = get_task_info(jenkins_url)
    owner_info = get_owner_info(task_info["owner_info"])

    for task in task_info:
        report_data = load_data_from_excel_report(report_path, task["report_name"])
        report_data = clean_data(report_data, task["name"])
        report_data = set_owner_info(report_data, owner_info)
        report_data = set_order_info(report_data)
        submit_data(report_data, task)
    return True
