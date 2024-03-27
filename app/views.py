from django.contrib import messages
from django.shortcuts import render
from .forms import StressLevelForm
import joblib
import pandas as pd
from .models import StressLevelRecord

# Load the model (consider loading this only once, e.g., at app startup)
model = joblib.load('static/model/random_forest_model.joblib')


def home(request):
    mild_reco = [
        'Practice deep breathing exercises',
        'Take short breaks to stretch and move around',
        'Engage in a hobby or activity you enjoy such as reading, listening to music',
        'Maintain a regular sleep schedule',
        'Connect with friends or loved ones for support',
        'Prioritize tasks and break them into smaller steps',
        'Practice mindfulness or meditation',
        'Limit exposure to stressors when possible',
        'Establish a daily routine for stability',
        'Focus on positive affirmations and gratitude'
    ]
    minimal_reco = [
        'Identify and acknowledge sources of stress',
        "Seek social support from friends or family about how you're feeling",
        'Use time management techniques to organize tasks',
        'Incorporate regular physical activity into your routine',
        'Delegate responsibilities to lighten the load',
        'Set realistic goals and expectations',
        'Practice relaxation techniques, such as deep breathing',
        'Consider journaling to express thoughts and feelings',
        'Take breaks for self-care and relaxation',
        'Explore new coping strategies or hobbies'
    ]
    moderate_reco = [
        'Consider professional counseling or therapy',
        'Develop a structured daily schedule',
        'Evaluate and adjust priorities and commitments',
        'Engage in regular exercise for stress relief',
        'Utilize problem-solving techniques for challenges',
        'Practice assertiveness in communicating needs',
        'Connect with a support group or community',
        'Explore mindfulness practices for stress reduction',
        'Take short breaks for relaxation during the day',
        'Ensure a healthy work-life balance'
    ]
    moderately_severe_reco = [
        'Prioritize self-care',
        'Practice mindfulness',
        'Set realistic goals',
        'Establish boundaries',
        'Seek social support',
        'Manage time effectively',
        'Engage in relaxation activities',
        'Limit exposure to stressful triggers',
        'Practice gratitude',
        'Seek professional help when needed'
    ]
    severe_reco = [
        'Reach out to a mental health professional for help',
        'Consider medication options if recommended by a professional',
        'Develop a comprehensive stress management plan',
        'Communicate with employers or academic institutions about the situation',
        'Build a strong support network of friends and family',
        'Implement stress-reduction techniques consistently',
        'Practice self-compassion and avoid self-blame',
        'Consider taking a temporary break from major stressors',
        'Attend support groups or therapy sessions',
        'Focus on self-care, including proper nutrition and sleep'
    ]

    if request.method == 'POST':
        form = StressLevelForm(request.POST)
        if form.is_valid():
            # Extract data from form
            input_data = form.cleaned_data

            # Convert PHQ scores to integers and sum them
            phq_scores_sum = sum(int(input_data['phq{}'.format(i)]) for i in range(1, 10))

            # Construct a DataFrame with the same structure as the training data
            model_input = pd.DataFrame([[
                int(input_data['age']),
                int(input_data['gender']),
                int(input_data['bmi_category']),
                int(input_data['phq1']),
                int(input_data['phq2']),
                int(input_data['phq3']),
                int(input_data['phq4']),
                int(input_data['phq5']),
                int(input_data['phq6']),
                int(input_data['phq7']),
                int(input_data['phq8']),
                int(input_data['phq9']),
                phq_scores_sum,
            ]], columns=[
                'Age', 'Gender', 'BMI Category', 'phq1', 'phq2', 'phq3',
                'phq4', 'phq5', 'phq6', 'phq7', 'phq8', 'phq9', 'phq_scores'
            ])

            # Make prediction
            stress_level_encoded = model.predict(model_input)[0]

            # Mapping of numeric stress level to readable category
            stress_level_mapping = {0: 'Mild', 1: 'Minimal', 2: 'Moderate', 3: 'Moderately Severe', 4: 'Severe'}

            # Convert numeric stress level to readable category
            stress_level = stress_level_mapping.get(stress_level_encoded, "Unknown")

            # Check the predicted stress level and select appropriate recommendations
            recommendations = {
                'Mild': mild_reco,
                'Minimal': minimal_reco,
                'Moderate': moderate_reco,
                'Moderately Severe': moderately_severe_reco,
                'Severe': severe_reco
            }.get(stress_level, [])

            # Convert numerical values to text for gender and BMI Category
            gender_text = dict(StressLevelForm.GENDER_CHOICES).get(int(input_data['gender']), 'Unknown')
            bmi_category_text = dict(StressLevelForm.BMI_CATEGORY_CHOICES).get(int(input_data['bmi_category']),
                                                                               'Unknown')

            # Save to database
            stress_level_record = StressLevelRecord(
                name=input_data['name'],
                age=input_data['age'],
                gender=gender_text,
                bmi_category=bmi_category_text,
                phq1=input_data['phq1'],
                phq2=input_data['phq2'],
                phq3=input_data['phq3'],
                phq4=input_data['phq4'],
                phq5=input_data['phq5'],
                phq6=input_data['phq6'],
                phq7=input_data['phq7'],
                phq8=input_data['phq8'],
                phq9=input_data['phq9'],
                phq_score_total=phq_scores_sum,
                # is_suicide='Yes' if int(input_data['phq9']) != 0 else 'No',
                stress_level=stress_level,
                recommendations=', '.join(recommendations)  # Convert list to string
            )
            stress_level_record.save()

            # Add a message with the stress level and redirect or render the template with recommendations
            messages.success(request, stress_level)
            # Instead of redirecting, render the same page with recommendations
            context = {
                'form': form,
                'recommendations': recommendations
            }

            # Add isSuicide to context only if it's not 0
            if int(input_data['phq9']) != 0:
                context['isSuicide'] = int(input_data['phq9'])

            return render(request, 'home.html', context)
        else:
            # Form is not valid, re-render the page with the form
            return render(request, 'home.html', {'form': form})
    else:
        form = StressLevelForm()
        return render(request, 'home.html', {'form': form})


def show_record(request):
    stress_level_record = StressLevelRecord.objects.all()

    return render(request, 'show_record.html', {'stress_level_record': stress_level_record})
