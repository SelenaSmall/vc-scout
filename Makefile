setup:
	pip install -r requirements.txt

run:
	python agent/run.py

fetch:
	cd agent && python -c "from fetch import fetch_all_articles; [print(f'[{a[\"source\"]}] {a[\"title\"]}') for a in fetch_all_articles()]"

discover:
	cd agent && python -c "from fetch import fetch_all_articles; from discover import extract_entities; a = fetch_all_articles()[0]; print(a['title']); print(extract_entities(a))"
