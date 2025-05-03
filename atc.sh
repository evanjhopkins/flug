#!/bin/bash
cd /home/evan/code/atc || exit 1
exec pixi run python /home/evan/code/atc/atc/__main__.py "$@"
