#export KAGGLE_API_TOKEN=KGAT_07544794848fdea400c3c5fb3fee4de9

import kagglehub

# Download latest version
path = kagglehub.dataset_download("kazanova/sentiment140")
print("Path to dataset files:", path)

path = kagglehub.dataset_download("dhruvildave/github-commit-messages-dataset")
print("Path to dataset files:", path)

path = kagglehub.dataset_download("smagnan/1-million-reddit-comments-from-40-subreddits")
print("Path to dataset files:", path)