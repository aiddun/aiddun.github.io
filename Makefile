all: 
	python gen.py
	cp static/* docs

clean:
	rm -r build