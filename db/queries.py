# Lentelės kūrimas
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);
"""

# Vartotojo įterpimas
insert_user = """
INSERT INTO users (name, email) VALUES (%s, %s);
"""

# Vartotojų gavimas
select_all_users = """
SELECT id, name, email FROM users;
"""
