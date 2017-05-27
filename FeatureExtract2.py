# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import  datetime
from datetime import  timedelta
import pickle
import os
import math


def convert_age(age_str):
    if age_str == u'-1':
        return 0
    elif age_str == u'15岁以下':
        return 1
    elif age_str == u'16-25岁':
        return 2
    elif age_str == u'26-35岁':
        return 3
    elif age_str == u'36-45岁':
        return 4
    elif age_str == u'46-55岁':
        return 5
    elif age_str == u'56岁以上':
        return 6
    else:
        return -1

def product_feature1():
    product = pd.read_csv('JData_Product.csv', encoding='GBK')
    a1 = pd.get_dummies(product["a1"], prefix="a1")
    a2 = pd.get_dummies(product["a2"], prefix="a2")
    a3 = pd.get_dummies(product["a3"], prefix="a3")
    product = pd.concat([product[['sku_id', 'cate', 'brand']], a1, a2, a3], axis=1)
    return product


def user_feature1():
    User = pd.read_csv('JData_User.csv', encoding='GBK')
    User['age'] = User['age'].map(convert_age)
    Age_df = pd.get_dummies(User["age"], prefix="age")
    Sex_df = pd.get_dummies(User["sex"], prefix="sex")
    user_lv_df = pd.get_dummies(User["user_lv_cd"], prefix="user_lv_cd")
    user = pd.concat([User['user_id'], Age_df, Sex_df, user_lv_df], axis=1)
    return user


def get_action_data(start_date, end_date):
    action1 = pd.read_csv('JData_Action_201602.csv', encoding='GBK')
    action2 = pd.read_csv('JData_Action_201603.csv', encoding='GBK')
    action3 = pd.read_csv('JData_Action_201604.csv', encoding='GBK')
    actions = pd.concat([action1, action2, action3])
    actions = actions[(actions.time >= start_date) & (actions.time < end_date)]
    return actions


def action_feature1(start_date, end_date):
    actions = get_action_data(start_date, end_date)
    actions = actions[['user_id', 'sku_id', 'type']]
    df = pd.get_dummies(actions["type"], prefix="action_type")
    actions1 = pd.concat([actions, df], axis=1)
    actions1 = actions1.groupby(['user_id', 'sku_id'], as_index=False).sum()
    actions1 = actions1.drop_duplicates()
    print actions1.head()
    return actions1

def time_action_feature(start_date, end_date):
    action = get_action_data(start_date, end_date)
    action = action[(action['type'] == 6) & (action['model_id'] == 111)]
    print action.head()


if __name__ == '__main__':
    train_start_date = '2016-02-01'
    train_end_date = '2016-03-01'
    # action_feature1(train_start_date, train_end_date)
    time_action_feature(train_start_date, train_end_date)

