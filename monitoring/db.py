"""
db.py
~~~~~

Raw PostgreSQL implementation of the DB Model.

"""
import psycopg2
from psycopg2.extras import DictCursor
from monitoring.settings import cfg
from monitoring.check_models import CheckResult


class DB:
    def __init__(self):
        self.conn = psycopg2.connect(cfg["postgresql_uri"])
        self.cur = self.conn.cursor(cursor_factory=DictCursor)
        self.setup_db()

    def setup_db(self):
        """ Create initial DB structure """
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS checks (
                check_id SERIAL PRIMARY KEY,
                url VARCHAR(4096),
                regexp VARCHAR(255),
                expected_code INTEGER,
                created TIMESTAMP,
                last_check TIMESTAMP,
                UNIQUE(url, regexp, expected_code)
            )
            """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS results (
                result_id BIGSERIAL PRIMARY KEY,
                check_id INTEGER REFERENCES checks(check_id),
                success BOOLEAN,
                code INTEGER,
                length INTEGER,
                response_time NUMERIC(7, 3),
                created TIMESTAMP
            );
            """
        )
        self.conn.commit()

    def enumerate_checks(self):
        self.cur.execute("SELECT * FROM checks")
        return self.cur.fetchall()

    def enumerate_results(self):
        self.cur.execute("SELECT * FROM results")
        return self.cur.fetchall()

    def add_check_result(self, result: CheckResult):
        """ Creates result entry with a proper check_id """
        check_id = self._create_or_update_check(result)

        self.cur.execute(
            """INSERT INTO results (check_id, success, code, length, response_time, created)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING result_id""",
            (
                check_id,
                result.success,
                result.response_code,
                result.response_length,
                result.response_time,
                result.created,  # last_check = created
            ),
        )
        self.conn.commit()

    def _create_or_update_check(self, result: CheckResult):
        """ Creates or updates check entry. Returns check_id """
        self.cur.execute(
            "SELECT check_id FROM checks WHERE url=%s AND regexp=%s AND expected_code=%s",
            (
                result.url,
                result.regexp,
                result.expected_code,
            ),
        )
        row = self.cur.fetchone()
        if row:
            check_id = row[0]
            self.cur.execute(
                "UPDATE checks SET last_check=%s WHERE check_id=%s",
                (
                    result.created,
                    check_id,
                ),
            )
        else:
            self.cur.execute(
                """INSERT INTO checks (url, regexp, expected_code, created, last_check)
                VALUES (%s, %s, %s, %s, %s) RETURNING check_id""",
                (
                    result.url,
                    result.regexp,
                    result.expected_code,
                    result.created,
                    result.created,  # last_check = created
                ),
            )
            check_id = self.cur.fetchone()[0]
        return check_id
