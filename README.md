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

Add the following hook to local .git/hooks:
```bash
pelican content -o output -s pelicanconf.py && ghp-import && git pub
```
