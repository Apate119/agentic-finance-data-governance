.PHONY: run install clean status

install:
	pip install -r requirements.txt

run:
	python src/pipeline/run_pipeline.py

status:
	git status

clean:
	rm -f data/warehouse/*.duckdb
	rm -f outputs/data_quality/*.csv
	rm -f outputs/scorecards/*.csv
	rm -f outputs/exceptions/*.csv
	rm -f outputs/remediation/*.csv