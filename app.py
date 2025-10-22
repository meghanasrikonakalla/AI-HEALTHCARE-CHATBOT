from flask import Flask, render_template, request, jsonify, session, flash, redirect, url_for
from functools import wraps
from flask_session import Session
import re, random, pandas as pd, numpy as np, csv, warnings, os
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from difflib import get_close_matches

warnings.filterwarnings("ignore", category=DeprecationWarning)
app = Flask(__name__)
app.secret_key = "supersecret"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# ------------------ Load Data (with error handling) ------------------
try:
    training = pd.read_csv('Data/Training.csv')
    testing = pd.read_csv('Data/Testing.csv')
    print("Success: Training and testing data loaded successfully")
except FileNotFoundError as e:
    print(f"Error: Could not find data files: {e}")
    print("Please ensure Data/Training.csv and Data/Testing.csv exist")
    exit(1)
except Exception as e:
    print(f"Error loading data: {e}")
    exit(1)

training.columns = training.columns.str.replace(r"\.\d+$", "", regex=True)
testing.columns  = testing.columns.str.replace(r"\.\d+$", "", regex=True)
training = training.loc[:, ~training.columns.duplicated()]
testing  = testing.loc[:, ~testing.columns.duplicated()]
cols = training.columns[:-1]
x = training[cols]
y = training['prognosis']
le = preprocessing.LabelEncoder()
y = le.fit_transform(y)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(x_train, y_train)
print("Success: ML Model trained successfully")

# Dictionaries
severityDictionary, description_list, precautionDictionary = {}, {}, {}
symptoms_dict = {symptom: idx for idx, symptom in enumerate(x)}

def getDescription():
    try:
        with open('MasterData/symptom_Description.csv') as csv_file:
            for row in csv.reader(csv_file):
                if len(row) >= 2:
                    description_list[row[0]] = row[1]
        print("Success: Symptom descriptions loaded successfully")
    except FileNotFoundError:
        print("Warning: symptom_Description.csv not found")
    except Exception as e:
        print(f"Error loading descriptions: {e}")

def getSeverityDict():
    try:
        with open('MasterData/symptom_severity.csv') as csv_file:
            for row in csv.reader(csv_file):
                try: 
                    if len(row) >= 2:
                        severityDictionary[row[0]] = int(row[1])
                except: pass
        print("Success: Severity dictionary loaded successfully")
    except FileNotFoundError:
        print("Warning: symptom_severity.csv not found")
    except Exception as e:
        print(f"Error loading severity data: {e}")

def getprecautionDict():
    try:
        with open('MasterData/symptom_precaution.csv') as csv_file:
            for row in csv.reader(csv_file):
                if len(row) >= 5:
                    precautionDictionary[row[0]] = [row[1], row[2], row[3], row[4]]
        print("Success: Precaution dictionary loaded successfully")
    except FileNotFoundError:
        print("Warning: symptom_precaution.csv not found")
    except Exception as e:
        print(f"Error loading precaution data: {e}")

getSeverityDict(); getDescription(); getprecautionDict()

symptom_synonyms = {
    "stomach ache":"stomach_pain","belly pain":"stomach_pain","tummy pain":"stomach_pain",
    "loose motion":"diarrhea","motions":"diarrhea","high temperature":"fever",
    "temperature":"fever","feaver":"fever","coughing":"cough","throat pain":"sore_throat",
    "cold":"chills","breathing issue":"breathlessness","shortness of breath":"breathlessness",
    "body ache":"muscle_pain"
}

def extract_symptoms(user_input, all_symptoms):
    extracted = []
    text = user_input.lower().replace("-", " ")
    for phrase, mapped in symptom_synonyms.items():
        if phrase in text: extracted.append(mapped)
    for symptom in all_symptoms:
        if symptom.replace("_"," ") in text: extracted.append(symptom)
    words = re.findall(r"\w+", text)
    for word in words:
        close = get_close_matches(word, [s.replace("_"," ") for s in all_symptoms], n=1, cutoff=0.8)
        if close:
            for sym in all_symptoms:
                if sym.replace("_"," ") == close[0]:
                    extracted.append(sym)
    return list(set(extracted))

def predict_disease(symptoms_list):
    input_vector = np.zeros(len(symptoms_dict))
    for symptom in symptoms_list:
        if symptom in symptoms_dict:
            input_vector[symptoms_dict[symptom]] = 1
    pred_proba = model.predict_proba([input_vector])[0]
    pred_class = np.argmax(pred_proba)
    disease = le.inverse_transform([pred_class])[0]
    confidence = round(pred_proba[pred_class]*100,2)
    return disease, confidence, pred_proba

