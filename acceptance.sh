set -e
docker build -t quickfixdoc-acceptance .
declare -a specs=("FIX40" "FIX41" "FIX42" "FIX43" "FIX44" "FIX50" "FIX50SP1" "FIX50SP2" "FIXT11")
for i in "${specs[@]}"
do
   docker run -t --rm -e FIXSPECNAME="$i" -v $(PWD)/acceptance/"$i":/tmp/quickfix-doc/output quickfixdoc-acceptance &
done
wait
