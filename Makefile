clean:
	@echo .. cleaning up temporary files
	@find . -type f -name "*.pyc" -exec rm {} \;
