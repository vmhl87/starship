# Starship - a Python static blog generator

A simple set of Python scripts to build a static,
JS-free, customizable blog.

## Usage

### Of course, fork the repo so you can make changes

Set the name of the blog in `name.txt`. Starting from
Starship release v1.3.2, you can easily change the
name/template/style of past content easily, so don't stress!

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

Because the generated blog is static, Starship stores build
artifacts to efficiently build content. It is **very important**
to check that your artifacts are up to date before publishing a
new page, or else page order could get *very* messed up - it's
like merge conflicts, but worse!

Artifacts are stored in `build/artifacts` and contain repackaged
past drafts. Editing posts is pretty easy - just edit the draft
as you would edit a normal one, and then run `rebuild.py` to
propagate changes. You can even use `preview.py` on these drafts,
too!

Post order is stored in `build/artifacts/state`. It is quite
literally just a text list of all posts created in order. If you
want to swap the order of posts, do so there.

To delete a post add the tag `hidden` to its draft and rebuild.
It'll hide from main content. Don't actually delete the file or
remove it from page order or it could potentially cause naming
conflicts in the future. (A future update might fix this.)

Also, don't change the filenames of anything in the artifacts
directory; it could definitely mess things up.

## Customization

Add theme modifications to `style.css`. If you need to
import extra stylesheets for google fonts or the like, do so
in `build/source/head.html`.

Messing around with the html layout is somewhat difficult as
the collections script reads both from `build/source/template.html`
and also input from `draft.py` and `collect.py` to generate the
final pages. Hopefully the code isn't *too* terrible to edit, though!

To apply name/template/head changes to past content, run `rebuild.py`
in `build`.

I would prefer that you leave the Starship grabber as-is, but
you can really do what you want :)
