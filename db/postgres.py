from pathlib import Path
import psycopg

from core import config


class PostgresDB:
    def __init__(self, dsn: str | None = None, schema_filename: str = "001_schema.sql"):
        self.dsn = dsn or config.postgres_url
        self.schema_path = (Path(__file__).parent / "sql" / schema_filename).resolve()

    @staticmethod
    def _read_sql_file(path: Path) -> str:
        if not path.exists():
            raise FileNotFoundError(f"SQL file not found: {path}")
        return path.read_text(encoding="utf-8")

    def init_db(self) -> None:
        """Apply db/sql/001_schema.sql (idempotent)."""
        sql_text = self._read_sql_file(self.schema_path)
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_text)  # type: ignore[arg-type]
        print(f"Applied schema: {self.schema_path.name}")

    def execute(self, sql: str, params: tuple | None = None) -> None:
        """Run a single INSERT/UPDATE/DELETE/DDL."""
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params or ())

    def executemany(self, sql: str, param_list: list[tuple]) -> None:
        """Run the same statement for many rows (useful for bulk migrate)."""
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                for params in param_list:
                    cur.execute(sql, params)

    def fetchall(self, sql: str, params: tuple | None = None) -> list[tuple]:
        """Fetch all rows from SELECT."""
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params or ())
                return cur.fetchall()


if __name__ == "__main__":
    PostgresDB().init_db()
