import logging
import json

from flask import render_template,request
from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.validators import Required

from . import app, estimator, target_names


logger = logging.getLogger('app')

# DiseaseChoices = [('1', 'Weight Loss Programs'),(1,'High Blood Pressure & High Cholesterol'),(1,'Low Back Pain'),(1,'Diabetes'),
# (1,'Pregnancy'),(1,'Asthma'),(1,'Heart Disease'),(1,'Depression'),(1,'Pain Management')]

# CSRchoices = [('1','73% AV Level Silver Plan'),(1,'87% AV Level Silver Plan'),(1,'94% AV Level Silver Plan'),(1,'Limited Cost Sharing Plan Variation'),(1,'Standard Bronze Off Exchange Plan'),(1,'Standard Bronze On Exchange Plan'),
# (1,'Standard Gold Off Exchange Plan'),(1,'Standard Gold On Exchange Plan'),(1,'Standard Platinum Off Exchange Plan'),(1,'Standard Silver Off Exchange Plan'),(1,'Standard Silver On Exchange Plan'),(1,'Zero Cost Sharing Plan Variation'),(1,'Standard Platinum  On Exchange Plan')]

# PlanTypeChoices = [('1','EPO'),(1,'HMO'),(1,'POS'),(1,'PPO'),]

class PredictForm(FlaskForm):
    """Fields for Predict"""
    First_Tier_Utilization = fields.DecimalField('First Tier Utilization', places=2, default = 0, validators=[Required()])
    Weight_Loss_Programs = fields.SelectField('Weight Loss Programs', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    Heart_Disease = fields.SelectField('Heart Disease', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    Pain_Management = fields.SelectField('Pain Management', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    Depression = fields.SelectField('Depression', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    High_BP_Chol = fields.SelectField('High Blood Pressure & High Cholesterol', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    Low_Back_Pain = fields.SelectField('Low Back Pain', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    Diabetes = fields.SelectField('Diabetes', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    Pregnancy = fields.SelectField('Pregnancy', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    Asthma = fields.SelectField('Asthma', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    HSAEliNo = fields.SelectField('No', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    HSAEliYes = fields.SelectField('Yes', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    ExistingPlan = fields.SelectField('Existing', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    NewPlan = fields.SelectField('New', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    PregNo = fields.SelectField('No', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    PregYes = fields.SelectField('Yes', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    SpecNo = fields.SelectField('No', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    SpecYes = fields.SelectField('Yes', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    MCInd = fields.SelectField('Individual', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    MCShop = fields.SelectField('SHOP', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    DDIntNo = fields.SelectField('No', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    DDIntYes = fields.SelectField('Yes', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    MOOPIntNo = fields.SelectField('No', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    MOOPIntYes = fields.SelectField('Yes', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    EPO = fields.SelectField('EPO', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    HMO = fields.SelectField('HMO', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    POS = fields.SelectField('POS', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    PPO = fields.SelectField('PPO', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    

    submit = fields.SubmitField('Submit')

    # DiseasesCovered = SelectMultipleField("Conditions Covered:", choices=DiseaseChoices)
    # CSRtypes = fields.SelectField('CSR Plans:', choices=CSRchoices)
    # IsHSAEligible = fields.SelectField('HSA Eligible?', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    # IsNewPlan = fields.SelectField('New Plan?', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    # IsPreg = fields.SelectField('Is Notice Required for Pregnancy?', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    # IsSpecialist = fields.SelectField('Is Referral Required For Specialist?', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    
    # MrktCvrg = fields.SelectMuField('Market Coverage', choices=[('1','Individual'),(1,'SHOP')], default = '0', validators=[Required()])
    # DeductiblesIntegrated = fields.SelectField('Medical Drug Deductibles Integrated?', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    # MOOPIntegrated = fields.SelectField('MOOP Integrated?', choices=[('1','Yes'),('0','No')], default = '0', validators=[Required()])
    # PlanType = fields.SelectField('Plan Type', choices=PlanTypeChoices, default = '0', validators=[Required()])

    


@app.route('/', methods=('GET', 'POST'))
def index():
    """Index page"""
    form = PredictForm()
    predicted_metallevel = None

    if form.validate_on_submit():

        # store the submitted values
        submitted_data = form.data

        # Retrieve values from form
        First_Tier_Utilization = float(submitted_data['First_Tier_Utilization'])
        Weight_Loss_Programs = float(submitted_data['Weight_Loss_Programs'])
        High_BP_Chol = float(submitted_data['High_BP_Chol'])
        Low_Back_Pain = float(submitted_data['Low_Back_Pain'])
        Diabetes = float(submitted_data['Diabetes'])
        Pregnancy = float(submitted_data['Pregnancy'])
        Asthma = float(submitted_data['Asthma'])
        HSAEliNo = float(submitted_data['HSAEliNo'])
        HSAEliYes = float(submitted_data['HSAEliYes'])
        ExistingPlan = float(submitted_data['ExistingPlan'])
        NewPlan = float(submitted_data['NewPlan'])
        PregNo = float(submitted_data['PregNo'])
        PregYes = float(submitted_data['PregYes'])
        SpecNo = float(submitted_data['SpecNo'])
        SpecYes = float(submitted_data['SpecYes'])
        MCInd = float(submitted_data['MCInd'])
        MCShop = float(submitted_data['MCShop'])
        DDIntNo = float(submitted_data['DDIntNo'])
        DDIntYes = float(submitted_data['DDIntYes'])
        MOOPIntNo = float(submitted_data['MOOPIntNo'])
        MOOPIntYes = float(submitted_data['MOOPIntYes'])
        EPO = float(submitted_data['EPO'])
        HMO = float(submitted_data['HMO'])
        POS = float(submitted_data['POS'])
        PPO = float(submitted_data['PPO'])
        Heart_Disease = float(submitted_data['Heart_Disease'])
        Depression = float(submitted_data['Depression'])
        Pain_Management = float(submitted_data['Pain_Management'])


        # Create array from values
        test_array = [First_Tier_Utilization, Weight_Loss_Programs, High_BP_Chol, Low_Back_Pain,
        Diabetes,Pregnancy,Asthma,HSAEliNo,HSAEliYes,ExistingPlan,
        NewPlan,PregNo,PregYes,SpecNo,SpecYes,MCInd,MCShop,DDIntNo,DDIntYes,MOOPIntNo,MOOPIntYes,EPO,HMO,
        POS,PPO,Heart_Disease,Depression,Pain_Management]
        
        my_prediction = estimator.predict(test_array)
        # Return only the Predicted iris species
        # print(target_names[my_prediction[0]])
        predicted_metallevel = target_names[my_prediction[0]]

    return render_template('index.html',
        form=form,
        prediction=predicted_metallevel)