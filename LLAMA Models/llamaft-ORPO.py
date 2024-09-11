PARAMS = dict({

	'train_on': [2015, 2021, 2017, 2018, 2019, 2020, 2016],
	'test_on': [2023, 2022, 2024],

	'epochs': 60,
	'LR': 0.5e-4,

	'Pred_period': '3m',
	'Zero-Shot': 0,
	'Fine_Tune': 1,
	"save_dir": './3m.txt'
	})
RESULTS = []
INSTRUCTION = "Financial reports data for a specefic company for the past four quarters is given in a tab-separated table bellow. \
in the table, K, M, and B means thousands, millions, and billions. predict if the stock price is going up or down at the end of the next quarter, in 3 months. \
Give a one word response with either [UP] or [DOWN]"
QU = "Based on the information answer with single word, Will the Stock Price gp UP or DOWN? Response:\n"
# import replicate
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

import pickle

from huggingface_hub import login
login(token='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')


import wandb

wb_token = '8eb7abb25a804ca9caaa71178f6ddfdc2f856866'
wandb.login(key=wb_token)

import pickle
import pandas as pd
from datasets import Dataset
import gc
import os
import torch
from datasets import load_dataset
from peft import LoraConfig, PeftModel, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import BitsAndBytesConfig, TrainingArguments, pipeline
from trl import ORPOConfig, ORPOTrainer, setup_chat_format

base_model = "meta-llama/Meta-Llama-3.1-8B-Instruct"
new_model = "FinLLaMA-3-8B"

# Set torch dtype and attention implementation
if torch.cuda.get_device_capability()[0] >= 8:
    torch_dtype = torch.bfloat16
    attn_implementation = "eager" #"flash_attention_2" flash should be used but
	                              #      I cannot install it on A100
else:
    torch_dtype = torch.float16
    attn_implementation = "eager"
# QLoRA config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch_dtype,
    bnb_4bit_use_double_quant=True,
)

# LoRA config
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=['up_proj', 'down_proj', 'gate_proj', 'k_proj', 'q_proj', 'v_proj', 'o_proj']
)

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(base_model)

# Load model
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    quantization_config=bnb_config,
    device_map="auto",
	attn_implementation = attn_implementation
)
model, tokenizer = setup_chat_format(model, tokenizer)
model = prepare_model_for_kbit_training(model)


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

def evaluator(model, tokenizer, test_data):
    generated_output = []
    real_output = []
    for i in tqdm(test_data):
        ins = i['prompt']
        print('prompting with:', ins[:20])
        inputs = tokenizer(ins, return_tensors="pt").to(model.device)
        output = model.generate(
            inputs["input_ids"],
            max_new_tokens=10,      # Set the maximum length of the generated text
            num_return_sequences=1,  # Number of generated sequences
            temperature=0.65,     # Controls randomness: lower values for more deterministic output
            top_k=50,            # Consider the top-k probable next tokens
            top_p=0.9,           # Use nucleus sampling (top-p sampling)
            repetition_penalty=1.2  # Penalize repetition of tokens
        )
        output = tokenizer.decode(output[0], skip_special_tokens=True)
        print('output: ', output[-20:])
        output = output.split('Response:')[-1].strip()
        if 'up' in output.lower() and 'down' in output.lower():
            out_bin = None
        elif 'up' in output.lower():
            out_bin = 1.0
        elif 'down' in output.lower():
            out_bin = 0.0
        else:
            out_bin = None

        benchmark = 1.0 if 'up' in i["output"].lower() else 0.0
        print(output, '\nexpected: ', benchmark, out_bin)
        generated_output.append(out_bin)
        real_output.append(benchmark)

    valid_indices = [i for i, output in enumerate(generated_output) if output is not None]
    generated_output_filtered = np.array([generated_output[i] for i in valid_indices])
    real_output_filtered = np.array([real_output[i] for i in valid_indices])
    print('validated generations:', len(generated_output_filtered)/len(test_data))
    print(real_output_filtered, generated_output_filtered)
    res = evaluate(real_output_filtered, generated_output_filtered)
    print('in evaluator', res)
    return res, (real_output_filtered, generated_output_filtered)

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
	return train_datas, test_datas

def logger(res, model = 'LLaMA3-8B'):
	resu = {}
	resu['model'] = model
	for i in res.keys():
		resu[i] = res[i]
	RESULTS.append(resu)

def op(s): 
  return '[UP]' if s == '[DOWN]' else '[DOWN]'

def format_chat_template(row):
    row["chosen"] = tokenizer.apply_chat_template(row["chosen"], tokenize=False)
    row["rejected"] = tokenizer.apply_chat_template(row["rejected"], tokenize=False)
    return row

def get_data_orpo(train_dict):
    ds_chat = [{'chosen': [{'content': INSTRUCTION+'\n'+i['input']+QU, 'role': 'user'}, {'content': i['output'], 'role': 'assistant'}], 
                'rejected': [{'content': INSTRUCTION+'\n'+i['input']+QU, 'role': 'user'}, {'content': op(i['output']), 'role': 'assistant'}], 
                'prompt': INSTRUCTION+'\n'+i['input']+QU, 'output': i['output']} for i in train_dict]

    dataset = Dataset.from_dict({key: [d[key] for d in ds_chat] for key in ds_chat[0]})

    dataset = dataset.map(
        format_chat_template,
        num_proc= os.cpu_count(),
    )
    return dataset

train_dict, test_dict = \
	get_dataset(target = PARAMS['Pred_period'], train_years = PARAMS['train_on'], test_years=PARAMS['test_on'])

dataset = get_data_orpo(train_dict)
dataset_test = get_data_orpo(test_dict[:10])
dataset_tes_tot = get_data_orpo(test_dict)

orpo_args = ORPOConfig(
    learning_rate=8e-6,
    lr_scheduler_type="linear",
    max_length=1024,
    max_prompt_length=512,
    beta=0.1,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    gradient_accumulation_steps=4,
    optim="paged_adamw_8bit",
    num_train_epochs=0.0786,
	max_steps=80,
    evaluation_strategy="steps",
    eval_steps=0.2,
    logging_steps=1,
    warmup_steps=10,
    report_to="wandb",
    output_dir="./results/",
)

trainer = ORPOTrainer(
    model=model,
    args=orpo_args,
    train_dataset=dataset,
    eval_dataset=dataset_test,
    peft_config=peft_config,
    tokenizer=tokenizer,
)

trainer.train()

print('saving the model')
trainer.save_model(new_model)

print('saving the model')
res, (real_output_filtered, generated_output_filtered) = evaluator(model,tokenizer, dataset_tes_tot)
print(res, (real_output_filtered, generated_output_filtered))
