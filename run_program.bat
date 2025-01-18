@echo D:\projects\

cd /d D:\projects\anilist

call venv\Scripts\activate

python main.py >> logs.txt 2>&1
deactivate
