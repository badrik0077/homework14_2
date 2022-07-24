import sqlite3
from flask import Flask, app, jsonify
import json

app = Flask(__name__)


def get_value_from_db(sql):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        result = connection.execute(sql).fetchall()
        return result


def search_by_title(title):
    sql = f""" SELECT * FROM netflix 
    WHERE title = '{title}' 
    ORDER BY release_year desc LIMIT 1 """

    result = get_value_from_db(sql)
    for item in result:
        return dict(item)


@app.get("/movie/<title>/")
def search_by_title_view(title):
    result = search_by_title(title=title)
    return jsonify(result)

@app.get("/movie/<year1>/to/<year2>/")
def search_date_view(year1, year2):
    sql = f"""
    select title, release_year
    from netlix
    where release_year between '{year1}' and '{year2}'
    limit 100
    """
    result = []
    for item in get_value_from_db(sql=sql):
        result.append(dict(item))

    return jsonify(result)


@app.get("/rating/<rating>/")
def search_rating_view(rating):
    my_dict = {
        "children": ("G", "G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }
    sql = f"""
    select title, rating, description
    from netlix
    where rating in {my_dict.get(rating, ("R", "R"))}
    """
    result = []
    for item in get_value_from_db(sql=sql):
        result.append(dict(item))

    return jsonify(result)


@app.get("/rating/<rating>genre/<genre>/")
def search_genre_view(genre):
    sql = f"""
    select *
    from netlix
    where listed_in like "%{genre}"
    order by release_year desc
    limit 10
    """
    result = []
    for item in get_value_from_db(sql=sql):
        result.append(dict(item))

    return jsonify(result)

@app.get("/movie/<year1>/to/<year2>/")
def search_double_name(name1, name2):
    sql = f"""
    select "cast"
    from netlix
    where "cast" LIKE "%{name1}% and "cast" like "%{name2}%
    """
    result = []
    names_dict = {}
    for item in get_value_from_db(sql=sql):
        names = set(dict(item).get("cast").split(",")) - set([name1, name2])

        for name in names:
            names_dict[str(name).strip()] = names+dict.get(name, 0) + 1

    for key, value in names_dict.items():
        if value >= 2:
            result.append(key)

    return jsonify(result)

def step_6(typ, year, genre):
    sql = f"""
    select title, description, listed_in
    from netlix
    where type = "{typ}"
    and release_year = "{year}",
    and listed_in like "%{genre}%"
    """
    result = []

    for item in get_value_from_db(sql):
        result.append(dict(item))

    return json.dumps(result, ensure_ascii=False, indent=4),

if __name__ == "__main__":
    app.run()
