from flask import Flask, request, jsonify, send_from_directory
# from NAP_retailer import *
import pandas as pd
import numpy as np
import os

df = pd.read_csv('nap_retailer.csv')
# df['basket_fluctuation_price'] = df['basket_fluctuation_price']*100
# print(df.discount_price.head())
# discount_grp_by_brand = pd.read_csv('discount_nap_retailer.csv')
# print(df['basket_fluctuation_price'].head())

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	return '<h1>This is Samyak Jain</h1> <br><h3>Greendeck Assignment</h3>'

@app.route('/favicon.ico', methods=['GET', 'POST'])
def dummy():
	# print('dummy endpoint called')
	return send_from_directory(os.path.join(app.root_path, ''), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/query', methods=['POST'])
def query():
	if request.method == 'POST':
		req = request.json
		query_type = req['query_type']
		if 'filters' in req.keys():
			filters = req['filters']
		if query_type == 'discounted_products_list':
			return discounted_products_list(filters[0])
		elif query_type == 'discounted_products_count|avg_discount':
			return discounted_products_count(filters[0])
		elif query_type == 'expensive_list':
			if 'filters' in req.keys():
				return expensive(filters[0])
			else:
				return expensive1()
		elif query_type == 'competition_discount_diff_list':
			return website_result(filters)
		else:
			return jsonify({'response':'Invalid query_type'})




@app.route('/test', methods=['GET', 'POST'])
def test():
	if request.method == 'GET':
		return jsonify({'response':'Get request called by test'})
	elif request.method == 'POST':
		req_json = request.json
		name = req_json['name']
		return jsonify({'response':'Hey '+name})

# Question 1
# NAP products where discount is greater than n%
@app.route('/discount_greater_than', methods=['POST'])

def discounted_products_list(filters):
	op1 = filters['operand1']
	op2 = filters['operand2']
	op = filters['operator']
	if op == '<':
		response = list(df.loc[df['discount_price'] < op2]['_id'].unique())
		return jsonify({'discounted_products_list':response})
	elif op == '>':
		response = list(df.loc[df['discount_price'] > op2]['_id'].unique())
		return jsonify({'discounted_products_list':response})
	else:
		response = list(df.loc[df['discount_price'] == op2]['_id'].unique())
		return jsonify({'discounted_products_list':response})


@app.route('/product_count', methods=['POST'])

def discounted_products_count(filters):
	op1 = filters['operand1']
	op2 = filters['operand2']
	op = filters['operator']

	# return jsonify({'discounted_products_count':product_count, 'avg_dicount': product_avg})

	if op1 == 'discount' and op == '>':
		product = df.loc[df['discount_price'] > op2]
		product_avg = product['discount_price'].mean()
		product_count = len(product.index)
		return jsonify({'discounted_products_count':product_count, 'avg_discount': product_avg})
	elif op1 == 'discount' and op == '<':
		product = df.loc[df['discount_price'] < op2]
		product_avg = product['discount_price'].mean()
		product_count = len(product.index)
		return jsonify({'discounted_products_count':product_count, 'avg_discount': product_avg})
	elif op1 == 'discount':
		product = df.loc[df['discount_price'] == op2]
		product_avg = product['discount_price'].mean()
		product_count = len(product.index)
		return jsonify({'discounted_products_count':product_count, 'avg_discount': product_avg})
	elif op1 == 'brand.name' and op == '==':
		brand_count = df['brand'].value_counts()
		product_count = int(brand_count[op2])
		avg_discount = df.groupby('brand')['discount_price'].mean()[op2]
		return jsonify({'discounted_products_count':product_count, 'avg_discount':avg_discount})	
	else:
		return jsonify({'response':'Invalid Operands or operator selected'})

@app.route('/expensive', methods=['POST'])

def expensive1():
	exp_list = list(df.loc[df['expensive_id'] != '[0]']['expensive_id'])
	return jsonify({'expensive_list':exp_list})

def expensive(filters):
	op1 = filters['operand1']
	op2 = filters['operand2']
	op = filters['operator']

	if op1 == 'brand.name':
		expensive_list = df.loc[df['brand'] == op2 ]
		expensive_list = list(expensive_list.loc[df['expensive_id'] != '[0]']['expensive_id'])
		return jsonify({'expensive_list':expensive_list})
	else:
		return jsonify({'response':'Invalid Operands or operator selected'})

@app.route('/website_result', methods=['POST'])

def website_result(filters):
	
	op1_q1 = filters[0]['operand1']
	op1_q2 = filters[1]['operand1']
	op2_q1 = filters[0]['operand2']
	op2_q2 = filters[1]['operand2']
	op = filters[0]['operator']
	# op = req_json['operator']

	if op == '>':
		competition_df = df.loc[df['basket_fluctuation_price'] > op2_q1]
		competition_list =  list(competition_df.loc[df['comp_website_id'] == op2_q2]['_id'].unique())
		
		return jsonify({'competition_discount_diff_list':competition_list})

	elif op == '<':
		competition_df = df.loc[df['basket_fluctuation_price'] < op2_q1]
		competition_list =  list(competition_df.loc[df['comp_website_id'] == op2_q2]['_id'].unique())
		
		return jsonify({'competition_discount_diff_list':competition_list})

	elif op == '==':
		competition_df = df.loc[df['basket_fluctuation_price'] == op2_q1]
		competition_list =  list(competition_df.loc[df['comp_website_id'] == op2_q2]['_id'].unique())
		
		return jsonify({'competition_discount_diff_list':competition_list})

	else:
		return jsonify({'response':'Invalid Operands or operator selected'})

if __name__ == '__main__':
	app.run(debug = True)