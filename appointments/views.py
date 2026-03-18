from datetime import date,datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Appointment,ContactMessage
from doctors.models import Doctor, DoctorSlot

# DOCTOR DASHBOARD
@login_required
def doctor_dashboard(request):
    try:
        doctor = request.user.doctor
    except Doctor.DoesNotExist:
        messages.error(request, "Access denied.")
        return redirect("index")

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
            appointment.save()

            send_mail(
                subject="Appointment Approved - ClinicEasy",
                message=f"""
            Dear {appointment.patient_name},

                Your appointment has been Approved by the doctor.

                Doctor: {appointment.doctor.name}
                Date: {appointment.appointment_date}
                Time: {appointment.appointment_time}
                Status: Approved

                Please arrive on time.

                Thank you,
                ClinicEasy Team
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[appointment.email],
                fail_silently=False,
            )

            messages.success(request, "Appointment approved and email sent.")

        elif action == "reject":
            appointment.status = "Rejected"
            appointment.save()

            send_mail(
                subject="Appointment Rejected - ClinicEasy",
                message=f"""
                Dear {appointment.patient_name},

                Unfortunately, your appointment has been Rejected.

                Doctor: {appointment.doctor.name}
                Date: {appointment.appointment_date}
                Time: {appointment.appointment_time}
                Status: Rejected

                Please try booking another on other time slot.

                Regards,
                ClinicEasy Team
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[appointment.email],
                fail_silently=False,
            )

            messages.warning(request, "Appointment rejected and email sent.")

        return redirect("doctor_dashboard")

    appointments = Appointment.objects.filter(
        doctor=doctor
    ).order_by("-appointment_date")

    return render(request, "doctor_dashboard.html", {
        "doctor": doctor,
        "appointments": appointments
    })

# BOOK APPOINTMENT
@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        appointment_date = request.POST.get("date")
        appointment_time = request.POST.get("time")

        if not phone or not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Enter a valid 10-digit phone number.")
            return redirect(request.path)
        if appointment_date < str(date.today()):
            messages.error(request, "You cannot select a past date.")
            return redirect(request.path)

        # CHECK IF SLOT IS ALREADY BOOKED
        slot_exists = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status__in=["Pending", "Approved"]
        ).exists()

        if slot_exists:
            messages.error(
                request,
                "This time slot is already booked. Please choose another time."
            )
            return redirect(request.path)

        Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            patient_name=name,
            email=email,
            phone=phone,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status="Pending"
        )

        #  SEND EMAIL
        send_mail(
            subject="Appointment Booked - ClinicEasy",
            message=f"""
               Dear {name},

               Your appointment has been successfully booked.

               Doctor: {doctor.name}
               Date: {appointment_date}
               Time: {appointment_time}
               Status: Pending

               Thank you for using ClinicEasy.
               """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, "Appointment booked successfully.")
        return redirect("my_appointments")

    return render(request, "appointment.html", {"doctor": doctor})

# MY APPOINTMENTS 
@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(
        patient=request.user
    ).order_by("-appointment_date")

    return render(request, "my_appointments.html", {
        "appointments": appointments
    })

# CANCEL APPOINTMENT
@login_required
def cancel_appointment(request, id):
    appointment = get_object_or_404(
        Appointment, id=id, patient=request.user )

    appointment.status = "Cancelled"
    appointment.save()

    send_mail(
    subject="Appointment Cancelled - ClinicEasy",
    message=f"""
        Dear {appointment.patient_name},

        Your appointment has been Cancelled.

        Doctor: {appointment.doctor.name}
        Date: {appointment.appointment_date}
        Time: {appointment.appointment_time}

        ClinicEasy Team
        """,
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[appointment.email],
    fail_silently=False,
)

    messages.success(request, "Appointment cancelled.")
    return redirect("my_appointments")


# RESCHEDULE APPOINTMENT
@login_required
def reschedule_appointment(request, id):
    appointment = get_object_or_404(
    Appointment, id=id,patient=request.user
     )

    if request.method == "POST":
        appointment.reschedule_date = request.POST["date"]
        appointment.reschedule_time = request.POST["time"]
        appointment.status = "Rescheduled"
        appointment.save()

        send_mail(
            subject="Appointment Rescheduled - ClinicEasy",
            message=f"""
                Dear {appointment.patient_name},

                Your appointment has been Rescheduled.

                Doctor: {appointment.doctor.name}
                New Date: {appointment.reschedule_date}
                New Time: {appointment.reschedule_time}

                Thank you for using ClinicEasy.
                """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            fail_silently=False,
            recipient_list=[appointment.email]
        )

        messages.success(request, "Appointment Rescheduled.")
        return redirect("my_appointments")

    return render(request, "appointments/reschedule.html", {
        "appointment": appointment
    })

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message_text = request.POST.get("message")

        if not name or not email or not subject or not message_text:
            messages.error(request, "All fields are required.")
            return redirect("contact")

        if len(message_text) < 10:
            messages.error(request, "Message must be at least 10 characters long.")
            return redirect("contact")

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_text
        )

        messages.error(request, "Your message has been sent successfully.")
        return redirect("contact")

    return render(request, "contact.html")
