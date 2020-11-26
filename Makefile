all: 
	python gen.py
	cp static/* build

clean:
	rm -r build