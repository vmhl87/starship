if [[ "$1" == "" ]]; then
	echo "usage: $0 [c|cst] [file]"
else
	if [[ "$1" == "c" ]]; then
		cat | python3 ~/misc/starship/build/format-c.py | xclip -i -selection clipboard
	elif [[ "$1" == "cst" ]]; then
		cat | python3 ~/misc/starship/build/format-cst.py | xclip -i -selection clipboard
	elif [[ -f $1 ]]; then
		echo $1
		lang="c"
		if [[ $1 == *s ]]; then
			lang="cst"
		fi
		cat $1 | python3 ~/misc/starship/build/format-$lang.py | xclip -i -selection clipboard
	else
		echo "$1: can't find file"
	fi
fi
