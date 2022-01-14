.PHONY: clean data lint requirements
#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = new-clients-probability
INTERPRETER = python
PROJECT_TYPE = model

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Set up Python or R environment
create_environment:
ifeq (True,$(HAS_CONDA))
	@echo ">>> Detected conda, creating environment."
ifeq (python,$(findstring python,$(INTERPRETER)))
ifeq (,$(wildcard ./environment.yml))
	@echo "name: $(PROJECT_NAME)\nchannels:\n    - conda-forge\n    - anaconda\ndependencies:\n    - python=3\n    - ipykernel\n    - jupyter\n    - pip\n    - pip:\n        - -r requirements.txt" > environment.yml
else
	@echo ">>> Environment file already exists"
	mkdir data/
	mkdir data/processed
	mkdir data/raw
endif
	conda env create -f environment.yml
	
ifeq (data_analysis,$(findstring data_analysis, $(PROJECT_TYPE)))
	rm -rf models src/models
	find . -type f -name "run_analysis.R" -execdir mv {} "run_analysis.py" \;
else
	rm -rf src/analysis
	find . -type f -name "predict.R" -execdir mv {} "predict.py" \;
	find . -type f -name "train.R" -execdir mv {} "train.py" \;
endif
else
ifeq (,$(wildcard ./environment.yml))
	@echo "name: $(PROJECT_NAME)\nchannels:\n    - conda-forge\n    - anaconda\ndependencies:\n    - r-base=4.0.0\n    - r-essentials=4.0.0\n    - jupyter\n    - r-irkernel" > environment.yml
else
	@echo ">>> Environment file already exists"
endif
	find . -type f -name "dump_data.py" -execdir mv {} "dump_data.R" \;
	find . -type f -name "make_dataset.py" -execdir mv {} "make_dataset.R" \;
	conda env create -f environment.yml

ifeq (data_analysis,$(findstring data_analysis, $(PROJECT_TYPE)))
	rm -rf models src/models
	find . -type f -name "run_analysis.py" -execdir mv {} "run_analysis.R" \;
else
	rm -rf src/analysis
	find . -type f -name "predict.py" -execdir mv {} "predict.R" \;
	find . -type f -name "train.py" -execdir mv {} "train.R" \;
endif
	find . -type f -name "*.py" -delete
	find . -type f -name "*.txt" -delete
endif
else
	@echo ">>> Conda installation not detected. Please install Conda first."
endif




## Create Jupyter Notebook Kernel
create_kernel:
ifeq (python,$(findstring python,$(INTERPRETER)))
	ipython kernel install --user --name=$(PROJECT_NAME)
else
	Rscript -e 'IRkernel::installspec(name="$(PROJECT_NAME)", displayname="$(PROJECT_NAME)")'
endif

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Get raw data
raw_data:
ifeq (python,$(findstring python,$(INTERPRETER)))
	$(INTERPRETER) src/data/dump_data.py data/raw 
else
	$(INTERPRETER) src/data/dump_data.R data/raw 
endif

## Create processed dataset
process_data:
ifeq (python,$(findstring python,$(INTERPRETER)))
	$(INTERPRETER) src/data/make_dataset.py data/raw data/processed
else
	$(INTERPRETER) src/data/make_dataset.R data/raw data/processed
endif

## Train model
train:
ifeq (python,$(findstring python,$(INTERPRETER)))
	$(INTERPRETER) src/models/train.py data/processed models/
else
	$(INTERPRETER) src/models/train.R data/processed models/
endif

## Predict data using model
predict:
ifeq (python,$(findstring python,$(INTERPRETER)))
	$(INTERPRETER) src/models/predict.py models/ data/processed outputs/
else
	$(INTERPRETER) src/models/predict.R models/ data/processed outputs/
endif

## Run analysis
analysis:
ifeq (python,$(findstring python,$(INTERPRETER)))
	$(INTERPRETER) src/analysis/run_analysis.py data/processed outputs/
else
	$(INTERPRETER) src/analysis/run_analysis.R data/processed outputs/
endif




#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
