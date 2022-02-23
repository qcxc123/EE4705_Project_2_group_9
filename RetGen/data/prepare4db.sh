# This shell script was written by Rachel
# Processes raw train.tsv for compression to db
less arxiv_train_raw.tsv| awk -F '\t' '{print $1"\t"$2"\t"$3}'> arxiv_train.tsv
