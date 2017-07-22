#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author - Prakhar Pratyush (er.prakhar2b@gmail.com)
#
######################################################################

import json
import sys

def check_condition(q, a):
	condition_list = q['conditions']
	result = False
	while(1):
		for condition in range(len(condition_list)):
			for inner_condition in range(len(condition_list[condition])):
				inner_result = True
				inner_result = inner_result and getattr(a, condition_list[condition][inner_condition])()
			
			result = result or inner_result

		if not result:
			a = input(q['text_new'] + ' :\n')
		else:
			break

	return a

def check_option(a):
	while not a.isdigit():
		a = input('Please enter number corresponding to option :\n')

	return a

def demo(input_file, user):
	full_name = user['Profile']['first_name'] + ' ' + user['Profile']['last_name']

	if 'demo_greet' in input_file:
		demo_greetings = input_file['demo_greet']['text']
		print(demo_greetings % full_name)

	if 'demo' in input_file:
		row = []
		demo_list = input_file['demo']
		for n in range(len(demo_list)):
			if 'text' in demo_list[n]:
				row.append([ item for item in input(demo_list[n]['text'] + ' :\n').split()])

		matrix = row

		iter_ = int(input_file['demo_final']['list_length'])

		print(" This is the input matrix :")
		for row_no in range(iter_):
			print(matrix[row_no])

		t_mat = [[matrix[j][i] for j in range(3)] for i in range(3)]

		demo_final = input_file['demo_final']['text']
		print(demo_final + ' :')

		for row_no in range(iter_):
			print(t_mat[row_no])


def qa(question, user):
	for i in range(len(question)):

		q = question[i]['text']
		if 'options' in  question[i]:
			option_list = question[i]['options']
			option_text = 'Please input number corresponding to the option. :\n'

			for option_no in range(len(option_list)):
				option_text += option_list[option_no] + ' [' + str(option_no+1) + '] \n'

			print(q)
			a = input(option_text)
			a = check_option(a)
			a = option_list[int(a)-1]  # get original option from option number
		else:
			a = input(q + ' :\n')

		if 'conditions' in question[i]:
			a = check_condition(question[i], a)

		user['Profile'][question[i]['var']] = a

	return user

def main():
	if len(sys.argv) <= 1:
		raise ValueError('Input file not provided. Please provide input json file')

	input_file = json.loads(open(str(sys.argv[1])).read())
	user = {}
	user['Profile'] = {}

	greetings = input_file['greet']['text']
	print(greetings)

	user = qa(input_file['questions'], user)

	final_message = input_file['final']['text']
	print(final_message)

	with open('user.json', 'w') as f:
		json.dump(user, f, indent = 2)


	demo(input_file, user)

if __name__ == '__main__':
	main()
