#!/bin/sh
# copy hooks
cp -r .githooks/* .git/hooks/
# make hooks executable
chmod +x .git/hooks/*
