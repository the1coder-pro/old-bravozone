from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse


import sys

sys.path.append(".")
from evaluation.models import Task
from account.models import User


def home_view(request: HttpRequest):
    return render(request, "main/home_view.html")


def leader_bord(request):
    employees = User.objects.filter(is_superuser=False, is_staff=False)

    leaderboard_list = []
    for employee in employees:
        employee_tasks = Task.objects.filter(assigned_to=employee)
        print(employee_tasks)
        completed_tasks_points = []
        for task in employee_tasks:
            if task.status == "completed":
                completed_tasks_points.append(int(task.points))

        print(completed_tasks_points)

        leaderboard_list.append(
            {
                "employee": employee,
                "number_of_tasks": len(employee_tasks),
                "total_points": sum(completed_tasks_points),
            }
        )
        print(leaderboard_list)

    ordered_list = sorted(
        leaderboard_list, key=lambda x: x["total_points"], reverse=True
    )

    

    return render(
        request,
        "main/leader_bord.html",
        {"first_three_employees": ordered_list[0:3], "ordered_list": ordered_list},
    )
