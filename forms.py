from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, NumberRange

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
