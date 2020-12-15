all: 
	python gen.py
	cp CNAME docs
	cp -r static docs

clean:
	rm -r docs