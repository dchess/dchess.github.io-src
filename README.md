# Personal Blog Source Code

## Dependencies

- Pipenv
- Python
- Pelican
- Pelican Themes
- ghp-import
- Markdown
- Flex theme

## Generate Site

To generate static HTML output from markdown content, run:

```bash
$ pelican content -o output -s pelicanconf.py
```

## Preview Site Locally

Switch to the output directory and launch the server:

```bash
$ cd /output
$ python -m pelican.server
```

## Githook

Add the following hook to local .git/hooks/post-commit:

```bash
pelican content -o output -s pelicanconf.py && ghp-import && git pub
```

## Git Remote

Add the following additional remote locally:

```bash
$ git remote add io https://github.com/dchess/dchess.github.io
```

## Git Alias

Add the follow alias to git config

```bash
$ git config --global alias.pub 'git push io gh-pages:master'
```

**Don't forget to push gh-pages branch to origin as well!**
