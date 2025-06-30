from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Dummy user store for demo purpose
users = {}

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        contact = request.form['contact']
        emergency = request.form['emergency']
        password = request.form['password']
        city=request.form['city']
        language=request.form['language']
        
        users[contact] = {
            'name': name,
            'address': address,
            'email': email,
            'emergency': emergency,
            'password': password,
            'city': city,
            'language': language
        }
        flash('Account created! Please login.')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        contact = request.form['contact']
        password = request.form['password']
        
        if contact in users and users[contact]['password'] == password:
            session['user'] = users[contact]['name']
            return redirect('/period')
        else:
            flash('Incorrect contact number or password!')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/period')
def period():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('period.html', user=session['user'])

@app.route('/pcod')
def pcod():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('pcod.html', user=session['user'])

@app.route('/tools')
def tools():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('tools.html', user=session['user'])

@app.route('/tracker', methods=['POST'])
def tracker():
    note = request.form['track_note']
    flash(f"Tracker saved: {note}")
    return redirect(url_for('tools'))

@app.route('/advice', methods=['POST'])
def advice():
    user_input = request.form.get('user_problem') or request.form.get('common_issue')
    want_yoga = request.form.get('want_yoga')

    response = ""
    yoga = ""

    if 'irregular' in user_input.lower():
        response = "Try to maintain a regular sleep schedule and manage stress."
        if want_yoga == "yes":
            yoga = "Cobra Pose, Child’s Pose"
    elif 'weight' in user_input.lower():
        response = "Focus on a low-GI diet and regular exercise."
        if want_yoga == "yes":
            yoga = "Warrior Pose, Bow Pose"
    elif 'mood' in user_input.lower() or 'stress' in user_input.lower():
        response = "Mindfulness and relaxation practices are key."
        if want_yoga == "yes":
            yoga = "Cat-Cow Pose, Breathing Exercises"
    elif 'pain' in user_input.lower() or 'cramp' in user_input.lower():
        response = "Heat therapy and hydration can help a lot."
        if want_yoga == "yes":
            yoga = "Butterfly Pose, Supine Twist"
    else:
        response = "Please consult a gynecologist for more specific guidance."
        if want_yoga == "yes":
            yoga = "Shavasana, Basic stretching and breathing"

    return render_template('tools.html', user=session['user'], advice=response, yoga=yoga)

@app.route('/pregnancy', methods=['POST'])
def pregnancy():
    symptoms = request.form['pregnancy_symptoms'].lower()

    high_risk_keywords = ['irregular', 'obesity', 'weight', 'hormonal', 'insulin', 'cyst', 'stress']
    risky = any(keyword in symptoms for keyword in high_risk_keywords)

    if risky:
        prediction = "⚠️ Based on your symptoms, pregnancy may be more difficult. Please consult a doctor and follow healthy lifestyle practices strictly."
    else:
        prediction = "✅ Your symptoms don’t indicate a high-risk pregnancy, but regular check-ups are still recommended."

    return render_template('tools.html', user=session['user'], pregnancy_result=prediction)



@app.route('/diet', methods=['POST'])
def diet():
    age = int(request.form['age'])
    disease = request.form['disease'].lower()
    
    if 'diabetes' in disease:
        diet = "Low-carb diet with oats, vegetables, and sugar-free fruits like berries."
    elif 'thyroid' in disease:
        diet = "Include iodine-rich food like eggs, dairy, and avoid gluten."
    else:
        if age < 30:
            diet = "Balanced diet with fruits, green veggies, dal, and water."
        else:
            diet = "Eat high-fiber foods, avoid sugar, and walk 30 min/day."

    return render_template('tools.html', user=session['user'], diet=diet)

from datetime import datetime, timedelta

@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session:
        return redirect(url_for('login'))

    last_period_str = request.form['last_period']
    try:
        last_period_date = datetime.strptime(last_period_str, "%Y-%m-%d")
        next_period = last_period_date + timedelta(days=28)
        next_date_str = next_period.strftime("%d-%B-%Y")

        return render_template('tools.html', user=session['user'], next_period=next_date_str)
    except:
        return render_template('tools.html', user=session['user'], next_period="Invalid Date")
    
    gyne_list = {
    "Kolkata": [
        {"name": "Dr. Rina Das", "address": "Salt Lake", "phone": "9876543210"},
        {"name": "Dr. Neha Roy", "address": "New Town", "phone": "9832012345"}
    ],
    "Delhi": [
        {"name": "Dr. Shweta Mehra", "address": "Lajpat Nagar", "phone": "9870012345"}
    ]
}

@app.route('/gyne')
def gyne():
    user_city = session.get('city', 'Kolkata')  # Default is Kolkata
    doctors = gyne.get(user_city, [])
    return render_template('gyne.html', doctors=doctors)

@app.route('/signin', methods=['POST'])
def signin():
    name = request.form['name']
    city = request.form['city']
    lang = request.form['language']

    session['user'] = name
    session['city'] = city
    session['lang'] = lang

    return redirect('/tools')  # or wherever you want to go next


@app.route('/set_language/<lang>')
def set_language(lang):
    session['lang'] = lang
    return redirect('/')




@app.route('/thankyou')
def thankyou():
    session.pop('user', None)
    return render_template('thankyou.html')



if __name__ == '__main__':
    app.run(debug=True)
