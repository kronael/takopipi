image := takopipi

image:
	docker build -t $(image) .

right:
	uvx pyright plugins/

test: right

clean:
	find plugins -type d -name __pycache__ -exec rm -rf {} +

.PHONY: image right test clean
