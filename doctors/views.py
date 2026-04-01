from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Doctor,Review
from appointments.models import Appointment
from django.db.models import Q, Avg

def doctor_list(request):
    query = request.GET.get('q')
    specialization = request.GET.get('specialization')
    department = request.GET.get('department')
    location = request.GET.get('location')

    doctors = Doctor.objects.all()

    if query:
        doctors = doctors.filter(Q(name__icontains=query) | Q(specialization__icontains=query))

    if specialization:
        doctors = doctors.filter(specialization__icontains=specialization)

    if department:
        doctors = doctors.filter(department__icontains=department)

    if location:
        doctors = doctors.filter(location__icontains=location)

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


def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    reviews = doctor.reviews.all()

    #  Calculate average rating
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