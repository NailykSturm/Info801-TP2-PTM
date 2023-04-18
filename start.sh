#!/bin/sh

python main.py
ps -aux | grep components/ | awk '{print $2}' | xargs kill -9
echo "Plus de processus zombies normalement"