import psycopg2
from datetime import datetime

def format_user(user):
    return f"ID: {user[0]}, Vardas: {user[1]}, El. paštas: {user[2]}"


# Funkcija, kuri padeda patikrinti ir grąžinti klaidas
def handle_db_error(error: psycopg2.Error):
    print(f"❌ Klaida duomenų bazėje: {error.pgcode} - {error.pgerror}")
    # Galite pridėti daugiau logikos, pvz., klaidos registravimą į failą arba siuntimą į monitoringą

# Funkcija, kuri grąžina paskutinį įrašytą ID
def get_last_inserted_id(cursor):
    cursor.execute("SELECT LASTVAL();")
    return cursor.fetchone()[0]

# Funkcija, kuri tikrina, ar lentelė egzistuoja
def table_exists(cursor, table_name):
    cursor.execute("""
    SELECT EXISTS (
        SELECT 1
        FROM   information_schema.tables 
        WHERE  table_name = %s
    );
    """, (table_name,))
    return cursor.fetchone()[0]

# Parametrizuota užklausa, kad užkirstų kelią SQL injekcijai
def execute_query_with_params(cursor, query, params):
    cursor.execute(query, params)

# Funkcija, kuri formatuoja vartotojo duomenis
def format_user(user):
    return f"ID: {user[0]}, Vardas: {user[1]}, El. paštas: {user[2]}"

# Funkcija, kuri formatuoja užklausos rezultatus į žmogui suprantamą tekstą
def format_query_results(cursor):
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    formatted_results = [dict(zip(columns, row)) for row in rows]
    return formatted_results

# Funkcija, kuri užtikrina, kad commit ir rollback būtų atlikti automatiškai
def commit_transaction(connection):
    try:
        connection.commit()
    except psycopg2.Error as e:
        connection.rollback()
        print(f"❌ Klaida atlikus commit: {e}")
        raise

# Funkcija, kuri leidžia vykdyti kelias užklausas iš karto
def execute_batch(cursor, queries, params_list):
    try:
        cursor.executemany(queries, params_list)
    except psycopg2.Error as e:
        print(f"❌ Klaida vykdant batch užklausas: {e}")
        raise


# Funkcija, kuri konvertuoja timestamp į žmogui suprantamą datą
def format_timestamp(timestamp):
    return timestamp.strftime("%Y-%m-%d %H:%M:%S") if timestamp else None

# Funkcija, kuri užkrauna SQL užklausą iš failo
def load_sql_from_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()
