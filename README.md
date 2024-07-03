# Starship - a Python static blog generator

A simple set of Python scripts to build a static,
JS-free, customizable blog.

## Usage

Starship uses HTML snippets to store blog drafts/entries.
Put meta-information like title, date, tags, etc. in an html
comment at the top of the file and simply write the rest of
the body in plain html. For example:

`build/drafts/example.html`
```
<!--
	:title Nothing to see here (yet)
-->

<p>Add Posts with <b>publish.py</b>!</p>
```

Longer posts can specify a summary cutoff with `[[ENDSUM]]`.
More information about formatting
[here](https://vmhl87.github.io/starship/pages/6_previews.html).

Render a draft with `preview.py <draft>`, or publish it with
`publish.py <draft>`. Because the generated blog is static,
Starship caches build artifacts to efficiently build content.
It is **very important** to check that the `.artifacts` folder
is up to date before publishing a new page.

## Customization

Set the blog name with setup.py, or manually in `build/source/title.cfg`.
(Due to the static nature of Starship, changing the blog name globally
is a pretty difficult process, but it's still possible.)

For theme modifications edit `style.css`, and if you need to
import extra stylesheets for google fonts or the like, do so
in `build/source/head.html`.

Messing around with the html layout is somewhat difficult as
the collections script reads both from `build/source/template.html`
and also input from `draft.py` to generate the final pages.
Hopefully the code isn't *too* terrible to edit, though.
