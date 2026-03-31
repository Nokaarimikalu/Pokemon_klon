import sqlite3
import requests


con = sqlite3.connect("pokemon_game.db")
cur = con.cursor()

# unabhaengige Tabellen
create_types_table = """

    CREATE TABLE IF NOT EXISTS types(
        id INTEGER PRIMARY KEY,
        name TEXT
    )

"""

create_items_table = """

    CREATE TABLE IF NOT EXISTS items(
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        category TEXT,
        price INTEGER,
        fling_power INTEGER,
        effect_value INTEGER,
        move_id INTEGER
    )

"""

create_pokemon_info_table = """

    CREATE TABLE IF NOT EXISTS pokemon_info(
        id INTEGER PRIMARY KEY,
        name TEXT,
        hp INTEGER,
        atk INTEGER,
        def INTEGER,
        sp_atk INTEGER,
        sp_def INTEGER,
        speed INTEGER,
        height INTEGER,
        weight INTEGER,
        base_experience INTEGER,
        capture_rate INTEGER,
        gender_rate INTEGER,
        hatch_counter INTEGER,
        growth_rate TEXT,
        flavor_text TEXT

    )
"""

# Die Regel- & Deteil-Tabellen

create_type_efficiency_table = """

    CREATE TABLE IF NOT EXISTS type_efficiency(
        damage_type_id INTEGER,
        target_type_id INTEGER,
        damage_factor REAL
    )

"""

create_moves_table = """

    CREATE TABLE IF NOT EXISTS moves(
        id INTEGER, 
        name TEXT,
        power INTEGER,
        accuracy INTEGER,
        pp INTEGER,
        priority INTEGER,
        type_id INTEGER,
        damage_class TEXT
    )

"""

create_pokemon_types = """

    CREATE TABLE IF NOT EXISTS pokemon_types(
        pokemon_id INTEGER,
        type_id INTEGER,
        slot INTEGER
    )
"""

create_pokemon_abilities = """

    CREATE TABLE IF NOT EXISTS pokemon_abilities(
        pokemon_id INTEGER,
        ability_name TEXT,
        is_hidden INTEGER
    )
"""

create_pokemon_moves_table = """
    CREATE TABLE IF NOT EXISTS pokemon_moves(
        pokemon_id INTEGER,
        move_id INTEGER,
        level_learned INTEGER,
        learn_method TEXT 
    )
"""

create_pokemon_evolutions_table = """
    CREATE TABLE IF NOT EXISTS pokemon_evolutions(
        from_id INTEGER,      
        to_id INTEGER,        
        evolution_level INTEGER, 
        item_id INTEGER,      
        trigger_name TEXT     
    )
"""

create_pokemon_egg_groups_table = """
    CREATE TABLE IF NOT EXISTS pokemon_egg_groups(
        pokemon_id INTEGER,
        group_name TEXT
    )
"""

tables = [
    create_types_table, create_items_table, create_pokemon_info_table,
    create_type_efficiency_table, create_moves_table, create_pokemon_types,
    create_pokemon_abilities, create_pokemon_moves_table, 
    create_pokemon_evolutions_table, create_pokemon_egg_groups_table
]

for table in tables:
    cur.execute(table)

con.commit()
con.close()
print("Datenbank-Schema erfolgreich erstellt!")