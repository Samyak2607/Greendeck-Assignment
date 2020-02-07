from flask import Flask, request, jsonify
# from NAP_retailer import *
import pandas as pd
import numpy as np

df = pd.read_csv('nap_retailer.csv')
# print(df.discount_price.head())
discount_grp_by_brand = pd.read_csv('discount_nap_retailer.csv')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return '<h1>This is Samyak Jain</h1> <br><h3>Greendeck Assignment</h3>'

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

def discount_greater_than():
	if request.method == 'POST':
		req_json = request.json
		op1 = req_json['operand1']
		op2 = req_json['operand2']
		op = req_json['operator']
		# return jsonify({'response':str(op1)+str(op2)+str(op)})
		
		return jsonify({'response':response})
		if op == '<':
			response = list(df.loc[df[op1] < op2]['_id'])
			return jsonify({'response':response})
		elif op == '>':
			response = list(df.loc[df[op1] > op2]['_id'])
			return jsonify({'response':response})
		else:
			response = list(df.loc[df[op1] == op2]['_id'])
			return jsonify({'response':response})


@app.route('/product_count', methods=['POST'])

def product_count():
	if request.method == 'POST':
		req_json = request.json
		op1 = req_json['operand1']
		op2 = req_json['operand2']
		op = req_json['operator']
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
		elif op1 == 'brand' and op == '==':
			brand_count = df['brand'].value_counts()
			product_count = int(brand_count[op2])
			avg_discount = df.groupby('brand')['discount_price'].mean()[op2]
			return jsonify({'discounted_products_count':product_count, 'avg_discount':avg_discount})	
		else:
			return jsonify({'response':'Invalid Operands or operator selected'})

@app.route('/expensive', methods=['POST'])

def expensive():
	if request.method == 'POST':
		req_json = request.json
		op1 = req_json['operand1']
		if op1 == 'expensive_list':
			expensive_list = list(df.loc[df['expensive_id'] != '[0]']['expensive_id'])
			return jsonify({'expensive_list':expensive_list})
		op2 = req_json['operand2']
		op = req_json['operator']

		if op1 == 'brand':
			expensive_list = df.loc[df['brand'] == op2 ]
			expensive_list = list(expensive_list.loc[df['expensive_id'] != '[0]']['expensive_id'])
			return jsonify({'expensive_list':expensive_list})
		else:
			return jsonify({'response':'Invalid Operands or operator selected'})

# def 

if __name__ == '__main__':
	app.run(debug=False)