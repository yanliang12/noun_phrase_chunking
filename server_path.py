##############server_path.py##############

import re
import time
import logging
import argsparser
from flask_restx import *
from flask import *

################

import spacy
nlp = spacy.load("en_core_web_sm")

##############llama2_qa.py##############


ns = Namespace(
	'noun_phrase_chunking', 
	description='Noun Phrase Chunking',
	)

args = argsparser.prepare_args()

##########################

noun_phrase_chunking_parser = ns.parser()
noun_phrase_chunking_parser.add_argument('text', type=str, location='json')

noun_phrase_chunking_inputs = ns.model(
	'spacy', 
		{
			'text': fields.String(example = u"My name is Amy Pai.")
		}
	)

@ns.route('/spacy')
class noun_phrase_chunking_api(Resource):
	def __init__(self, *args, **kwargs):
		super(noun_phrase_chunking_api, self).__init__(*args, **kwargs)
	@ns.expect(noun_phrase_chunking_inputs)
	def post(self):		
		start = time.time()
		try:			
			args = noun_phrase_chunking_parser.parse_args()	

			output = {}
			output['noun_phrase_chunks'] = []

			doc = nlp(args['text'])
			for chunk in doc.noun_chunks:
				output['noun_phrase_chunks'] += [
				{
					'sentence': chunk.sent.text,
					'start': chunk.start_char,
					'end': chunk.end_char,
					'text': chunk.text,
				}]

			output['status'] = 'success'
			output['running_time'] = float(time.time()- start)
			return output, 200
		except Exception as e:
			output = {}
			output['status'] = str(e)
			output['running_time'] = float(time.time()- start)
			return output




##########################

batch_noun_phrase_chunking_parser = ns.parser()
batch_noun_phrase_chunking_parser.add_argument('texts', type=list, location='json')

batch_noun_phrase_chunking_inputs = ns.model(
	'spacy_batch', 
		{
			'texts': fields.List(fields.String(), example = [u"My name is Amy Pai.", u"Hi How are you?"])
		}
	)

@ns.route('/spacy_batch')
class batch_noun_phrase_chunking_api(Resource):
	def __init__(self, *args, **kwargs):
		super(batch_noun_phrase_chunking_api, self).__init__(*args, **kwargs)
	@ns.expect(batch_noun_phrase_chunking_inputs)
	def post(self):		
		start = time.time()
		try:			
			args = batch_noun_phrase_chunking_parser.parse_args()	

			output = {}
			output['noun_phrase_chunks'] = []

			for text in args['texts']:
				doc = nlp(text)
				chunks = []
				for chunk in doc.noun_chunks:
					chunks.append(
					{
						'sentence': chunk.sent.text,
						'start': chunk.start_char,
						'end': chunk.end_char,
						'text': chunk.text,
					})
				output['noun_phrase_chunks'].append(chunks)

			output['status'] = 'success'
			output['running_time'] = float(time.time()- start)
			return output, 200
		except Exception as e:
			output = {}
			output['status'] = str(e)
			output['running_time'] = float(time.time()- start)
			return output


##############server_path.py##############