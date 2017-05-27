# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import  datetime
from datetime import  timedelta
import pickle
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

def product_feature1():
    dump_path = './cache/product_feature1.pkl'
    if os.path.exists(dump_path):
        product = pickle.load(open(dump_path))
    else:
        product = pd.read_csv('JData_Product.csv', encoding='GBK')
        frame = pd.Series(list(map(lambda x, y, z: x + y + z,\
                               product['a1'], product['a2'], product['a3'])))
        product['sum'] = frame
        # 离散化
        a1 = pd.get_dummies(product["a1"], prefix="a1")
        a2 = pd.get_dummies(product["a2"], prefix="a2")
        a3 = pd.get_dummies(product["a3"], prefix="a3")
        product = pd.concat([product[['sku_id', 'cate', 'brand', 'sum']], a1, a2, a3], axis=1)
        pickle.dump(product, open(dump_path, 'w'))
    return product

def user_feature1():
    dump_path = './cache/user_feature1.pkl'
    if os.path.exists(dump_path):
        user = pickle.load(open(dump_path))
    else:
        User = pd.read_csv('JData_User.csv', encoding='GBK')
        # 读取数据
        User['age'] = User['age'].map(convert_age)
        Age_df = pd.get_dummies(User["age"], prefix="age")
        Sex_df = pd.get_dummies(User["sex"], prefix="sex")
        user_lv_df = pd.get_dummies(User["user_lv_cd"], prefix="user_lv_cd")
        user = pd.concat([User['user_id'], Age_df, Sex_df, user_lv_df], axis=1)
        pickle.dump(user, open(dump_path, 'w'))
    return user


def get_action_data(start_date, end_date):
    dump_path = './cache/all_action_%s_%s.pkl' % (start_date, end_date)
    if os.path.exists(dump_path):
        actions = pickle.load(open(dump_path))
    else:
        action1 = pd.read_csv('JData_Action_201602.csv', encoding='GBK')
        action2 = pd.read_csv('JData_Action_201603.csv', encoding='GBK')
        action3 = pd.read_csv('JData_Action_201604.csv', encoding='GBK')
        actions = pd.concat([action1, action2, action3])
        actions = actions[(actions.time >= start_date) & (actions.time < end_date)]
        pickle.dump(actions, open(dump_path, 'w'))
    return actions

def action_feature1(start_date, end_date):
    dump_path = './cache/action_feature1_%s_%s.pkl' % (start_date, end_date)
    if os.path.exists(dump_path):
        actions1 = pickle.load(open(dump_path))
    else:
        actions = get_action_data(start_date, end_date)
        actions = actions[['user_id', 'sku_id', 'type']]
        df = pd.get_dummies(actions["type"], prefix="action_type")
        actions1 = pd.concat([actions, df], axis=1)
        actions1 = actions1.groupby(['user_id', 'sku_id'], as_index=False).sum()
        del actions['type']
        pickle.dump(actions1, open(dump_path, 'w'))
    return actions1


