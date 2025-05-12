
import numpy as np
import joblib
import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm, PredictionForm, ProfileUpdateForm, ContactForm
from django.contrib.auth import logout
from .forms import UserRegisterForm, PredictionForm, ProfileUpdateForm
from .models import Prediction, Profile
from mediapp.ml_models.predict import predict


def home(request):
    """View for home page"""
    return render(request, 'mediapp/home.html')

def about(request):
    """View for about page"""
    return render(request, 'mediapp/about.html')

def contact(request):
    return render(request, 'mediapp/contact.html')
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Format email message
            email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            
            # Send email to admin
            admin_email = settings.ADMIN_EMAIL if hasattr(settings, 'ADMIN_EMAIL') else 'admin@medicost.com'
            
            try:
                send_mail(
                    message=email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@medicost.com',
                    recipient_list=[admin_email],
                    fail_silently=False,
                )
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('contact')
            except Exception as e:
                messages.error(request, f'Failed to send message: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = ContactForm()
    
    return render(request, 'mediapp/contact.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'mediapp/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return render(request, 'mediapp/logout.html')

@login_required
def dashboard(request):
    predictions = Prediction.objects.filter(user=request.user).order_by('-created_at')
    
    # Get data for visualizations
    prediction_data = {
        'dates': [p.created_at.strftime('%Y-%m-%d') for p in predictions],
        'costs': [p.predicted_cost for p in predictions],
    }
    
    # Get average prediction
    avg_cost = 0
    if predictions:
        avg_cost = sum(p.predicted_cost for p in predictions) / len(predictions)
    
    context = {
        'predictions': predictions,
        'prediction_data': prediction_data,
        'avg_cost': avg_cost,
    }
    return render(request, 'mediapp/dashboard.html', context)

@login_required
def profile(request):
    # Ensure profile exists
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, instance=profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'p_form': p_form,
    }
    return render(request, 'mediapp/profile.html', context)

@login_required
def prediction_new(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            prediction = form.save(commit=False)
            prediction.user = request.user
            
            try:
                # Call the predict function
                cost = predict(
                    age=prediction.age,
                    sex=prediction.gender,
                    bmi=prediction.bmi,
                    children=prediction.children,
                    smoker=prediction.smoker,
                    region=prediction.region
                )
                prediction.predicted_cost = round(cost, 2)
                prediction.save()
                messages.success(request, 'Prediction successful!')
                return redirect('prediction_result', prediction_id=prediction.id)
            except Exception as e:
                messages.error(request, f'Prediction error: {str(e)}')
    else:
        form = PredictionForm()
    return render(request, 'mediapp/prediction_form.html', {'form': form})


@login_required
def prediction_result(request, prediction_id):
    try:
        prediction = Prediction.objects.get(id=prediction_id, user=request.user)
    except Prediction.DoesNotExist:
        messages.error(request, 'Prediction not found.')
        return redirect('dashboard')
    
    # Calculate risk level
    if prediction.predicted_cost < 5000:
        risk_level = "Low"
        risk_color = "#4CAF50"  # Green
    elif prediction.predicted_cost < 15000:
        risk_level = "Medium"
        risk_color = "#FFC107"  # Amber
    else:
        risk_level = "High"
        risk_color = "#F44336"  # Red
    
    # Get average cost for comparison
    user_predictions = Prediction.objects.filter(user=request.user)
    avg_cost = sum(p.predicted_cost for p in user_predictions) / len(user_predictions) if user_predictions else 0
    
    # Prepare comparison data
    comparison = {
        'user_avg': avg_cost,
        'difference': prediction.predicted_cost - avg_cost,
        'percent_diff': ((prediction.predicted_cost - avg_cost) / avg_cost) * 100 if avg_cost > 0 else 0
    }
    
    context = {
        'prediction': prediction,
        'risk_level': risk_level,
        'risk_color': risk_color,
        'comparison': comparison
    }
    return render(request, 'mediapp/prediction_result.html', context)


model_path = os.path.join(settings.BASE_DIR, 'mediapp', 'ml_models', 'insurance_model.pkl')
model = joblib.load(model_path)

def estimate_cost(request):
    if request.method == 'POST':
        # Get form data
        input_data = [age, sex, bmi, ...]  
        prediction = predict(input_data)
        return render(request, 'result.html', {'prediction': prediction})

def predict_charge(input_data):
    # Convert input to DataFrame with matching feature names
    input_df = pd.DataFrame([input_data], 
                          columns=['age', 'sex', 'bmi', 'children', 'smoker', 'region'])
    
    prediction = model.predict(input_df)  # Now maintains feature names
    return prediction[0]