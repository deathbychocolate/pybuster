.PHONY: test
test:
	@pipenv run pytest --log-cli-level=ERROR

.PHONY: coverage
coverage:
	@pipenv run pytest --log-cli-level=ERROR --cov=gptcli/src/ --cov-report html --cov-branch

.PHONY: clean
clean:
	@python3 -m pyclean .

.PHONY: clean-coverage
clean-coverage:
	@rm .coverage
	@rm -r htmlcov
