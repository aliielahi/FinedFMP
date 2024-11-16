# -*- coding: utf-8 -*-
"""Llama_3_8b_Unsloth.ipynb

Automatically generated by Colab.

Original file is located at
		https://colab.research.google.com/drive/1xKGYBMYEaSruQjsrGBqYfdZ3w9CRRlvQ

# Finetuning LLaMA-3 8B

task: ONR
optim: LoRa

Table of context:
1. Imports and Installs
2. Utils
3. Data Import
4. Model and Trainer Definisions
5. Training and Testing Process
"""
import sys

PARAMS = dict({

	'train_on': [2015, 2021, 2017, 2018, 2019, 2020, 2016],
	'test_on': [2023, 2022, 2024],

	'epochs': 64,
	'LR': 0.8e-4,

	'Pred_period': sys.argv[1],
	'Zero-Shot': int(sys.argv[2]),
	'Fine_Tune': int(sys.argv[3]),
	"save_dir": sys.argv[4]
	})
RESULTS = []
INSTRUCTION = "Financial reports data for a specefic company for the past four quarters is given in a tab-separated table bellow. \
in the table, K, M, and B means thousands, millions, and billions. predict if the stock price is going up or down at the end of the next quarter, in 3 months. \
Give a one word response with either [UP] or [DOWN]"

"""## Installs and Imports"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install triton
# !pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
# !pip install --no-deps "xformers<0.0.27" "trl<0.9.0" peft accelerate bitsandbytes
# !pip install trl bitsandbytes peft

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install xFormers

from tqdm import tqdm
import random
import os
from sklearn.metrics import mean_squared_error, r2_score
from collections import Counter
import numpy as np
import re
from sklearn.metrics import f1_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import ast
## model

from unsloth import FastLanguageModel
import torch

import pickle
from datasets import Dataset
## training libraries
from trl import SFTTrainer
from transformers import TrainingArguments
from unsloth import is_bfloat16_supported

"""## Utils"""

def extract_float(text):
		match = re.search(r"[-+]?\d*\.\d+", text)
		if match:
				return float(match.group(0))
		else:
				return None

def r4(value):
	if isinstance(value, float):
		# If the input is a single float, round it and format it to 4 decimal places
		return f"{round(value, 3):.3f}"
	else:
		value = list(value)
		return [f"{round(v, 3):.3f}" for v in value]

def evaluate(y_test,y_pred, roundd = False, arrayed = False):
	print(precision_recall_fscore_support(y_test, y_pred))    
	[pp, pn] = list(precision_recall_fscore_support(y_test, y_pred)[0])
	[rp, rn] = list(precision_recall_fscore_support(y_test, y_pred)[1])
	[fp, fn] = list(precision_recall_fscore_support(y_test, y_pred)[2])
	wf1 = f1_score(y_test, y_pred, average = 'weighted')
	acc = accuracy_score(y_test, y_pred)
	mcc = matthews_corrcoef(y_test, y_pred)
	if roundd:
		[pp, pn] = [r4(pp), r4(pn)]
		[rp, rn] = [r4(rp), r4(rn)]
		[fp, fn] = [r4(fp), r4(fn)]
		wf1 = r4(wf1)
		acc = r4(acc)
		mcc = r4(mcc)
	
	
	res =  {'P+-': [pp, pn],\
			'R+-': [rp, rn],\
			'f1s': [fp, fn],\
			'wf1': wf1,\
			'ACC': acc,\
			'MCC': mcc}
	
	if arrayed:
		return [pp, pn, rp, rn, fp, fn, wf1, acc, mcc]
	return res

def np_ratio(arr):
	ar = []
	for i in arr:
		if i == '[UP]':
			ar.append(1)
		else:
			ar.append(0)
	C = Counter(ar)
	return 'Neg: ' + str(C[0]/(C[1]+C[0])) + ' Pos: ' + str(C[1]/(C[1]+C[0])) 

