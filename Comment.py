import pandas as pd
import numpy as np

comment = pd.read_csv('JData_Comment.csv', encoding='GBK')

grouped_comment = comment.groupby(comment['comment_num'])
grouped_has_bad_comment = comment.groupby(comment['has_bad_comment'])
grouped_bad_comment_rate = comment.groupby(comment['bad_comment_rate'])

group_sku_number_per_day = comment['sku_id'].groupby(comment['dt'])
group_comment_per_sku = comment['comment_num'].groupby(comment['sku_id'])
group_bad_comment_rate = comment['bad_comment_rate'].groupby(comment['sku_id'])
group_has_bad_sku = comment['sku_id'].groupby(comment['has_bad_comment'])

# print grouped_comment.size()
# print grouped_has_bad_comment.size()
# print grouped_bad_comment_rate.size()
print group_sku_number_per_day.size()
print group_comment_per_sku.size()
print grouped_bad_comment_rate.size()
print group_has_bad_sku.size()


