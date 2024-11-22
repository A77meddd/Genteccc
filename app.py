import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from flask import Flask, request, render_template

app = Flask(__name__)

# قراءة البيانات من ملف CSV
data = pd.read_csv('Genetic_Prediction_Template.csv', delimiter=';')
data.columns = data.columns.str.strip()  # إزالة المسافات الزائدة

# تنظيف البيانات ومعالجة القيم المفقودة
data.dropna(subset=['Gene Name', 'Chromosome', 'Variation ID', 'Mutation Effect'], inplace=True)

# تحويل البيانات النصية إلى قيم رقمية
label_encoder = LabelEncoder()
columns_to_encode = ['Mutation Type', 'Mutation Effect', 'Gene Name', 'Chromosome', 'Gene Position', 'Variation ID']

for col in columns_to_encode:
   if col in data.columns:
       data[col] = label_encoder.fit_transform(data[col])

X = data[['Gene Name', 'Chromosome', 'Gene Position', 'Variation ID', 'Mutation Type']]
y = data['Mutation Effect']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

@app.route('/')
def home():
   return render_template('welcome.html')

@app.route('/predict', methods=['POST'])
def predict():
   gene_name = request.form['gene_name']
   chromosome = request.form['chromosome']
   gene_position = request.form['gene_position']
   variation_id = request.form['variation_id']
   mutation_type = request.form['mutation_type']

   input_data = pd.DataFrame({
       'Gene Name': [label_encoder.transform([gene_name])[0]],
       'Chromosome': [label_encoder.transform([chromosome])[0]],
       'Gene Position': [label_encoder.transform([gene_position])[0]],
       'Variation ID': [label_encoder.transform([variation_id])[0]],
       'Mutation Type': [label_encoder.transform([mutation_type])[0]]
   })

   prediction = model.predict(input_data)
   result_text = label_encoder.inverse_transform([prediction[0]])[0]
   
   return render_template('result.html', result=result_text)

if __name__ == '__main__':
   app.run(debug=True)