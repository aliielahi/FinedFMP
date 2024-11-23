# FinedFMP

### FewShot/Fine-tuned Financial Movement Prediction Models

GPUSetUp/Command.txt and GPUSetUp/run_commands.sh
In the commands.txt files, you see a list of packages to install the necessary packages, and a few eamples how to run the llamaft.py code to finetune the llama3.1 8B Instruct model. run_commands.sh runs all of the lines on the command.txt file if you are using a GPU remotely.
to make run_commands.sh executable: chmod +x ./run_commands.sh

LLM Few-Shot/*
Few shot learning language models such as LLaMA and GPT for the stock movement classification task.

LLM FT/*
The jupyter notebook version for llama fine-tuneing is for experimental changes to the model or data.
The .py versions are supposed to be uploaded to the GPU environment to run the experiments selected.
look at the commands.txt files to see what arguments do the llamaft.py gets from command line to run the code. example:
python llamaft.py 3m 0 1 './3m.txt'
python llamaft.py <Prediction period can be 1d, 10d, 1m, 3m, 6m> <Few-shot 0 or 1> <Fine Tune 0 or 1> <Path to save the results> 

DataProcessor/*
All necessary code to generate promps.

IEEE-BigData paper's dataset: [link](https://drive.google.com/file/d/1NJc2ynah5JFx53c1t9pTo2TY_KGCcoBp/view?usp=sharing)
  This is the first verrsion of the dataset. It data from contains 20 companies, from 2022-2024.

The *Latest version* dataset for this project can be find on: [Link](https://drive.google.com/file/d/1SL_fTu0AYSc3iSkRtSy4rIdOFn3Cja7k/view) 
  This dataset contains news data, Financial report (tables) data, historical price data, for more than 100 (high trading volum) companies from 2014-2024.
  List of news websites: WSJ, NYT and a few other sources. Also, CMIN dataset's news are attached to this dataset.