def evaluator(test_data, model):
	generated_output = []
	real_output = []
	FastLanguageModel.for_inference(model) # Enable native 2x faster inference
	for testcases in tqdm(test_data):
		inputs = tokenizer(
		[
		  alpaca_prompt.format(
			  testcases["instruction"], # instruction
			  testcases["input"], # input
			  "", # output - leave this blank for generation!
		  )
		], return_tensors = "pt").to("cuda")

		outputs = model.generate(**inputs, max_new_tokens = 64, use_cache = True)

		outputs = tokenizer.batch_decode(outputs)[0]
		outputs = outputs.split("### Response:")[1]
		if 'up' in outputs.lower() and 'down' in outputs.lower():
			outputs = None
		elif 'up' in outputs.lower():
			outputs = 1.0
		elif 'down' in outputs.lower():
			outputs = 0.0
		else:
			outputs = None

		benchmark = 1.0 if 'up' in testcases["output"].lower() else 0.0

		generated_output.append(outputs)
		real_output.append(benchmark)
	valid_indices = [i for i, output in enumerate(generated_output) if output is not None]
	generated_output_filtered = np.array([generated_output[i] for i in valid_indices])
	real_output_filtered = np.array([real_output[i] for i in valid_indices])
	print('validated generations:', len(generated_output_filtered)/len(test_data))
	res = evaluate(real_output_filtered, generated_output_filtered)
	print('in evaluator', res)
	return res

def get_dataset(target, train_years, test_years, bin_targets = True, dir = './prompts/'):
	train_datas = []
	test_datas = []

	for i in os.listdir(dir):
		if i.split('.')[-1]=='pkl':
			with open(dir+i, 'rb') as f:
				data = pickle.load(f)
				data = [dict(zip(data.keys(), values)) for values in zip(*data.values())]
				
				for i in data:
					target_datum = i['targets_bin'][target] if bin_targets else i['targets'][target]
					target_datum = '[UP]' if target_datum else '[DOWN]'
					datum = {'instruction': INSTRUCTION, 'input': i['prompts'], 'output': target_datum}
					if int(i['dates'].split('-')[0]) in train_years:
						train_datas.append(datum)
					elif int(i['dates'].split('-')[0]) in test_years:
						test_datas.append(datum)
	random.shuffle(train_datas)
	random.shuffle(test_datas)
	return train_datas, Dataset.from_dict({key: [d[key] for d in train_datas] for key in train_datas[0]}),\
		 test_datas, Dataset.from_dict({key: [d[key] for d in test_datas] for key in test_datas[0]})

def logger(res, model = 'LLaMA3-8B'):
	resu = {}
	resu['model'] = model
	for i in res.keys():
		resu[i] = res[i]
	RESULTS.append(resu)

"""## Model"""

max_seq_length = 2048 # Choose any! We auto support RoPE Scaling internally!
dtype = None # torch.float16 #None for 4 bit # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
load_in_4bit = True #True # Use 4bit quantization to reduce memory usage. Can be False.

# 4bit pre quantized models we support for 4x faster downloading + no OOMs.
fourbit_models = [
		"unsloth/mistral-7b-v0.3-bnb-4bit",      # New Mistral v3 2x faster!
		"unsloth/mistral-7b-instruct-v0.3-bnb-4bit",
		"unsloth/llama-3-8b-bnb-4bit",           # Llama-3 15 trillion tokens model 2x faster!
		"unsloth/llama-3-8b-Instruct-bnb-4bit",
		"unsloth/llama-3-70b-bnb-4bit",
		"unsloth/Phi-3-mini-4k-instruct",        # Phi-3 2x faster!
		"unsloth/Phi-3-medium-4k-instruct",
		"unsloth/mistral-7b-bnb-4bit",
		"unsloth/gemma-7b-bnb-4bit",             # Gemma 2.2x faster!
] # More models at https://huggingface.co/unsloth

