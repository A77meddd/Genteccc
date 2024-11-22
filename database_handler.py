import sqlite3
import os

# الاتصال بقاعدة البيانات وإنشائها إذا لم تكن موجودة
def connect_to_database():
    # تعديل المسار ليشير إلى الموقع الجديد لقاعدة البيانات
    db_path = r'D:\genetic-prediction-app\Data\genetic_data.db'
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # إنشاء الجدول إذا لم يكن موجودًا
        create_table_query = """
        CREATE TABLE IF NOT EXISTS gene_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chromosome TEXT,
            gene_name TEXT,
            gene_position TEXT,
            variation_id TEXT,
            mutation_type TEXT,
            associated_conditions TEXT,
            age TEXT,
            gender TEXT,
            ethnicity TEXT,
            lifestyle_factors TEXT,
            environmental_exposure TEXT,
            disease_severity TEXT,
            inheritance_pattern TEXT
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        return conn

    except sqlite3.OperationalError as e:
        raise sqlite3.OperationalError(f"SQLite error occurred: {e}")

# مثال لإدخال بيانات إلى قاعدة البيانات
def insert_data(data):
    conn = connect_to_database()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO gene_data (
        chromosome, gene_name, gene_position, variation_id,
        mutation_type, associated_conditions, age,
        gender, ethnicity, lifestyle_factors,
        environmental_exposure, disease_severity,
        inheritance_pattern
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """

    cursor.execute(insert_query, data)
    conn.commit()
    conn.close()

# مثال لاسترجاع البيانات من قاعدة البيانات
def get_all_data():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gene_data")
    rows = cursor.fetchall()
    conn.close()
    return rows

# اختبار الكود (تجربة إدخال واسترجاع البيانات)
if __name__ == "__main__":
    try:
        # إدخال بيانات كمثال
        example_data = (
            '1', 'NRAS', '1p13.2', 'c.182A>G', 'Missense', 
            'Cancer', 'Late adulthood(40-60)', 'Male & Female',
            'Caucasian, Asian', 'Healthy diet, avoiding smoking and alcohol',
            'Radiation, carcinogens', 'High', 'Autosomal Dominant'
        )
        insert_data(example_data)

        # استرجاع البيانات وعرضها
        all_data = get_all_data()
        for row in all_data:
            print(row)

    except FileNotFoundError as e:
        print(e)
    except sqlite3.OperationalError as e:
        print(f"SQLite error occurred: {e}")
