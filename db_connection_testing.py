import psycopg2

conn = psycopg2.connect(
    host='127.0.0.1',
    database='TGbotDB',
    user='tgbotty',
    password='yttobgt'
)
try:
    cursor = conn.cursor()
except psycopg2.OperationalError:
    print(psycopg2.OperationalError)

user_id = 1093678627
username = 'DimonRonD'

# cursor.execute(f'insert into notes (uid, uname, date_note, note) values ({user_id}, \'{username}\', CURRENT_DATE, \'my very long text\');')
# conn.commit()
cursor.execute('SELECT * FROM notes;', (1,))


# Fetch all results
rows = cursor.fetchall()
all_notes_str = ''
for row in sorted(rows):
    # for el in row:
    #     print(el)
    # print('\n')
    all_notes_str += str(row[3]) + '\t' + str(row[4]) + '\n'

print(all_notes_str)


cursor.close()
conn.close()

