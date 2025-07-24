if [[ "$1" == "" ]]; then
	echo -e "<!--\n:title x\n-->\n<pre class=code-color>" > /tmp/e.html
	cat | python3 format-c.py >> /tmp/e.html
	echo "</pre>" >> /tmp/e.html
	python3 preview.py /tmp/e.html
else
	echo -e "<!--\n:title x\n-->\n<pre class=code-color>" > /tmp/e.html
	cat $1 | python3 format-c.py >> /tmp/e.html
	echo "</pre>" >> /tmp/e.html
	python3 preview.py /tmp/e.html
fi
