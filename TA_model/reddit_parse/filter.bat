:: This batch file was written by Rachel
:: Iterates through subdirectories in reddit_data to collect subreddit names and count
@echo off
FOR /D %%y IN (reddit_data\*) DO (
	@ECHO Getting data from %%y
	python filter_subs.py --input_file %%y
	)
