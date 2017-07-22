#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author - Prakhar Pratyush (er.prakhar2b@gmail.com)
#
#####################################################

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

def check_option(a, option_text):
	while not a.isdigit():
		print('Please enter number corresponding to option :\n')
		a = input(option_text)

	return a

def qa(question, response):

	stage_no = 2

	for i in range(len(question)):

		q = question[i]['text']
		response['stage' + str(stage_no)] = {'Bot Says':[{'message':{'text':q}}]}

		if 'options' in  question[i]:
			option_list = question[i]['options']
			option_text = 'Please input number corresponding to the option. :\n'

			quick_replies = []
			for option_no in range(len(option_list)):
				option_text += option_list[option_no] + ' [' + str(option_no+1) + '] \n'

				quick_replies.append({'content_type':'text', 'title':option_list[option_no].title(), 'payload':option_list[option_no]})

			response['stage' + str(stage_no)]['Bot Says'][0]['message']['quick_replies'] = quick_replies

			print(q)
			a = input(option_text)
			a = check_option(a, option_text)

			a = option_list[int(a)-1]

		else:
			a = input(q + ' :\n')


		if 'conditions' in question[i]:
			a = check_condition(question[i], a)

		response['stage' + str(stage_no)]['User Says'] = [{question[i]['var']:a}]

		stage_no += 1
	return stage_no

def main():

	if len(sys.argv) <= 1:
		raise ValueError('Input file not provided. Please provide input json file')

	input_file = json.loads(open(str(sys.argv[1])).read())
	response = {}

	greetings = input_file['greet']['text']
	print(greetings)

	response['stage1'] = {'Bot Says':[{'message':{'text': greetings}}]}

	stage_no = qa(input_file['questions'], response)

	final_message = input_file['final']['text']
	print(final_message)
	response['stage' + str(stage_no)] = {'Bot Says':[{'message':{'text': final_message}}]}

	with open('output.json', 'w') as f:
		json.dump(response, f, indent = 2)

if __name__ == '__main__':
	main()

