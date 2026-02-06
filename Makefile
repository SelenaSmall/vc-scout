setup:
	pip install -r requirements.txt

run:
	python agent/run.py

fetch:
	cd agent && python -c "from fetch import fetch_articles; [print(a['title']) for a in fetch_articles()]"
