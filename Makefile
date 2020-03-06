index:
	./make_index.py --manifest ../Packages/MANIFEST.txt  

clean:
	rm -f index.html
	find . -name \*~ | xargs rm


PHONY: clean index
