setup:
	pip install -r requirements.txt

run:
	python agent/run.py

fetch:
	cd agent && python -c "from fetch import fetch_titles; print(fetch_titles())"
