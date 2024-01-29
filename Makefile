# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* data_pipelines/*.py

black:
	@black scripts/* data_pipelines/*.py

pre-commit:
	@pre-commit run --file `find . -name "*.py" | grep -v "alembic"`
	@pre-commit run check-yaml --file `find . -name "*.y*ml"`

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"
