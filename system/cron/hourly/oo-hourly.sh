#!/bin/bash

# tasks run hourly

OO_HOME=/home/oo/ordine.psicologipuglia.it

pushd ${OO_HOME}

echo "Load virtual env"
. private/system/load_venv.sh

echo "Rebuilding Solr indexes"
django-admin.py rebuild_index --verbosity=2 --noinput

echo "Deactivate virtual env"
deactivate

popd
