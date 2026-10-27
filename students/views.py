from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Student


def student_list(request):
    students = Student.objects.all().order_by("-created_at")

    return render(
        request,
        "students/student_list.html",
        {"students": students},
    )


def add_student(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        course = request.POST.get("course", "").strip()

        if not name or not email or not course:
            messages.error(request, "All fields are required.")
            return redirect("add_student")

        if Student.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            return redirect("add_student")

        Student.objects.create(
            name=name,
            email=email,
            course=course,
        )

        messages.success(request, "Student registered successfully!")
        return redirect("student_list")

    return render(request, "students/add_student.html")


def delete_student(request, student_id):
    if request.method == "POST":
        student = get_object_or_404(Student, id=student_id)
        student.delete()
        messages.success(request, "Student deleted successfully.")

    return redirect("student_list")