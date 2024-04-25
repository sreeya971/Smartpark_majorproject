from flask import Flask, render_template, request, session, redirect, url_for, g
import cv2
import pickle
import cvzone
import numpy as np
import sqlite3

app = Flask(__name__)
app.secret_key = 'a'

# Connect to SQLite database (create a new database if it doesn't exist)
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Create a table if it doesn't exist
def init_db():
    with app.app_context():
        db = get_db()
        with db:
            db.execute('''
                CREATE TABLE IF NOT EXISTS REGISTER (
                    NAME TEXT,
                    EMAIL TEXT PRIMARY KEY,
                    PASSWORD TEXT
                )
            ''')

@app.route('/')
def project():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/model')
def model():
    return render_template('model.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/aboutus.html')
def aboutus():
    return render_template('aboutus.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

@app.route("/signup", methods=['POST', 'GET'])
def signup1():
    msg = ''
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        cursor = get_db().cursor()
        insert_sql = "INSERT INTO REGISTER (NAME, EMAIL, PASSWORD) VALUES (?, ?, ?)"
        cursor.execute(insert_sql, (name, email, password))
        get_db().commit()
        msg = "You have successfully registered!"
    return render_template('login.html', msg=msg)

@app.route("/login", methods=['POST', 'GET'])
def login1():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        cursor = get_db().cursor()
        sql = "SELECT * FROM REGISTER WHERE EMAIL=? AND PASSWORD=?"
        cursor.execute(sql, (email, password))
        account = cursor.fetchone()
        if account:
            session['Loggedin'] = True
            session['id'] = account[1]
            session['email'] = account[1]
            return render_template('model.html')
        else:
            msg = "Incorrect Email/password"
            return render_template('login.html', msg=msg)
    else:
        return render_template('login.html')

@app.route('/modelq')
def liv_pred():
    # Initialize webcam feed
    cap = cv2.VideoCapture(0, cv2.CAP_ANY)

    # Load parking position data
    with open('carParkPos', 'rb') as f:
        posList = pickle.load(f)
    width, height = 107, 48

    # Function to check parking spaces
    def checkParkingSpace(imgPro):
        spaceCounter = 0
        for pos in posList:
            x, y = pos
            imgCrop = imgPro[y:y + height, x:x + width]
            count = cv2.countNonZero(imgCrop)
            if count < 900:
                color = (0, 255, 0)
                thickness = 5
                spaceCounter += 1
            else:
                color = (0, 0, 255)
                thickness = 2
            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
            cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                               thickness=2, offset=0, colorR=color)
        cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3, thickness=5, offset=20,
                           colorR=(0, 200, 0))

    while True:
        # Capture frame-by-frame
        success, img = cap.read()

        # Break the loop if frame is not read successfully
        if not success:
            break

        # Preprocessing steps
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
        imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                             25, 16)
        imgMedian = cv2.medianBlur(imgThreshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

        # Check parking spaces
        checkParkingSpace(imgDilate)

        # Display the frame
        cv2.imshow("Image", img)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    return redirect(url_for('model'))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
