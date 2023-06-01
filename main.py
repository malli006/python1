from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client['task2']
task3 = db['excel_data']

@app.route('/')
def index():
    data = task3.find()
    return render_template('index.html', data=data)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    rollno = request.form.get('rollno')
    year = request.form.get('year')
    interestedinGCC = request.form.get('interestedinGCC')

    # Store the data in MongoDB
    data = {'name': name, 'rollno': rollno, 'year': year, 'interestedinGCC': interestedinGCC}
    task3.insert_one(data)
    return 'Data submitted successfully!'

@app.route('/chart')
def chart():
    # Retrieve the data from MongoDB
    data = task3.find({}, {'_id': 0, 'interestedinGCC': 1})

    # Count the number of 'Yes' and 'No' responses
    yes_count = 0
    no_count = 0
    for doc in data:
        if 'interestedinGCC' in doc:
            if doc['interestedinGCC'] == 'yes':
                yes_count += 1
            elif doc['interestedinGCC'] == 'no':
                no_count += 1

    # Prepare the data for the pie chart
    labels = ['Interested in GCC', 'Not Interested in GCC']
    data = [yes_count, no_count]

    return render_template('chart.html', labels=labels, data=data)

if __name__ == '__main__':
    app.run(debug=True)
