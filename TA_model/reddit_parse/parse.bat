:: This batch file was written by Rachel
:: Iterates through subdirectories in reddit_data to run reddit_parse
@echo off
FOR /D %%y IN (reddit_data\*) DO (
	python reddit_parse.py --input_file %%y
	)
