import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ClinicEasy.settings')
django.setup()

from doctors.models import Doctor
from django.contrib.auth.models import User

new_doctors = ['drrahul', 'drmehul', 'drpooja', 'drvishal', 'drheena', 'drmanish', 'drsneha', 'drnikhil', 'drankit', 'drkrunal']

print("Checking Doctor records for the 10 new doctors:")
print("-" * 50)

missing = []
for username in new_doctors:
    email = f"{username}@gmail.com"
    user_exists = User.objects.filter(username=email).exists()
    doctor_exists = Doctor.objects.filter(user__username=email).exists()
    
    status = "✓" if doctor_exists else "✗"
    print(f"{status} {email}: User={user_exists}, Doctor={doctor_exists}")
    
    if not doctor_exists:
        missing.append(email)

print("-" * 50)
print(f"\nTotal new doctors in database: {len([u for u in new_doctors if Doctor.objects.filter(user__username=f'{u}@gmail.com').exists()])}/10")
print(f"Total all doctors in database: {Doctor.objects.count()}")

if missing:
    print(f"\nMissing Doctor records for: {missing}")
    print("\nCreating missing Doctor records...")
    
    data = {
        "drrahul@gmail.com": ("Dr. Rahul Patel", "Cardiology", "Cardiologist", 20, "Heart specialist with advanced treatment experience.", "Ahmedabad"),
        "drmehul@gmail.com": ("Dr. Mehul Shah", "Neurology", "Neurologist", 11, "Specialist in brain and nerve disorders.", "Rajkot"),
        "drpooja@gmail.com": ("Dr. Pooja Joshi", "Pediatrics", "Pediatrician", 10, "Focused on child healthcare and growth.", "Ahmedabad"),
        "drvishal@gmail.com": ("Dr. Vishal Trivedi", "Orthopedics", "Orthopedic Surgeon", 17, "Expert in bone and joint surgeries.", "Rajkot"),
        "drheena@gmail.com": ("Dr. Heena Desai", "Dermatology", "Dermatologist", 9, "Skin care and cosmetic specialist.", "Ahmedabad"),
        "drmanish@gmail.com": ("Dr. Manish Bhatt", "Oncology", "Oncologist", 13, "Cancer specialist with modern treatments.", "Rajkot"),
        "drsneha@gmail.com": ("Dr. Sneha Pandya", "Radiology", "Radiologist", 8, "Expert in MRI and CT scan diagnosis.", "Ahmedabad"),
        "drnikhil@gmail.com": ("Dr. Nikhil Vyas", "Emergency", "Emergency Medicine", 12, "Handles trauma and emergency cases.", "Rajkot"),
        "drankit@gmail.com": ("Dr. Ankit Dave", "Cardiology", "Cardiologist", 15, "Experienced in heart surgeries.", "Ahmedabad"),
        "drkrunal@gmail.com": ("Dr. Krunal Patel", "Dermatology", "Dermatologist", 7, "Skin specialist with modern techniques.", "Rajkot"),
    }
    
    for email in missing:
        user = User.objects.get(username=email)
        name, dept, spec, exp, desc, loc = data[email]
        Doctor.objects.create(
            user=user,
            name=name,
            department=dept,
            specialization=spec,
            experience=exp,
            description=desc,
            location=loc
        )
        print(f"  ✓ Created Doctor for {name}")

print(f"\nFinal count: {Doctor.objects.count()} total doctors in database")
