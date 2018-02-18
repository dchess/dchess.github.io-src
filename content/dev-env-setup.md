Title: Automating Developer Environment Setup
Date: 2018-02-18 13:30
Category: Blog
Summary: Scripting my setup for development has made my life easier

I develop on Linux. Ubuntu to be specific. Most of the web apps I build I end
up deploying to Heroku. Since their stack is based on Ubuntu and Postgres, I 
try to make my local environment as close to production as possible. 

That means I don't use simpler development databases like SQLite in my local
setup and I don't build on Windows or Mac and then hope my code will deploy
properly in production. I don't want any suprises!

To that effect, I try to automate my setup as much as possible. 

For work, I develop within a Linux virtual machine (using Virtualbox). At home, 
I'm already using linux as my main os. But I want my setup, tools, and 
configurations to be identical no matter where I am working. I also want to be
able to spin up a new VM at a moment's notice and be ready to go in no time.

To help facilitate that need, I have a [github repo](https://github.com/dchess/dev-env-setup)
where I store my dotfiles and a few shell scripts to easily setup my
development environment. 

I prefer to work in the terminal as much as possible and so I use Vim as my
text editor with a few custom configurations to emulate some IDE like features.

I also prefer to handle version control with git in the terminal and have a few
custom aliases I like to make sure are available wherever I'm working.

But the most valuable script I have is my database setup script. Installing
Postgres can be daunting, particularly at the start of a new project. I don't
want that to be a hindrance for myself or other developers on my team. While I
have a generic postgres setup script, I also have a more custom one for use in
Django web apps that I store in the source code of each app I deploy. That can
be a huge help when handing off to another developer on the team, so they have
exactly the same database configuration as every other developer working on the
project, with single button deployment.

# VIM Config

My Vim config is pretty simple compared to many I've seen, but there are a few
things I can't live without. I was big on Sublime before I moved to Vim and so
I really appreciate having a fuzzy finder and file tree available. So I use
NERDTree and CtrlP for that. I also like being able to easily comment blocks of
code and use NERDCommenter for that. 

As I've shifted to using Python more, I found [this tutorial from Real Python](https://realpython.com/blog/python/vim-and-python-a-match-made-in-heaven/)
really helpful for thinking about how I wanted Vim configured to better support
Python specifically. The main call outs are white space config (both indents and
trailing whitespace), code-completion, and PEP8 compliance. Using static 
analysis tools like Flake8 has greatly cut down on the need for those arguments
during code review.

Beyond those Vundle plugins, I keep a copy of my current .vimrc file in my repo
for easy syncing. If I make a change locally, I push it to the repo so I can
pull it down in any other environment I'm working in. I also like a certain
color scheme and run a support script during setup to ensure both my terminal
and Vim use the same colors. It cuts down on context switching when I have to 
hop in and out of my editor to run commands.

# Git Config

My git settings mostly consist of setting up my editor to be Vim by default and
a series of helpful aliases. I drew a lot of inspiration from
[this article from You've Been Haacked](https://haacked.com/archive/2014/07/28/github-flow-aliases/).

I use the quick commit and pretty formatted git log constantly. Likewise the
grep functionality for the commit history is incredibly useful.

# Bash Config

My .bashrc is pretty standard, with one key exception. I really like being
able to see the git branch name in my prompt. I incorporated
[this tip from Coderwall](https://coderwall.com/p/fasnya/add-git-branch-name-to-bash-prompt),
which couldn't be any easier. Other than that I mostly have aliases to quickly
jump to current project directories I'm working on. Although lately, I've been
experimenting with some aliases for Django. Typing out `python manage.py runserver`
or even `./manage.py makemigrations` all the time can be a little tedious. I
know I could use [django-shortcuts](https://github.com/jgorset/django-shortcuts)
but it really seems like a bash function ought to be able to handle my needs. 

# Postgres Installation

When I first was working in Rails and trying to set up PostgreSQL, I had a lot
of hiccups initially. I'd install with the wrong account permissions, or I was
missing some dependency. I'd get it configured, then port to a new system and 
have to spend time trying to get it all back to working order. It was a serious
headache.

Then, I found this great resource for installing Ruby on Rails on Ubuntu from 
[Go Rails](https://gorails.com/setup/ubuntu/16.04) which had a small aside
about Postgres. I was inspired by the simplicity of their directions and
[translated it into a shell script](https://github.com/dchess/dev-env-setup/blob/master/rails.sh)
to automate it. 

While I have since largely put Rails behind me (I still have a few legacy apps
that I maintain), I am absolutely indebted to the advice about databse setup.

Just to show how simple this is, here is my postgre setup script. It's 7 lines.

```bash
#!/bin/bash

user=$(whoami)

sudo sh -c "echo 'deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main' > /etc/apt/sources.list.d/pgdg.list"
wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install -y postgresql-common
sudo apt-get install -y postgresql libpq-dev

sudo -u postgres createuser $user -s
```

It does all the heavy lifting. Figures out what account I am installing with,
gets the necessary repository info, installs postgres, and even sets up a user
based on my account to access it with. 

I've taken this idea a little further for Django and now run something a
little more complicated. 

```bash
#!/bin/bash

# Exit if command fails
set -e
# Treat unset variables as errors
set -u

# Set user as current account
user=$(whoami)

# Install Postgres 10
sudo sh -c "echo 'deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main' >> /etc/apt/sources.list.d/pgdg.list"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install -y postgresql-common
sudo apt-get install -y postgresql-10 postgresql-contrib libpq-dev

# Create superuser account as self for local management
sudo -u postgres createuser $user -s

# Set env vars for colors
YELLOW='\033[1;33m'
NC='\033[0m'

# Collect arguments from user
# Project specific values
printf "${YELLOW}Database name:\n${NC}"
read database
printf "${YELLOW}Username:\n${NC}"
read username
printf "${YELLOW}Password:\n${NC}"
read password

# Create database and user
RUN_ON_PSQL="psql -X -U $user --set ON_ERROR_STOP=on --set AUTOCOMMIT=off postgres"
$RUN_ON_PSQL <<SQL
CREATE DATABASE $database;
CREATE USER $username WITH PASSWORD '$password';
ALTER ROLE $username SET client_encoding TO 'utf8';
ALTER ROLE $username SET default_transaction_isolation TO 'read committed';
ALTER ROLE $username SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE $database TO $username; 
ALTER USER $username CREATEDB;
commit;
SQL

exit 0
```

Now my team can clone my repo, run this app and be good to go in seconds. It
could not be any easier to hand off my code!

# Conclusion

There are always ways to automate your workflow. I am constantly on the look
out for ways I can take the guess work out of my development configuration.

There are other things I rely on that I haven't mentioned here in detail (but 
you can find them in my [repo](https://github.com/dchess/dev-env-setup)) like
installing [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) or 
[ngrok](https://ngrok.com/). 

I keep adding more automation to my setup as I go. In fact, I'm pretty sure 
that's my most active public repo!
