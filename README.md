# Personal Blog Source Code

## Dependencies

- Pipenv
- Python3.8


## Generate Site

To generate static HTML output from markdown content, run:

```bash
$ pipenv run pelican content -o output
```

## Preview Site Locally

Switch to the output directory and launch the server:

```bash
$ pipenv run pelican --listen
```

## Publish Site

```
$ pipenv run pelican -s publishconf.py
```

Then commit & push changes in output to github pages repo.
