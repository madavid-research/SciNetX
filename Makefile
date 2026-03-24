.PHONY: public-records public-records-check

PUBLIC_RECORDS_CONFIG := public_records/config/scinetx.json

public-records:
	python3 scripts/generate_public_records.py --config $(PUBLIC_RECORDS_CONFIG)

public-records-check:
	python3 -m py_compile scripts/generate_public_records.py
	python3 scripts/generate_public_records.py --config $(PUBLIC_RECORDS_CONFIG)