model, tokenizer = FastLanguageModel.from_pretrained(
		model_name = "unsloth/Meta-Llama-3.1-8B-bnb-4bit", #"unsloth/llama-3-8b-bnb-4bit",
		max_seq_length = max_seq_length,
		dtype = dtype,
		load_in_4bit = load_in_4bit,
		# token = "hf_...", # use one if using gated models like meta-llama/Llama-2-7b-hf
)

model = FastLanguageModel.get_peft_model(
		model,
		r = 16, # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
		target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
											"gate_proj", "up_proj", "down_proj",],
		lora_alpha = 16,
		lora_dropout = 0, # Supports any, but = 0 is optimized
		bias = "none",    # Supports any, but = "none" is optimized
		# [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
		use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
		random_state = 3407,
		use_rslora = False,  # We support rank stabilized LoRA
		loftq_config = None, # And LoftQ
)

"""## Data Import"""

alpaca_prompt = """
### Instruction:
{}

### Input:
{}
Is the stock price going [UP] or [DOWN] 3 months from now?

### Response:
{}"""

EOS_TOKEN = tokenizer.eos_token # Must add EOS_TOKEN

def formatting_prompts_func(examples):
	instructions = examples["instruction"]
	inputs       = examples["input"]
	outputs      = examples["output"]
	texts = []
	for instruction, inps, output in zip(instructions, inputs, outputs):
			# Must add EOS_TOKEN, otherwise your generation will go on forever!
			text = alpaca_prompt.format(instruction, inps, output) + EOS_TOKEN
			texts.append(text)
	return { "text" : texts, }

train_dict, train_dataset, test_dict, test_dataset = \
	get_dataset(target = PARAMS['Pred_period'], train_years = PARAMS['train_on'], test_years=PARAMS['test_on'])
dataset = train_dataset.map(formatting_prompts_func, batched = True,)
print('training data: ', len(train_dict))
print('testing data: ', len(test_dict))
print(len(dataset))
print('n/p ratio for train', np_ratio([i['output'] for i in train_dict]))
print('n/p ratio for train', np_ratio([i['output'] for i in test_dict]))
print(dataset[4]['text'])

"""## Train and Evaluate"""

if PARAMS['Zero-Shot']:
	print('testing zero-shot model ...')
	try:
		res = evaluator(test_dict, model)
		logger(res, model = 'LLaMA3-8B 0-Shot')
		print(res)
	except Exception as e:
		print('error: Zero-Shot test on')
		print(e)

trainer = SFTTrainer(
		model = model,
		tokenizer = tokenizer,
		train_dataset = dataset,
		dataset_text_field = "text",
		max_seq_length = max_seq_length,
		dataset_num_proc = 2,
		packing = False, # Can make training 5x faster for short sequences.
		args = TrainingArguments(
				per_device_train_batch_size = 2,
				gradient_accumulation_steps = 4,
				warmup_steps = 5,
				max_steps = PARAMS['epochs'],
				learning_rate = PARAMS['LR'],
				fp16 = not is_bfloat16_supported(), # True, # if not 4bit
				bf16 = is_bfloat16_supported(), #False, # if not 4 bit
				logging_steps = 1,
				optim = "adamw_8bit",
				weight_decay = 0.02,
				lr_scheduler_type = "linear",
				seed = 3407,
				output_dir = "outputs",
		),
)

if PARAMS['Fine_Tune']:
	trainer_stats = trainer.train()

if PARAMS['Fine_Tune']:
	print('testing fine-tuned model ...')
	# try:
	res = evaluator(test_dict[:200], model)
	logger(res, model = 'LLaMA3-8B')
	# except Exception as e:
	# 	print('error: fine-tuned on.')
	# 	print(e)

for i in RESULTS:
	print(i)
if len(RESULTS) == 0:
	print('Nothing has been done.')

with open(PARAMS['save_dir'], 'w') as file:
	for item in RESULTS:
		file.write(str(item) + '\n')












# %%
