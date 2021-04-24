all: 
	python3 gen.py
	# cp CNAME docs
	cp -r static docs

clean:
	rm -r docs

git:	all
	git add .
