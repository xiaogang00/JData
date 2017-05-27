# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import  datetime
from datetime import  timedelta
import  pickle
import os
import math
import  time

comment_date = ["2016-02-01", "2016-02-08", "2016-02-15", "2016-02-22", "2016-02-29", "2016-03-07", "2016-03-14",
                "2016-03-21", "2016-03-28",
                "2016-04-04", "2016-04-11", "2016-04-15"]

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

if __name__ == '__main__':
    User = pd.read_csv('JData_User.csv', encoding='GBK')
    # 读取数据
    User['age'] = User['age'].map(convert_age)
    print User.head()
    group_age = (User[(User['age'] != 0)]).groupby(User['age'])

    # 处理sex的数据
    group_sex = User.groupby(User['sex'])

    # 用户的等级
    group_user_lv_cd = User.groupby(User['user_lv_cd'])
    # 用户的注册时间
    group_user_reg_tm = User.groupby(User['user_reg_tm'])

    print group_age.size()
    print group_sex.size()
    print group_user_lv_cd.count()
    print group_user_reg_tm.size()