from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'  # MySQL server address
app.config['MYSQL_USER'] = 'd'  # MySQL username
app.config['MYSQL_PASSWORD'] = '123456'  # MySQL password
app.config['MYSQL_DB'] = 'survey_db'  # MySQL database name

mysql = MySQL(app)

@app.route('/simulate-load', methods=['POST'])
def simulate_load():
    # Simulate high CPU load
    result = 0
    for i in range(10000):
        for j in range(10000):
            result += i * j

    return "CPU load simulation complete!"

@app.route('/', methods=['GET', 'POST'])
def survey():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM survey_questions')
    survey_questions = cur.fetchall()
    cur.close()

    if request.method == 'POST':
    
        # Handle the survey submission
        
        name = request.form.get('name')
        response = {}
        
        for question in survey_questions:
            question_id = question[0]
            question_text = question[1]
            selected_option = request.form.get(str(question_id))
            response[question_text] = selected_option

        cur = mysql.connection.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS survey_responses (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                response TEXT NOT NULL
            )
        ''')
        cur.execute('''
            INSERT INTO survey_responses (name, response)
            VALUES (%s, %s)
        ''', (name, str(response)))
        mysql.connection.commit()
        cur.close()

        return "Thank you for completing the survey!"
    else:
        # Display the survey form
        return render_template('survey.html', questions=survey_questions)


if __name__ == '__main__':
    app.run(debug=True)



















