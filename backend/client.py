import os
import random

from backend.admin import connection

from backend.data import load_sudent_data, load_languages

DB = "questalliance.db"


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
        CREATE IF NOT EXIST TABLE courses ();
        """
    conn.execute(sql);


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


def seed():
    if os.path.exists(DB):
        os.remove(DB)
    total_students = upload_student_data(DB)
    total_languages = upload_languages(DB)
    upload_language_known(DB, total_students, total_languages)

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


def main():
    # total_students = seed()
    # validate_seed(total_students, view=10)
    mark_survey_complete(DB, [3, 4])


if __name__ == '__main__':
    main()
