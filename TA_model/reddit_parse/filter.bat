@echo off
FOR /D %%y IN (reddit_data\*) DO (
	@ECHO Getting data from %%y
	python filter_subs.py --input_file %%y
	)
