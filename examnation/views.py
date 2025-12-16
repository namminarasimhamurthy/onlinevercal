from django.shortcuts import render, redirect
from django.contrib import messages
from .models import RegisterUser, Question
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User


def index(request):
    return render(request, 'index.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_superuser = False
        user.is_staff = False
        user.save()

        RegisterUser.objects.create(
            username=username,
            email=email,
            password=password,
            confirm_password=confirm_password
        )

        messages.success(request, "Registration successful!")
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    return redirect("admin_add_question")
                else:
                    return redirect("dashboard")
            else:
                messages.error(request, "Your account is inactive.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

@user_passes_test(lambda u: u.is_superuser)
def add_question_view(request):
    if request.method == 'POST':
        course = request.POST['course']
        question_text = request.POST['question']
        option1 = request.POST['option1']
        option2 = request.POST['option2']
        option3 = request.POST['option3']
        option4 = request.POST['option4']
        answer = request.POST['answer']

        Question.objects.create(
            course=course,
            question_text=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_answer=answer
        )

        messages.success(request, "Question added successfully!")
        return redirect('admin_add_question')

    return render(request, "admin_add_question.html")

def dashboard_view(request):
    courses = [
        {
            "name": "python",
            "title": "Python Programming",
            "description": "Learn the basics of Python.",
            "image_url": "/static/pythonimg.png"
        },
        {
            "name": "webdev",
            "title": "Web Development",
            "description": "Build websites with HTML, CSS, and JS.",
            "image_url": "/static/webdevimg.png"
        },
        {
            "name": "datasci",
            "title": "Data Science",
            "description": "Analyze data using Python and tools.",
            "image_url": "/static/datascience.png"
        }
    ]
    return render(request, "dashboard.html", {"courses": courses})

def test_view(request, course_name):
    questions = list(Question.objects.filter(course=course_name))

    if not questions:
        return render(request, "404.html", {"message": "No questions available for this course."})

    session_key_index = f"{course_name}_index"
    session_key_score = f"{course_name}_score"

    if session_key_index not in request.session:
        request.session[session_key_index] = 0
        request.session[session_key_score] = 0

    index = request.session[session_key_index]

    if index >= len(questions):
        score = request.session[session_key_score]
        del request.session[session_key_index]
        del request.session[session_key_score]
        return render(request, "result.html", {
            'score': score,
            'total': len(questions) * 2,
            'course_name': course_name.capitalize()
        })

    question = questions[index]

    if request.method == 'POST':
        selected = request.POST.get('option')
        if selected == question.correct_answer:
            request.session[session_key_score] += 2
        else:
            request.session[session_key_score] -= 1

        request.session[session_key_index] += 1
        return redirect('take_test', course_name=course_name)

    return render(request, "test.html", {
        'course_name': course_name.capitalize(),
        'question': question,
        'options': [question.option1, question.option2, question.option3, question.option4],
        'index': index + 1,
        'total': len(questions)
    })

def result_view(request):
    return render(request, 'result.html')
