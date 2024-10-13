import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myterminology.settings')
django.setup()

from django.db import connection
from konlpy.tag import Kkma

# Open and read the file
with open("body.txt", 'r', encoding="utf-8") as f1:
    data = f1.read()

kkma = Kkma()
kor_text = data
text_list = kkma.pos(kor_text)

# Insert data into the database
for i, text in enumerate(text_list):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO search_list (id, search_word, search_pos)
            VALUES (%s, %s, %s)
        """, [i, text[0], text[1]])
