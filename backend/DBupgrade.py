import mysql.connector
import json

conn = mysql.connector.connect(
    host="localhost",   # e.g., 'localhost'
    user="root",   # e.g., 'root'
    password="12345678",   # e.g., 'password'
    database="testdb"   # e.g., 'dict'
)

cursor = conn.cursor()

with open('C:/Users/whals/Downloads/용어_내려받기_20241012031232.json','r', encoding='utf-8') as f:
    json_data = json.load(f)

    for item in json_data['terms']:
        title = item['form'].replace('^', ' ')
        print(title)

        if item.get('orginal_language') and len(item['orginal_language']) > 0:
            original_word = item['orginal_language'][0]['form']
        else:
            original_word = None  # Fallback if orginal_language is missing or empty
        #print(f"Original word: {original_word}")

        description = ''

        for i, data in enumerate(item['definitions'], 1):
            description += f"{data['definition']} "
        
        synonym = None
        korean_word = None

        for related_term in item.get('related_terms', []):
            term_type = related_term.get('type').strip().lower()
            form = related_term.get('form').replace('^', ' ')  # Replace ^ with space
            if term_type == '동의어':
                synonym = form  # Save synonym
            elif term_type == '다듬은 말':  # Refined word, 'prepared speech' is an example
                korean_word = form  # Save refined word

        translations_list = [translation.get('translation', '') for translation in item.get('translations', []) if 'translation' in translation]
        translations = ', '.join(translations_list) if translations_list else None  # Use '' if you prefer empty string

        cursor.execute("SELECT COUNT(*) FROM dict WHERE title = %s", (title,))
        result = cursor.fetchone()

        if result[0] > 0:
        # If the title exists, update the description2 field
            update_query = "UPDATE dict SET description2 = %s, original_word = %s, synonym = %s, korean_word = %s, translations = %s WHERE title = %s"
            cursor.execute(update_query, (description, original_word, synonym, korean_word, translations, title))
        else:
        # If the title does not exist, insert into the description field
            insert_query = "INSERT INTO dict (title, description, original_word, synonym, korean_word, translations) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (title, description, original_word, synonym, korean_word, translations))

# Commit the changes and close the database connection
conn.commit()
cursor.close()
conn.close()
