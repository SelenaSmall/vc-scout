setup:
	pip install -r requirements.txt

run:
	python agent/run.py

fetch:
	python -c "from agent.fetch import fetch_titles; print(fetch_titles())"
