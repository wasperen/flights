#!/bin/bash
tail +2 $1 | python transform-flights.py >trans-$1
gzip $1
