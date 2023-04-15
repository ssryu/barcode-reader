import os
import sqlite3

import openpyxl as excel


class DatabaseManager:
    def __init__(
        self,
        database_path="stock.db",
        excel_book_path="stock.xlsx",
    ):
        current_directory = os.path.dirname(__file__)
        self.database_path = os.path.join(current_directory, database_path)
        self.excel_book_path = os.path.join(current_directory, excel_book_path)

        self.connection = sqlite3.connect(self.database_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def select_all(self):
        self.cursor.execute("SELECT * FROM food")
        rows = []

        for row in self.cursor.fetchall():
            rows.append(
                {
                    "jan": row["jan"],
                    "product_name": row["product_name"],
                    "stock": row["stock"],
                    "lower": row["lower"],
                }
            )

        return rows

    def update_stock(self, code, quantity):
        result = self.cursor.execute(
            "UPDATE food SET stock = stock + ? WHERE jan = ?", (quantity, code)
        )
        self.connection.commit()
        return result.rowcount

    def check_alert(self, code):
        return self.cursor.execute(
            "SELECT product_name FROM food WHERE jan = ? AND stock = lower", (code,)
        ).fetchone()

    def export_excel(self):
        wb = excel.Workbook()
        ws = wb.active
        result = self.cursor.execute("SELECT * FROM food")
        header = [d[0] for d in self.cursor.description]
        ws.append(header)

        for r in result.fetchall():
            ws.append((r[0], r[1], r[2], r[3]))

        wb.save(self.excel_book_path)

    def close(self):
        self.cursor.close()
        self.connection.close()
