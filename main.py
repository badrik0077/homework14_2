import sqlite3
from flask import Flask, app, jsonify
import json

app = Flask(__name__)


def get_data_by_sql(sql):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        result = connection.execute(sql).fetchall()

    return result


@app.get("/movie/<title>/")
def step_1(title):
    result = {}
    for item in get_data_by_sql(sql=f'''
            select title, country, release_year, listed_in as genre, description 
            from netflix 
            where title = '{title}'  
            order by release_year desc limit 1 
            '''):
        result = dict(item)

    return app.response_class(
        json.dumps(result, ensure_ascii=False, indent=4),
        mimetype="application/json",
        status=200
    )


@app.get("/movie/<int:year1>/to/<int:year2>/")
def step_2(year1, year2):
    result = {}
    sql = f'''
        select * from netflix
        where release_year between {year1} and {year2} 
        limit 100 
        '''
    result = []

    for item in get_data_by_sql(sql):
        result.append(dict(item))

    return app.response_class(
        json.dumps(result, ensure_ascii=False, indent=8),
        mimetype="application/json",
        status=200
    )


@app.get("/rating/<rating>/")
def step_3(rating):
    my_rating = {
        "children": ("G", "G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }
    sql = f"""
        select * from netflix
        where rating in {my_rating.get(rating, ("R", "R"))}
        """

    result = []

    for item in get_data_by_sql(sql):
        result.append(dict(item))

    return app.response_class(
        json.dumps(result, ensure_ascii=False, indent=8),
        mimetype="application/json",
        status=200
    )


@app.get("/genre/<genre>/")
def step_4(genre):
    sql = f"""
        select show_id, type from netflix
        where listed_in like '%{str(genre).title()}%' 
        group by
        """

    result = []

    for item in get_data_by_sql(sql):
        result.append(dict(item))

    return app.response_class(
        json.dumps(result, ensure_ascii=False, indent=8),
        mimetype="application/json",
        status=200
    )




def step_5(name1='Rose McIver', name2='Ben Lamb'):
    sql = f'''
        SELECT \"cast\" FROM netflix
        WHERE \"cast\" LIKE '%{name1}%' AND \"cast\" LIKE '%{name2}%'
        '''
    #sql = f'''
        #select "cast" from netflix
        #where "cast" like '%{name1}%' and "cast" like '%{name2}'
        #'''

    names_dict = {}

    for item in get_data_by_sql(sql):
        result = dict(item)

        names = set(result.get('cast').split(", ")) - {name1, name2}

        for name in names:
            names_dict[name.strip()] = names_dict.get(name.strip(), 0) + 1

    print(names_dict)

    for key, value in names_dict.items():
        if value >= 2:
            print(key)




def step_6(types='Movie', year=2020, genre='Horror'):
    sql = f'''
        select * from netflix
        where type = '{types.title()}' and release_year = '{year}' and listed_in like '%{genre.title()}%'
        '''
    result = []

    for item in get_data_by_sql(sql):
        result.append(dict(item))

    return json.dumps(result, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    print(step_6())
