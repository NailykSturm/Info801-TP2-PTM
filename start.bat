@echo off

python main.py
taskkill /F /FI "IMAGENAME eq components/" /T
echo "Plus de processus zombies normalement"