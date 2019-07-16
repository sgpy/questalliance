import os
import random
from functools import partial

from admin import connection

from data import load_sudent_data, load_languages, load_courses

DB = "/Users/vinay/Sites/questalliance/backend/questalliance.db"

COURSES = ["tk_pk_id",  "tk_tags", "tk_name", "tk_description", "language", "url", "tk_image"]

@connection
def create_user_table(conn):
    sql = \
        """
        CREATE TABLE IF NOT EXISTS users (stud_pk_id INTEGER PRIMARY KEY AUTOINCREMENT, stud_first_name VARCHAR(50), stud_gender char(1), nationality varchar(50), survey_status char(1) DEFAULT "0");
        """
    conn.execute(sql);
    pass

@connection
def create_course_table(conn):
    sql = \
        """
        CREATE TABLE IF NOT EXISTS courses (tk_pk_id INTEGER PRIMARY KEY AUTOINCREMENT,  tk_tags VARCHAR(50) DEFAULT "", tk_name VARCHAR(50) DEFAULT "", tk_description VARCHAR(50) DEFAULT "", language VARCHAR(50) DEFAULT "", url VARCHAR(100)  DEFAULT "", tk_image BLOB  DEFAULT "");
        """
    conn.execute(sql);
    pass


@connection
def create_language_table(conn):
    sql = \
        """
        CREATE TABLE IF NOT EXISTS languages (lang_pk_id INTEGER PRIMARY KEY AUTOINCREMENT, language VARCHAR(50));
        """
    conn.execute(sql);


@connection
def create_language_known(conn):
    sql = \
        """
        CREATE TABLE IF NOT EXISTS languages_known (stud_pk_id INTEGER, lang_pk_id INTEGER, FOREIGN KEY (stud_pk_id) REFERENCES users(stud_pk_id));
        """
    conn.execute(sql);


@connection
def upload_student_data(conn):
    create_user_table(DB)
    rs = load_sudent_data()
    sql = \
        """
        INSERT INTO users (stud_first_name, stud_gender, nationality) VALUES (?, ?, ?); 
        """
    with conn:
        for _ in rs:
            conn.execute(sql, _)
    return len(rs)


@connection
def upload_languages(conn):
    create_language_table(DB)

    rs = load_languages()
    sql = \
        """
        INSERT INTO languages (language) VALUES (?); 
        """
    with conn:
        for _ in rs:
            conn.execute(sql, (_[1],))

    return len(rs)


@connection
def add_language_known(conn, elems):
    create_language_known(conn)
    sql = \
        """
        INSERT INTO languages_known (stud_pk_id, lang_pk_id) VALUES (?, ?);
        """
    with conn:
        for elem in elems:
            conn.execute(sql, elem)


@connection
def users_info(conn, users):
    sql = \
        """
        SELECT stud_pk_id, stud_first_name, survey_status FROM users WHERE stud_pk_id in ({});
        """

    sql = sql.format(str(users)[1:-1])
    # print(sql)
    cols = tuple(map(lambda x: x.strip(), "stud_pk_id, stud_first_name, survey_status".split(",")))
    all_users = {}

    for data in conn.execute(sql):
        all_users[data[0]] = dict(zip(cols, data))
        all_users[data[0]]['languages_known'] = []

    sql = \
        """
        SELECT x.stud_pk_id, language FROM(
            (SELECT stud_pk_id, lang_pk_id FROM languages_known WHERE stud_pk_id in ({}) ) x
            INNER JOIN 
            languages y
            ON x.lang_pk_id = y.lang_pk_id
        );
        """

    sql = sql.format(str(users)[1:-1])

    for user_id, language in tuple(conn.execute(sql)):
        all_users[user_id]['languages_known'].append(language)

    return all_users


def upload_language_known(db, total_students, total_languages):
    rs = []
    max_language_known = 5
    for i in range(1, total_students + 1):
        language_known = random.randint(1, max_language_known)
        for _ in range(0, language_known):
            j = random.randint(1, total_languages + 1)
            rs.append((i, j))
    add_language_known(db, rs)


def validate_seed(total_students, view=10):
    users = [random.randint(1, total_students + 1) for _ in range(0, view)]
    for _, user_info in users_info(DB, users).items():
        print(user_info)

find_user_info = partial(users_info, DB)

def seed():
    if os.path.exists(DB):
        os.remove(DB)
    total_students = upload_student_data(DB)
    total_languages = upload_languages(DB)
    upload_language_known(DB, total_students, total_languages)

    upload_course_data(DB)
    return total_students


@connection
def mark_survey_complete(conn, user_ids):
    if not user_ids:
        return
    if not isinstance(user_ids, (list, tuple)):
        user_ids = [user_ids]

    sql = \
        """
        UPDATE  users SET survey_status = "1" WHERE stud_pk_id = ?
        """
    with conn:
        for user_id in user_ids:
            conn.execute(sql, (user_id,))

survey_complete = partial(mark_survey_complete, DB)

@connection
def upload_course_data(conn):
    create_course_table(DB)
    data = load_courses()
    sql = \
    """
    INSERT INTO courses ({}) VALUES ({})
    """




    for row in data:

        if len(row) > len(COURSES):
            row = row[:len(COURSES)]

        # row = [_.strip() for _ in row]
        data_size = len(row)
        cols = COURSES[0:data_size]
        cols_placeholders = ",".join(["?" for _ in range(0, len(cols))])
        sql = sql.format(str(cols)[1:-1], cols_placeholders)
        with conn:
            conn.execute(sql, row)
@connection
def courses(conn, tags):


    sql = \
    """
    SELECT * FROM courses WHERE tk_tags IN ({})
    """
    sql = sql.format(str(tags)[1:-1])
    print(sql)
    with conn:
        rs = conn.execute(sql)

    result = []
    for _ in rs:
        result.append(dict(zip(COURSES, _)))
    return  result

search_courses = partial(courses, DB)

def main():
    # total_students = seed()
    pass




if __name__ == '__main__':
    main()
