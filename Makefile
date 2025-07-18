# Local analysis by pytest, coverage run pytest, flake8, and badge generation.
#
# This Makefile presumes an activated virtual environment of Python and an
# internet connection for pytest's checks on pubchempy's interaction with NIH.
# In contast to e.g., the coverage badge by coveralls, the setup here does not
# rely on a separate account, nor a GitHub token to work.  By flag `-l`, the
# badges are created locally, independent of genbadge's default to reach out
# for shields.io.

default:
	@echo "Tap the tabulator key twice to display the options available."

analysis_setup:
# For now, the partial overlap with `requirements/dev.txt` is intentional.
	pip install -r requirements/analysis.txt

pytest_analysis:
	pytest --cache-clear --junitxml=junit.xml -v
pytest_badge:
	genbadge tests -i junit.xml -lv

coverage_analysis:
	coverage run -m pytest -v
coverage_badge:
	coverage report && coverage xml && coverage html
	genbadge coverage -i coverage.xml -lv

flake8_analysis:
	-rm -r reports
	-rm flake8stats.txt
	mkdir reports

	flake8 pubchempy.py --exit-zero --statistics --count \
		--tee --format=html --htmldir=reports/ --output-file flake8stats.txt \
		--max-line-length 120

	@echo ""
	@echo "For a more detailed report, see file reports/index.html."
flake8_badge:
	genbadge flake8 -i flake8stats.txt -lv

remove_all_but_the_badges:
	-rm -r __pycache__
	-rm -r tests/__pycache__
	-rm *.xml

	-rm .coverage
	-rm -r htmlcov

	-rm -r reports
	-rm flake8stats.txt

	-pyclean .