quotes = [
    "🌸 Health is wealth, take care of yourself.",
    "💪 A healthy outside starts from the inside.",
    "☀️ Every day is a chance to get stronger and healthier.",
    "🌿 Take a deep breath, your health matters the most.",
    "🌺 Remember, self-care is not selfish."
]

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('Data/users.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == username and row[1] == password:
                    session['user'] = username
                    flash('Logged in successfully!', 'success')
                    return redirect(url_for('index'))
        flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            # Validate that all required fields are present
            if not all([name, email, username, password, confirm_password]):
                flash('All fields are required.', 'error')
                return render_template('signup.html')
            
            if password != confirm_password:
                flash('Passwords do not match.', 'error')
                return render_template('signup.html')
            
            # Create users.csv if it doesn't exist
            if not os.path.exists('Data/users.csv'):
                with open('Data/users.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['username', 'password', 'name', 'email'])
            
            # Check for existing username/email
            existing_users = []
            try:
                with open('Data/users.csv', 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)  # Skip header row
                    existing_users = list(reader)
            except Exception as e:
                print(f"Error reading users.csv: {e}")
                existing_users = []
            
            # Check for duplicate username/email
            for row in existing_users:
                if row and len(row) > 0 and row[0] == username:
                    flash('Username already exists.', 'error')
                    return render_template('signup.html')
                if row and len(row) > 2 and row[2] == email:
                    flash('Email already registered.', 'error')
                    return render_template('signup.html')
            
            # Add new user
            try:
                with open('Data/users.csv', 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([username, password, name, email])
                print(f"Successfully added user: {username}")
                flash('Account created successfully! Please log in.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                print(f"Error writing to users.csv: {e}")
                flash('An error occurred while creating your account. Please try again.', 'error')
                return render_template('signup.html')
                
        except Exception as e:
            print(f"Signup error: {e}")
            flash('An error occurred. Please try again.', 'error')
            return render_template('signup.html')
            
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# ------------------ Routes ------------------
@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('index'))
    return render_template('home.html')

@app.route('/chatbot')
@login_required
def index():
    session['step'] = 'welcome'
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if 'user' not in session:
        return jsonify(reply="You have been logged out. Please log in again.")
    try:
        user_msg = request.json['message'].strip()
        step = session.get('step', 'welcome')
        
        if not user_msg:
            return jsonify(reply="Please enter a valid message.")

        # replicate each console step
        if step == 'welcome':
            session['step'] = 'name'
            return jsonify(reply="🤖 Welcome to HealthCare ChatBot!\n👉 What is your name?")
        elif step == 'name':
            session['name'] = user_msg
            session['step'] = 'age'
            return jsonify(reply=f"Nice to meet you {user_msg}! 👉 Please enter your age:")
        elif step == 'age':
            try:
                age = int(user_msg)
                if age <= 0 or age > 150:
                    return jsonify(reply="Please enter a valid age between 1 and 150:")
                session['age'] = user_msg
                session['step'] = 'gender'
                return jsonify(reply="👉 What is your gender? (M/F/Other):")
            except ValueError:
                return jsonify(reply="Please enter a valid number for your age:")
        elif step == 'gender':
            if user_msg.upper() not in ['M', 'F', 'MALE', 'FEMALE', 'OTHER']:
                return jsonify(reply="Please enter M, F, or Other for gender:")
            session['gender'] = user_msg
            session['step'] = 'symptoms'
            return jsonify(reply="👉 Describe your symptoms in a sentence (e.g., 'I have fever and headache'):")
        elif step == 'symptoms':
            symptoms_list = extract_symptoms(user_msg, cols)
            if not symptoms_list:
                return jsonify(reply="❌ Could not detect valid symptoms from your description. Please try again with symptoms like 'fever', 'headache', 'cough', etc.:")
            session['symptoms'] = symptoms_list
            disease, conf, _ = predict_disease(symptoms_list)
            session['pred_disease'] = disease
            session['step'] = 'days'
            return jsonify(reply=f"✅ Detected symptoms: {', '.join([s.replace('_', ' ') for s in symptoms_list])}\n👉 For how many days have you had these symptoms?")
        elif step == 'days':
            try:
                days = int(user_msg)
                if days <= 0:
                    return jsonify(reply="Please enter a positive number of days:")
                session['days'] = user_msg
                session['step'] = 'severity'
                return jsonify(reply="👉 On a scale of 1–10, how severe is your condition? (1=mild, 10=severe)")
            except ValueError:
                return jsonify(reply="Please enter a valid number of days:")
        elif step == 'severity':
            try:
                severity = int(user_msg)
                if severity < 1 or severity > 10:
                    return jsonify(reply="Please enter a number between 1 and 10:")
                session['severity'] = user_msg
                session['step'] = 'preexist'
                return jsonify(reply="👉 Do you have any pre-existing conditions? (yes/no)")
            except ValueError:
                return jsonify(reply="Please enter a number between 1 and 10:")
        elif step == 'preexist':
            session['preexist'] = user_msg
            session['step'] = 'lifestyle'
            return jsonify(reply="👉 Do you smoke, drink alcohol, or have irregular sleep? (yes/no)")
        elif step == 'lifestyle':
            session['lifestyle'] = user_msg
            session['step'] = 'family'
            return jsonify(reply="👉 Any family history of similar illness? (yes/no)")
        elif step == 'family':
            session['family'] = user_msg
            # guided disease-specific questions
            disease = session['pred_disease']
            disease_symptoms = list(training[training['prognosis'] == disease].iloc[0][:-1].index[
                training[training['prognosis'] == disease].iloc[0][:-1] == 1
            ])
            session['disease_syms'] = disease_symptoms
            session['ask_index'] = 0
            session['step'] = 'guided'
            return ask_next_symptom()
        elif step == 'guided':
            # record yes/no
            idx = session['ask_index'] - 1
            if idx >= 0 and idx < len(session['disease_syms']):
                if user_msg.strip().lower() in ['yes', 'y']:
                    if session['disease_syms'][idx] not in session['symptoms']:
                        session['symptoms'].append(session['disease_syms'][idx])
            return ask_next_symptom()
        elif step == 'final':
            # already answered all guided
            return final_prediction()
        else:
            return jsonify(reply="Something went wrong. Let's start over.")
            
    except Exception as e:
        print(f"Error in chat route: {e}")
        return jsonify(reply="❌ An error occurred. Please try again."), 500

def ask_next_symptom():
    i = session['ask_index']
    ds = session['disease_syms']
    if i < min(8, len(ds)):
        sym = ds[i]
        session['ask_index'] += 1
        return jsonify(reply=f"👉 Do you also have {sym.replace('_',' ')}? (yes/no):")
    else:
        session['step'] = 'final'
        return final_prediction()

def final_prediction():
    try:
        disease, conf, _ = predict_disease(session['symptoms'])
        about = description_list.get(disease, 'No description available.')
        precautions = precautionDictionary.get(disease, [])
        
        # Enhanced result formatting
        text = (f"🩺 **Medical Assessment Results**\n\n"
                f"**Patient:** {session.get('name', 'Unknown')}\n"
                f"**Age:** {session.get('age', 'Unknown')}\n"
                f"**Gender:** {session.get('gender', 'Unknown')}\n\n"
                f"**Predicted Condition:** {disease}\n"
                f"**Confidence Level:** {conf}%\n\n"
                f"**Description:** {about}\n")
        
        if precautions:
            text += "\n**🛡️ Recommended Precautions:**\n"
            for i, p in enumerate(precautions):
                if p.strip():  # Only add non-empty precautions
                    text += f"{i+1}. {p}\n"
        
        # Add health tips based on severity
        severity = int(session.get('severity', 5))
        if severity >= 8:
            text += "\n⚠️ **URGENT:** Your symptoms appear severe. Please consult a healthcare professional immediately.\n"
        elif severity >= 6:
            text += "\n⚡ **IMPORTANT:** Consider consulting a healthcare professional soon.\n"
        else:
            text += "\n💡 **Note:** Monitor your symptoms and consult a doctor if they worsen.\n"
        
        text += f"\n{random.choice(quotes)}"
        text += f"\n\n**Disclaimer:** This is an AI-based assessment and should not replace professional medical advice.\n"
        text += f"\nThank you for using our healthcare chatbot, {session.get('name', 'User')}! 🌟"
        
        # Store session data for potential follow-up
        session['consultation_complete'] = True
        
        return jsonify(reply=text)
    except Exception as e:
        print(f"Error in final prediction: {e}")
        return jsonify(reply="❌ An error occurred while generating your assessment. Please try again.")

# Add a new route for restarting consultation
@app.route('/restart', methods=['POST'])
def restart_consultation():
    session.clear()
    session['step'] = 'welcome'
    return jsonify(reply="🔄 Session restarted. Let's begin a new consultation!\n🤖 Welcome to HealthCare ChatBot!\n👉 What is your name?")

# Add error handler
@app.errorhandler(500)
def internal_error(error):
    return jsonify(reply="❌ Internal server error. Please try again later."), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify(reply="❌ Page not found."), 404

if __name__ == '__main__':
    print("Starting Healthcare Chatbot Application...")
    print("Loading data and initializing ML model...")
    print("Server will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    try:
        app.run(
            host='127.0.0.1',  # Use 127.0.0.1 for better compatibility
            port=5000,
            debug=False,  # Disable debug mode for stability
            use_reloader=False,  # Disable reloader for stability
            threaded=True  # Enable threading
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
