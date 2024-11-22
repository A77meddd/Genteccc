from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# الاتصال بقاعدة البيانات وإنشائها إذا لم تكن موجودة
def connect_to_database():
    db_path = 'genetic_data.db'  # سيتم إنشاء قاعدة البيانات في نفس مسار المشروع
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gene_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chromosome TEXT,
                gene_name TEXT,
                gene_position TEXT,
                variation_id TEXT,
                age TEXT,
                gender TEXT
            )
        """)
        conn.commit()
        conn.close()
    return sqlite3.connect(db_path)

# نقطة نهاية لإدخال البيانات الجديدة
@app.route('/submit-data', methods=['POST'])
def submit_data():
    data = request.json
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO gene_data (chromosome, gene_name, gene_position, variation_id, age, gender)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_query, (
            data['chromosome'], data['gene_name'], data['gene_position'],
            data['variation_id'], data['age'], data['gender']
        ))
        conn.commit()
        conn.close()
        return jsonify({"message": "Data inserted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# نقطة نهاية لاسترجاع جميع البيانات
@app.route('/get-data', methods=['GET'])
def get_all_data():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gene_data")
        rows = cursor.fetchall()
        conn.close()

        result = [dict(zip(['id', 'chromosome', 'gene_name', 'gene_position', 'variation_id', 'age', 'gender'], row)) for row in rows]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
