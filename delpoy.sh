#! /bin/bash
#
# delpoy.sh
# Copyright (C) 2020 renard <renard@voyager>
#
# Distributed under terms of the MIT license.
#


PYBIN=$(which python3 | tr -d '\n')
VENVBIN=$(which virtualenv | tr -d '\n')
VENVDIR=venv

if [ ! -n PYBIN ]; then
    echo "Python 3 binary not found." >&2;
    return 1;
fi

if [ ! -n VENVBIN ]; then
    echo "Virtualenv binary not found." >&2;
    return 1;
fi

if [ ! -n $(which pip3 | tr -d '\n') ]; then
    echo "Pip3 binary not found." >&2;
    return 1;
fi

if [ ! -n $(which mysql | tr -d '\n') ]; then
    echo "MySQL is not installed." >&2;
    return 1;
fi

$VENVBIN -p $PYBIN $VENVDIR
source $VENVDIR/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
deactivate

echo; echo "Please enter your password to enable the MySQL service."
sudo systemctl enable mariadb.service

echo; echo "EpyTodo environment installed."
echo "Please source the right activation script for your shell from $VENVDIR/bin/."
