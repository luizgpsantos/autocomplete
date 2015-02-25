.PHONY: clean setup test

clean:
	@rm -rf `find . -name "*.pyc"` `find . -name "*.orig"`

setup:
	@pip install -r test-requirements.txt

test: setup
	@nosetests tests/unit --spec-color --with-spec