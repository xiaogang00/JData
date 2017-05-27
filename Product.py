import pandas as pd
import numpy as np

product = pd.read_csv('JData_Product.csv', encoding='GBK')

grouped_a1 = product.groupby(product['a1'])
grouped_a2 = product.groupby(product['a2'])
grouped_a3 = product.groupby(product['a3'])
grouped_cate = product.groupby(product['cate'])
grouped_brand = product.groupby(product['brand'])


group_cate_per_sku = product['sku_id'].groupby(product['cate'])
group_brand_per_sku = product['sku_id'].groupby(product['brand'])
group_sku_a1 = product['sku_id'].groupby(product['a1'])
group_sku_a2 = product['sku_id'].groupby(product['a2'])
group_sku_a3 = product['sku_id'].groupby(product['a3'])

frame = pd.Series(list(map(lambda x, y, z: x + y + z,\
                           product['a1'], product['a2'], product['a3'])))
product['sum'] = frame
print grouped_a3.count()
print group_cate_per_sku.size()
print group_brand_per_sku.size()
print group_sku_a1.size()

