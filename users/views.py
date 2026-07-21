# Create your views here.
from datetime import datetime
from datetime import timedelta
from django.conf import settings
import pandas as pd
from django.contrib import messages
from django.shortcuts import render, HttpResponse
from jose import JWTError, jwt

from .forms import UserRegistrationForm
from .models import UserRegistrationModel, TokenCountModel

SECRET_KEY = "ce9941882f6e044f9809bcee90a2992b4d9d9c21235ab7c537ad56517050f26b"
ALGORITHM = "HS256"


def create_access_token(data: dict):
    to_encode = data.copy()
    # expire time of the token
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # return the generated token
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HttpResponse(
            status_code=HttpResponse(status=204),
            detail="Could not validate credentials",
        )


# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            loginId = form.cleaned_data['loginid']
            TokenCountModel.objects.create(loginid=loginId, count=0)
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                data = {'loginid': loginid}
                token_jwt = create_access_token(data)
                request.session['token'] = token_jwt
                print("User id At", check.id, status)
                return render(request, 'users/UserHomePage.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})


def UserHome(request):
    return render(request, 'users/UserHomePage.html', {})


def ViewDataset(request):
    path = settings.MEDIA_ROOT + "\\" + "SocialServiceData.csv"
    df = pd.read_csv(path)
    df = df.to_html(index=False)
    return render(request, 'users/UserViewDataset.html', {'data': df})


def RegressionAnalysis(request):
    from .utility.anovamodel import start_proccess
    summary, result = start_proccess()
    return render(request, 'users/analysis.html',
                  {'summary': summary, 'data': '', 'result': result})


def TestStatisticsAnalysis(request):
    from .utility.chi_square_test import start_chi
    data = start_chi()
    return render(request, "users/chi_test_result.html", {'data': data})


questions = [
    {
        'question': "What is the most common type of phishing attack?",
        'options': ['Spear phishing', 'Whaling', 'Vishing', 'Smishing'],
        'answer': 'Spear phishing'
    },
    {
        'question': "Which protocol is used for secure web browsing?",
        'options': ['HTTP', 'HTTPS', 'FTP', 'SMTP'],
        'answer': 'HTTPS'
    },
    {
        'question': "What is a firewall used for?",
        'options': ['Encrypting data', 'Filtering network traffic', 'Accessing websites', 'Scanning for malware'],
        'answer': 'Filtering network traffic'
    },
    {
        'question': "Which one is a strong password?",
        'options': ['password123', 'admin2020', 'Qw!7$pLk@9$', '123456'],
        'answer': 'Qw!7$pLk@9$'
    }
]


def SampleTest(request):
    if request.method=='POST':
        # Collect demographic information and exam answers
        gender = request.POST.get('gender')
        age_group = request.POST.get('age_group')
        occupation = request.POST.get('occupation')
        region = request.POST.get('region')
        answers = [request.POST.get(f'answer{i}') for i in range(len(questions))]

        # Calculate the score based on correct answers
        score = sum(1 for i, question in enumerate(questions) if answers[i] == question['answer'])

        # Determine cybersecurity level based on the score
        if score == len(questions):
            level = "Advanced"
        elif score >= len(questions) // 2:
            level = "Intermediate"
        else:
            level = "Beginner"

        # Render the result template
        return render(request, 'users/result.html', {
            'score': score,
            'level': level,
            'gender': gender,
            'age_group': age_group,
            'occupation': occupation,
            'region': region,
            'total_questions': len(questions)
        })

    else:
        return render(request, 'users/exam.html', {'questions': questions})
