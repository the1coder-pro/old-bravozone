from django.shortcuts import render, redirect

from evaluation.models import Task
from .forms import SignUpEmployeeForm, SignUpForm, EducationalQualificationForm
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .models import User, EducationalQualification
from django.contrib.auth import logout

from evaluation.models import Task


def home(request):
    # users = User.objects.all()
    users = User.objects.filter(is_superuser=False, is_staff=False)
    return render(request, "accounts/admin_view.html", {"users": users})


def signup(request):
    if request.method == "POST":
        user_form = SignUpForm(request.POST, request.FILES)
        print(user_form)
        if user_form.is_valid():
            user = user_form.save()

            role = user_form.cleaned_data["role"]
            if role == "admin":
                user.is_staff = True
            elif role == "superadmin":
                user.is_staff = True
                user.is_superuser = True
            user.save()
            return redirect("account:login")
    else:
        user_form = SignUpForm()
    return render(
        request,
        "accounts/signup.html",
        {"user_form": user_form},
    )


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    if user.is_superuser:
                        return redirect("account:home")
                    else:
                        return redirect('main:home_view')
                else:
                    form.add_error(None, "Invalid username or password.")
        else:
            form = LoginForm()
        return render(request, "accounts/login.html", {"form": form})
    return redirect("account:profile")


def logout_view(request):
    logout(request)
    return redirect("account:login")


def profile(request, user_id=None):
    if user_id != None:
        profile_user = User.objects.get(pk=user_id)
        print(profile_user)
    else:
        profile_user = User.objects.get(pk=request.user.id)
      
        print(profile_user)

    task_list = Task.objects.filter(assigned_to=profile_user, status='completed')
    print(task_list)
    return render(request, "accounts/profile.html", {"profile_user": profile_user, 'task_list': task_list})


def all_emploee(request):
    employees = User.objects.filter(is_superuser=False, is_staff=False)
    
    leaderboard_list = []
    for employee in employees:
        employee_tasks = Task.objects.filter(assigned_to=employee)
        print(employee_tasks)
        completed_tasks_points = []
        for task in employee_tasks:
            if task.status == 'completed':
                completed_tasks_points.append(int(task.points))
            
        print(completed_tasks_points)

        leaderboard_list.append({'employee': employee, 'number_of_tasks': len(employee_tasks),'total_points':sum(completed_tasks_points)})
        print(leaderboard_list)


    return render(request, "accounts/all_employee.html", {"users": leaderboard_list})


def register_employee(request):
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            if request.method == "POST":
                employee_form = SignUpEmployeeForm(request.POST, request.FILES)
                print(employee_form)
                if employee_form.is_valid():
                    employee = employee_form.save()


                    employee.save()
                    return redirect(f"/account/profile/{employee.id}")
            else:
                employee_form = SignUpEmployeeForm(request.POST, request.FILES)
            return render(
                request,
                "accounts/register_employee.html",
                {"employee_form": employee_form},
            )
        else:
            return render(request, "<h1>You are not Allowed.</h1>")
    else:
        return render(request, "account:login")

    
    # return render(request, "accounts/regester.html", {"users": user})        


def edit_profile(request, user_id):
    if request.user.is_authenticated:
        
        user = User.objects.get(pk=user_id)
        if request.user.is_superuser or request.user == user:
            education_user = EducationalQualification.objects.get_or_create(user=user)
            education_form = EducationalQualificationForm(request.POST)
            print(education_user[0].skills)
            if request.method == "POST":
                # if education_form.is_valid():
                user.first_name = request.POST.get("first_name")
                user.last_name = request.POST.get("last_name")
                user.bio = request.POST.get("bio")
                user.email = request.POST.get("email")

                skills = request.POST.getlist("skills")
                print(skills)

                education_user[0].skills.set(skills)
                education_user[0].major = request.POST.get("major")
                education_user[0].degree = request.POST.get("degree")

                education_user[0].university_name = request.POST.get("university_name")
                education_user[0].save()
                print(education_user)
                user.save()
                # education = education_form.save(commit=False)
                # education.user = user

                # education.save()

                return redirect(f"/account/profile/{user.id}")
            return render(
                request,
                "accounts/edit_profile.html",
                {
                    "profile_id": user_id,
                    "profile_user": user,
                    "education_form": education_form,
                },
            )
        else:
            return render(request, '<h3>your are not allowed</h3>')
    else:
        return render("account:login")
