@echo off
FOR /D %%y IN (reddit_data\*) DO (
	python reddit_parse.py --input_file %%y
	)
