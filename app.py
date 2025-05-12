from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
from wtforms import IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, NumberRange
import joblib
import numpy as np
from forms import HeartDiseaseForm
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
CORS(app)

# Load the trained model
model = joblib.load('model/model.pkl')

# Define lifestyle recommendations
LIFESTYLE_RECOMMENDATIONS = {
    'exercise': {
        'low': "Increase physical activity to at least 30 minutes per day, 5 days a week.",
        'moderate': "Maintain your current exercise routine, consider adding variety.",
        'high': "Excellent! Keep up your active lifestyle."
    },
    'diet': {
        'unhealthy': "Focus on a balanced diet with more fruits, vegetables, and whole grains.",
        'average': "Your diet is decent but could use more variety and nutrients.",
        'healthy': "Great job maintaining a healthy diet!"
    },
    'stress': {
        'high': "Practice stress-reduction techniques like meditation or yoga.",
        'moderate': "Try to identify and reduce key stressors in your life.",
        'low': "You're managing stress well. Keep it up!"
    }
}

class HeartDiseaseForm(FlaskForm):
    # Basic health metrics
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=1, max=120)])
    sex = SelectField('Sex', choices=[(0, 'Female'), (1, 'Male')], validators=[DataRequired()])
    cp = SelectField('Chest Pain Type', choices=[
        (0, 'Typical angina'),
        (1, 'Atypical angina'),
        (2, 'Non-anginal pain'),
        (3, 'Asymptomatic')
    ], validators=[DataRequired()])
    trestbps = IntegerField('Resting Blood Pressure (mm Hg)', validators=[DataRequired(), NumberRange(min=50, max=250)])
    chol = IntegerField('Serum Cholesterol (mg/dl)', validators=[DataRequired(), NumberRange(min=100, max=600)])
    fbs = SelectField('Fasting Blood Sugar > 120 mg/dl', choices=[(0, 'No'), (1, 'Yes')], validators=[DataRequired()])
    
    # Lifestyle factors
    exercise = SelectField('Exercise Frequency', choices=[
        ('low', 'Less than 1 hour/week'),
        ('moderate', '1-3 hours/week'),
        ('high', 'More than 3 hours/week')
    ], validators=[DataRequired()])
    diet = SelectField('Diet Quality', choices=[
        ('unhealthy', 'Mostly processed foods'),
        ('average', 'Mix of healthy and unhealthy'),
        ('healthy', 'Mostly whole, unprocessed foods')
    ], validators=[DataRequired()])
    stress = SelectField('Stress Level', choices=[
        ('high', 'Frequent stress'),
        ('moderate', 'Occasional stress'),
        ('low', 'Rarely stressed')
    ], validators=[DataRequired()])
    family_history = SelectField('Family History of Heart Disease', choices=[(0, 'No'), (1, 'Yes')], validators=[DataRequired()])
    smoking = SelectField('Smoking Status', choices=[(0, 'Non-smoker'), (1, 'Smoker')], validators=[DataRequired()])
    
    # Doctor communication
    share_with_doctor = BooleanField('Share results with my doctor')
    share_with_family = BooleanField('Share results with family members')

@app.route('/predict', methods=['POST'])
def predict():
    form = HeartDiseaseForm()
    
    if form.validate_on_submit():
        # Prepare features for prediction
        features = [
            form.age.data,
            form.sex.data,
            form.cp.data,
            form.trestbps.data,
            form.chol.data,
            form.fbs.data,
            0,  # restecg - placeholder
            0,  # thalach - placeholder
            0,  # exang - placeholder
            0,  # oldpeak - placeholder
            0,  # slope - placeholder
            0,  # ca - placeholder
            0   # thal - placeholder
        ]
        
        # Make prediction
        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0][1]
        
        # Generate lifestyle recommendations
        recommendations = {
            'exercise': LIFESTYLE_RECOMMENDATIONS['exercise'][form.exercise.data],
            'diet': LIFESTYLE_RECOMMENDATIONS['diet'][form.diet.data],
            'stress': LIFESTYLE_RECOMMENDATIONS['stress'][form.stress.data]
        }
        
        # Additional suggestions based on risk level
        if probability > 0.7:
            recommendations['general'] = "Your risk is high. Consider consulting a cardiologist for a comprehensive evaluation."
        elif probability > 0.4:
            recommendations['general'] = "Moderate risk detected. Lifestyle changes can significantly reduce your risk."
        else:
            recommendations['general'] = "Low risk detected. Maintain your healthy habits!"
        
        # Process sharing options
        share_options = {
            'doctor': form.share_with_doctor.data,
            'family': form.share_with_family.data
        }
        
        return render_template('results.html', 
                            prediction=prediction, 
                            probability=round(probability*100, 2),
                            recommendations=recommendations,
                            share_options=share_options)
    
    return render_template('index.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)