def action_accumulate_feature(start_date, end_date):
    dump_path = './cache/action_accumulate_%s_%s.pkl' % (start_date, end_date)
    if os.path.exists(dump_path):
        actions = pickle.load(open(dump_path))
    else:
        actions = get_action_data(start_date, end_date)
        df = pd.get_dummies(actions['type'], prefix='action')
        actions = pd.concat([actions, df], axis=1)
        # print actions.head()
        actions['weight'] = actions['time'].map(lambda x: datetime.strptime(end_date, '%Y-%m-%d')\
                                                      - datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
        actions['weight'] = actions['weight'].map(lambda x: math.exp(-x.days))
        actions['action_1'] = actions['action_1'] * actions['weight']
        actions['action_2'] = actions['action_2'] * actions['weight']
        actions['action_3'] = actions['action_3'] * actions['weight']
        actions['action_4'] = actions['action_4'] * actions['weights']
        actions['action_5'] = actions['action_5'] * actions['weights']
        actions['action_6'] = actions['action_6'] * actions['weights']
        del actions['model_id']
        del actions['type']
        del actions['time']
        del actions['datetime']
        del actions['weight']
        actions = actions.groupby(['user_id', 'sku_id', 'cate', 'brand'], as_index=False).sum()
        pickle.dump(actions, open(dump_path, 'w'))
    return actions

def get_accumulate_user_feat(start_date, end_date):
    feature = ['user_id', 'user_action_1_ratio', 'user_action_2_ratio', 'user_action_3_ratio',
               'user_action_5_ratio', 'user_action_6_ratio']
    dump_path = './cache/user_feat_accumulate_%s_%s.pkl' % (start_date, end_date)
    if os.path.exists(dump_path):
        actions = pickle.load(open(dump_path))
    else:
        actions = get_action_data(start_date, end_date)
        df = pd.get_dummies(actions['type'], prefix='action')
        actions = pd.concat([actions['user_id'], df], axis=1)
        actions = actions.groupby(['user_id'], as_index=False).sum()
        actions['user_action_1_ratio'] = actions['action_4'] / actions['action_1']
        actions['user_action_2_ratio'] = actions['action_4'] / actions['action_2']
        actions['user_action_3_ratio'] = actions['action_4'] / actions['action_3']
        actions['user_action_5_ratio'] = actions['action_4'] / actions['action_5']
        actions['user_action_6_ratio'] = actions['action_4'] / actions['action_6']
        actions = actions[feature]
        pickle.dump(actions, open(dump_path, 'w'))
    return actions

def get_accumulate_product_feat(start_date, end_date):
    feature = ['sku_id', 'product_action_1_ratio', 'product_action_2_ratio', 'product_action_3_ratio',
               'product_action_5_ratio', 'product_action_6_ratio']
    dump_path = './cache/product_feat_accumulate_%s_%s.pkl' % (start_date, end_date)
    if os.path.exists(dump_path):
        actions = pickle.load(open(dump_path))
    else:
        actions = get_action_data(start_date, end_date)
        df = pd.get_dummies(actions['type'], prefix='action')
        actions = pd.concat([actions['sku_id'], df], axis=1)
        actions = actions.groupby(['sku_id'], as_index=False).sum()
        actions['product_action_1_ratio'] = actions['action_4'] / actions['action_1']
        actions['product_action_2_ratio'] = actions['action_4'] / actions['action_2']
        actions['product_action_3_ratio'] = actions['action_4'] / actions['action_3']
        actions['product_action_5_ratio'] = actions['action_4'] / actions['action_5']
        actions['product_action_6_ratio'] = actions['action_4'] / actions['action_6']
        actions = actions[feature]
        pickle.dump(actions, open(dump_path, 'w'))
    return actions

def get_labels(start_date, end_date):
    dump_path = './cache/labels_%s_%s.pkl' % (start_date, end_date)
    if os.path.exists(dump_path):
        actions = pickle.load(open(dump_path))
    else:
        actions = get_action_data(start_date, end_date)
        actions = actions[actions['type'] == 4]
        actions = actions.groupby(['user_id', 'sku_id'], as_index=False).sum()
        actions['label'] = 1
        actions = actions[['user_id', 'sku_id', 'label']]
        pickle.dump(actions, open(dump_path, 'w'))
    return actions

def comments_features(start_date, end_date):
    dump_path = './cache/comments_feature_%s_%s.pkl' % (start_date, end_date)
    if os.path.exists(dump_path):
        comments = pickle.load(open(dump_path))
    else:
        comments = pd.read_csv('JData_Comment.csv', encoding='GBK')
        comments = comments[(comments.dt >= start_date) & (comments.dt < end_date)]
        df = pd.get_dummies(comments['comment_num'], prefix='comment_num')
        comments = pd.concat([comments, df], axis=1)
        comments = comments[['sku_id', 'has_bad_comment', 'bad_comment_rate', 'comment_num_1', 'comment_num_2', 'comment_num_3',
         'comment_num_4']]
        pickle.dump(comments, open(dump_path, 'w'))
    return comments

def make_test_set(train_start_date, train_end_date):
    start_days = "2016-02-01"
    user = user_feature1()
    product = product_feature1()
    user_acc = get_accumulate_user_feat(start_days, train_end_date)
    product_acc = get_accumulate_product_feat(start_days, train_end_date)
    comment_acc = comments_features(train_start_date, train_end_date)
    actions = None
    for i in (1, 2, 3, 5, 7, 10, 15, 21, 30):
        start_days = datetime.strptime(train_end_date, '%Y-%m-%d') - timedelta(days=i)
        start_days = start_days.strftime('%Y-%m-%d')
        if actions is None:
            actions = action_feature1(start_days, train_end_date)
        else:
            actions = pd.merge(actions, action_feature1(start_days, train_end_date), how='left',
                                   on=['user_id', 'sku_id'])

        actions = pd.merge(actions, user, how='left', on='user_id')
        actions = pd.merge(actions, user_acc, how='left', on='user_id')
        actions = pd.merge(actions, product, how='left', on='sku_id')
        actions = pd.merge(actions, product_acc, how='left', on='sku_id')
        actions = pd.merge(actions, comment_acc, how='left', on='sku_id')
        actions = actions.fillna(0)
        actions = actions[actions['cate'] == 8]

    users = actions[['user_id', 'sku_id']].copy()
    del actions['user_id']
    del actions['sku_id']
    print "make_end"
    return users, actions

def make_train_set(train_start_date, train_end_date, test_start_date, test_end_date, days=30):
    start_days = "2016-02-01"
    user = user_feature1()
    product = product_feature1()
    user_acc = get_accumulate_user_feat(start_days, train_end_date)
    product_acc = get_accumulate_product_feat(start_days, train_end_date)
    comment_acc = comments_features(train_start_date, train_end_date)
    labels = get_labels(test_start_date, test_end_date)
    actions = None
    for i in (1, 2, 3, 5, 7, 10, 15, 21, 30):
        start_days = datetime.strptime(train_end_date, '%Y-%m-%d') - timedelta(days=i)
        start_days = start_days.strftime('%Y-%m-%d')
        if actions is None:
            actions = action_feature1(start_days, train_end_date)
        else:
            actions = pd.merge(actions, action_feature1(start_days, train_end_date), how='left',
                                   on=['user_id', 'sku_id'])
        actions = pd.merge(actions, user, how='left', on='user_id')
        actions = pd.merge(actions, user_acc, how='left', on='user_id')
        actions = pd.merge(actions, product, how='left', on='sku_id')
        actions = pd.merge(actions, product_acc, how='left', on='sku_id')
        actions = pd.merge(actions, comment_acc, how='left', on='sku_id')
        actions = pd.merge(actions, labels, how='left', on=['user_id', 'sku_id'])
        actions = actions.fillna(0)

    users = actions[['user_id', 'sku_id']].copy()
    labels = actions['label'].copy()
    del actions['user_id']
    del actions['sku_id']
    del actions['label']
    print "make_end"
    return users, product, labels

def report(pred, label):

    actions = label
    result = pred

    # 所有用户商品对
    all_user_item_pair = actions['user_id'].map(str) + '-' + actions['sku_id'].map(str)
    all_user_item_pair = np.array(all_user_item_pair)
    # 所有购买用户
    all_user_set = actions['user_id'].unique()

    # 所有品类中预测购买的用户
    all_user_test_set = result['user_id'].unique()
    all_user_test_item_pair = result['user_id'].map(str) + '-' + result['sku_id'].map(str)
    all_user_test_item_pair = np.array(all_user_test_item_pair)

    # 计算所有用户购买评价指标
    pos, neg = 0,0
    for user_id in all_user_test_set:
        if user_id in all_user_set:
            pos += 1
        else:
            neg += 1
    all_user_acc = 1.0 * pos / ( pos + neg)
    all_user_recall = 1.0 * pos / len(all_user_set)
    print '所有用户中预测购买用户的准确率为 ' + str(all_user_acc)
    print '所有用户中预测购买用户的召回率' + str(all_user_recall)

    pos, neg = 0, 0
    for user_item_pair in all_user_test_item_pair:
        if user_item_pair in all_user_item_pair:
            pos += 1
        else:
            neg += 1
    all_item_acc = 1.0 * pos / ( pos + neg)
    all_item_recall = 1.0 * pos / len(all_user_item_pair)
    print '所有用户中预测购买商品的准确率为 ' + str(all_item_acc)
    print '所有用户中预测购买商品的召回率' + str(all_item_recall)
    F11 = 6.0 * all_user_recall * all_user_acc / (5.0 * all_user_recall + all_user_acc)
    F12 = 5.0 * all_item_acc * all_item_recall / (2.0 * all_item_recall + 3 * all_item_acc)
    score = 0.4 * F11 + 0.6 * F12
    print 'F11=' + str(F11)
    print 'F12=' + str(F12)
    print 'score=' + str(score)

if __name__ == '__main__':
    train_start_date = '2016-02-01'
    train_end_date = '2016-03-01'
    test_start_date = '2016-03-01'
    test_end_date = '2016-03-05'
    action_accumulate_feature(train_start_date, train_end_date)