import sqlite3
import os

# Conectar a la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data.db")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Crear tabla
cursor.execute("""
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT,
    valor REAL,
    fecha TEXT
)
""")

# Insertar datos de ejemplo
ventas_data = [
    ("Electronica", 5000, "2024-02-01"),
    ("Ropa", 2000, "2024-02-02"),
    ("Alimentos", 3000, "2024-02-03"),
    ("Juguetes", 1500, "2024-02-04"),
    ("Electronica", 6000, "2024-02-05"),
    ("Ropa", 2500, "2024-02-06"),
    ("Alimentos", 4000, "2024-02-07"),
    ("Juguetes", 1800, "2024-02-08"),
]

cursor.executemany("INSERT INTO ventas (categoria, valor, fecha) VALUES (?, ?, ?)", ventas_data)

# Guardar cambios y cerrar
conn.commit()
conn.close()
print("Base de datos creada y datos insertados.")

