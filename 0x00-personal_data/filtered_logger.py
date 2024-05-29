#!/usr/bin/env python3
"""filtered_logger module"""
import logging,re
from logging import StreamHandler
import os
import mysql.connector

def filter_datum(fields: list[str], redaction: str, message: str, separator: str) -> str:
        return re.sub(f'(?<=^|{separator})({"|".join(fields)})=[^{separator}]+', f'{redaction}', message)

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        filtered_values = map(self.filter_datum, [getattr(record, field, '') for field in self.fields])
        record.msg = self.SEPARATOR.join(filtered_values)
        return super().format(record)
    
    def filter_datum(self, field: str) -> str:
        return filter_datum(self.fields, self.REDACTION, field, self.SEPARATOR)

PII_FIELDS = ('name','email', 'phone', 'ssn', 'password')

def get_logger() -> logging.Logger:
    """ get_logger function """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    try:
        connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
        )
        print("Connection to database established")
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        exit(e)

def main():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    for row in cursor:
        print(row)
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()  # python3 0x00-personal_data/filtered_logger.py
    
