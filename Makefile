
gcloud_path = /Users/natapollimpananuwat/google-cloud-sdk/bin
# export PATH="${PATH}:$(gcloud_path)"

first_setup:
	pip install poetry
	poetry install
	
gcloud:
	
	@echo ${PATH}

gcp_login_and_setup:
	gcloud auth application-default login
	gcloud config set project stock-analytics-403505

dvc_initialize:
	dvc init
	dvc remote add -d myremote gs://stock-analytics-project/dvc_data