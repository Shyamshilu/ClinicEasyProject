from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Doctor,Review
from appointments.models import Appointment


from django.db.models import Q, Avg
from .models import Doctor

def doctor_list(request):
    query = request.GET.get('q')
    specialization = request.GET.get('specialization')
    department = request.GET.get('department')
    location = request.GET.get('location')

    doctors = Doctor.objects.all()

    # Filters
    if query:
        doctors = doctors.filter(Q(name__icontains=query) | Q(specialization__icontains=query))

    if specialization:
        doctors = doctors.filter(specialization__icontains=specialization)

    if department:
        doctors = doctors.filter(department__icontains=department)

    if location:
        doctors = doctors.filter(location__icontains=location)

    # ⭐ Add rating data
    doctors = doctors.annotate(
        avg_rating=Avg('reviews__rating')
    )

    return render(request, 'doctors.html', {'doctors': doctors})
@login_required
def doctor_dashboard(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return redirect('login')

    if request.method == "POST":
        appointment_id = request.POST.get("appointment_id")
        action = request.POST.get("action")

        appointment = get_object_or_404(
            Appointment,
            id=appointment_id,
            doctor=doctor
        )

        if action == "approve":
            appointment.status = "Approved"
        elif action == "reject":
            appointment.status = "Rejected"

        appointment.save()
        return redirect('doctor_dashboard')

    appointments = Appointment.objects.filter(
        doctor=doctor
    ).order_by('-appointment')

    context = {
        'doctor': doctor,
        'appointments': appointments
    }

    return render(request, 'doctor_dashboard.html', context)

from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from .models import Doctor, Review

def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    reviews = doctor.reviews.all()

    # ⭐ Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    total_reviews = reviews.count()

    if request.method == "POST":
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if request.user.is_authenticated:
            if not Review.objects.filter(doctor=doctor, user=request.user).exists():
                Review.objects.create(
                    doctor=doctor,
                    user=request.user,
                    rating=rating,
                    comment=comment
                )

        return redirect('doctor_detail', doctor_id=doctor.id)

    context = {
        'doctor': doctor,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'total_reviews': total_reviews
    }

    return render(request, 'doctor_detail.html', context)




from django.http import HttpResponse
from django.contrib.auth.models import User
from doctors.models import Doctor

def add_all_doctors(request):
    data = [
        ("drarjun@gmail.com", "Dr. Arjun Sharma", "Cardiology", "Cardiologist", 18, "Experienced cardiologist specializing in heart health.", "Rajkot", "doctors/staff-11.webp"),
        ("drajay@gmail.com", "Dr. Ajay Mehta", "Neurology", "Neurologist", 14, "Expert in neurological disorders.", "Rajkot", "doctors/staff-7.webp"),
        ("dranjali@gmail.com", "Dr. Anjali Verma", "Orthopedics", "Orthopedic Surgeon", 16, "Specialist in joint replacement and trauma.", "Rajkot", "doctors/anjali.webp"),
        ("drneha@gmail.com", "Dr. Neha Kapoor", "Pediatrics", "Pediatrician", 12, "Dedicated to child healthcare.", "Ahmedabad", "doctors/staff-3.webp"),
        ("drrohit@gmail.com", "Dr. Rohit Malhotra", "Dermatology", "Dermatologist", 15, "Expert in skin care and treatments.", "Rajkot", "doctors/rohit.webp"),
        ("drkavita@gmail.com", "Dr. Kavita Nair", "Oncology", "Oncologist", 12, "Specialist in cancer care.", "Ahmedabad", "doctors/staff-14.webp"),
        ("drkaran@gmail.com", "Dr. Karan Singh", "Emergency", "Emergency Medicine", 13, "Expert in trauma care.", "Ahmedabad", "doctors/staff-5.webp"),
        ("drshivam@gmail.com", "Dr. Shivam Iyer", "Radiology", "Radiologist", 9, "Specialist in medical imaging.", "Rajkot", "doctors/staff-1.webp"),
        ("drrahul@gmail.com", "Dr. Rahul Patel", "Cardiology", "Cardiologist", 20, "Heart specialist with advanced treatment experience.", "Ahmedabad", "doctors/Rahul.jfif"),
        ("drpooja@gmail.com", "Dr. Pooja Joshi", "Pediatrics", "Pediatrician", 10, "Focused on child healthcare and growth.", "Ahmedabad", "doctors/Pooja.jpg"),
        ("drvishal@gmail.com", "Dr. Vishal Trivedi", "Orthopedics", "Orthopedic Surgeon", 17, "Expert in bone and joint surgeries.", "Rajkot", "doctors/Vishal.jfif"),
        ("drmanish@gmail.com", "Dr. Manish Bhatt", "Oncology", "Oncologist", 13, "Cancer specialist with modern treatments.", "Rajkot", "doctors/Manish.jfif"),
        ("drsneha@gmail.com", "Dr. Sneha Pandya", "Radiology", "Radiologist", 8, "Expert in MRI and CT scan diagnosis.", "Ahmedabad", "doctors/Sneha.jfif"),
        ("drnikhil@gmail.com", "Dr. Nikhil Vyas", "Emergency", "Emergency Medicine", 12, "Handles trauma and emergency cases.", "Rajkot", "doctors/Nikhil.jpg"),
        ("drankit@gmail.com", "Dr. Ankit Dave", "Cardiology", "Cardiologist", 15, "Experienced in heart surgeries.", "Ahmedabad", "doctors/Ankit.jfif"),
        ("drkrunal@gmail.com", "Dr. Krunal Patel", "Dermatology", "Dermatologist", 7, "Skin specialist with modern techniques.", "Rajkot", "doctors/Krunal.jfif"),
    ]

    added = 0

    for email, name, dept, spec, exp, desc, loc, img in data:
        if not User.objects.filter(username=email).exists():
            user = User.objects.create_user(username=email, password="doctor123")

            Doctor.objects.create(
                user=user,
                name=name,
                department=dept,
                specialization=spec,
                experience=exp,
                description=desc,
                location=loc,
                image=img
            )
            added += 1

    return HttpResponse(f"✅ {added} doctors added successfully")