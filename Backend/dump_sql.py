import sys
import os
import json
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable, DropTable

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.database import Base
from app.models.product import Product
from seed import PRODUCTS

engine = create_engine('postgresql://')

# Start DDL with a drop command (optional but safe)
ddl = "DROP TABLE IF EXISTS products CASCADE;\n\n"

# Generate CREATE TABLE
create_table_stmt = CreateTable(Product.__table__).compile(engine)
ddl += str(create_table_stmt).strip() + ";\n\n"

def json_escape(v):
    if v is None:
        return 'NULL'
    s = json.dumps(v)
    return "'" + s.replace("'", "''") + "'"

def str_escape(v):
    if v is None:
        return 'NULL'
    return "'" + str(v).replace("'", "''") + "'"

for p in PRODUCTS:
    insert = f"""
    INSERT INTO products (id, name, category, price, "oldPrice", badge, color, sizes, colors, images, description, details, fit, stock_quantity)
    VALUES (
        {p['id']},
        {str_escape(p['name'])},
        {str_escape(p['category'])},
        {p['price']},
        {p['oldPrice'] if p['oldPrice'] is not None else 'NULL'},
        {str_escape(p.get('badge'))},
        {str_escape(p['color'])},
        {json_escape(p['sizes'])},
        {json_escape(p['colors'])},
        {json_escape(p['images'])},
        {str_escape(p['description'])},
        {json_escape(p['details'])},
        {str_escape(p['fit'])},
        100
    );
    """
    ddl += insert

with open('seed.sql', 'w', encoding='utf-8') as f:
    f.write(ddl)

print("seed.sql generated successfully")

