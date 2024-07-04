# Starship - a Python static blog generator

A simple set of Python scripts to build a static,
JS-free, customizable blog.

## Usage

### Of course, fork the repo so you can make changes

Set the name of the blog in `name.txt`. Because the blog
is statically generated, you won't easily be able to change
its name later.

Starship uses HTML snippets to store blog drafts/entries.
Put meta-information like title, date, tags, etc. in an html
comment at the top of the file and simply write the rest of
the body in plain html. For example:

`build/drafts/example.html`
```html
<!--
	:title Nothing to see here (yet)
	:tag example help test
-->

<p>Add Posts with <b>publish.py</b>!</p>
```

With longer posts, you can delineate a "summary" section by
adding an `[[ENDSUM]]` object in the body. It'll render into
the main blog feed and any categories it's in as only the
summary, and show the whole post in a standalone page.

You can store these in `build/drafts/`, or really wherever
you want.

Preview a draft with `preview.py <draft>`, or publish it with
`publish.py <draft>`. (These scripts are located in the `build`
dir, and you should run them from there.)

**As it is currently very difficult to edit or delete past posts,
make sure that your draft is as you want it before publishing.
If you aren't sure, use the preview script!**

Because the generated blog is static, Starship stores build
artifacts to efficiently build content. It is **very important**
to check that your artifacts are up to date before publishing a
new page - it's like merge conflicts, but worse!

## Customization

Add theme modifications to `style.css`. If you need to
import extra stylesheets for google fonts or the like, do so
in `build/source/head.html`.

Messing around with the html layout is somewhat difficult as
the collections script reads both from `build/source/template.html`
and also input from `draft.py` and `collect.py` to generate the
final pages. Hopefully the code isn't *too* terrible to edit, though!

I would prefer that you leave the Starship grabber as-is, but
you can really do what you want :)
