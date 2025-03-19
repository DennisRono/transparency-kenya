.PHONY: local

local:
	uvicorn app.main:app --reload
	