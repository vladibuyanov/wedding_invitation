#!/bin/bash


echo "Update files"
echo "---------------------"
pybabel extract -o messages.pot -F babel.cfg .
pybabel update -i messages.pot -d translations
pybabel compile -d translations