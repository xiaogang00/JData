import pandas as pd
import numpy as np 

Action1 = pd.read_csv('JData_Action_201602.csv', encoding='GBK')
Action2 = pd.read_csv('JData_Action_201603.csv', encoding='GBK')
Action3 = pd.read_csv('JData_Action_201604.csv', encoding='GBK')

Action1.append(Action2).append(Action3)
grouped_model = Action1.groupby(Action1['model_id'])
grouped_brand = Action1.groupby(Action1['brand'])
grouped_type = Action1.groupby(Action1['type'])
grouped_cate = Action1.groupby(Action1['cate'])

group_user = Action1['sku_id'].groupby(Action1['user_id'])
print group_user.size()

#str_data = (Action1['time'].str.split(' ')[0])[0]
#str_select = ("".join(str_data)).split('-')
#print str_select

group = Action1[Action1['time'] < '2016-04-15'].groupby(Action1['model_id'])

print grouped_brand.size(), grouped_cate.size(), grouped_type.size()
print grouped_model.size()

