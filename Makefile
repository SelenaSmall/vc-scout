setup:
	pip install -r requirements.txt

run:
	python agent/run.py

fetch:
	cd agent && python -c "from fetch import fetch_articles; [print(a['title']) for a in fetch_articles()]"

discover:
	cd agent && python -c "from fetch import fetch_articles; from discover import extract_entities; a = fetch_articles()[0]; print(a['title']); print(extract_entities(a))"
