docker build -t quickfixdoc-acceptance .
docker run -t --rm -e FIXSPECNAME=FIX42 -v $(PWD)/acceptance/FIX42:/tmp/quickfix-doc/output quickfixdoc-acceptance
echo "PASS"