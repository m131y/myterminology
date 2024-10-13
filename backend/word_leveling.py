import mysql.connector
from leveling import assign_level_based_on_description, technical_terms  # Import necessary functions

conn = mysql.connector.connect(
    host="localhost",   # e.g., 'localhost'
    user="root",   # e.g., 'root'
    password="12345678",   # e.g., 'password'
    database="testdb"   # e.g., 'dict'
)

cursor = conn.cursor()

# Step 2: Retrieve titles and descriptions from the 'dict' table
cursor.execute("SELECT id, title, description, description2 FROM dict")
words = cursor.fetchall()

# Prepare the data for the leveling algorithm
terms = [title for _, title, _, _ in words]  # Unpack four values
descriptions = [
    f"{description} {description2}" if description2 else description
    for _, _, description, description2 in words
]
# Step 3: Calculate levels using the leveling algorithm
term_levels = assign_level_based_on_description(terms, descriptions, technical_terms)

# Step 4: Save the calculated levels back to the database
for word_data in words:
    word_id, title, description, description2  = word_data
    level = term_levels.get(title, 1)  # Default to level 1 if the title is not in term_levels

    cursor.execute("UPDATE dict SET word_level = %s WHERE id = %s", (level, word_id))

# Commit the changes and close the database connection
conn.commit()
cursor.close()
conn.close()

print("Leveling process completed!")
