if [[ -f $1 ]]; then
	echo $1
	cat $1 | python3 ~/misc/starship/build/format.py | xclip -i -selection clipboard
else
	cat | python3 ~/misc/starship/build/format.py | xclip -i -selection clipboard
fi
