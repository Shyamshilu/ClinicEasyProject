import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ClinicEasy.settings')
django.setup()

from django.contrib.auth.models import User
from doctors.models import Doctor

data = [
    ("drrahul@gmail.com", "Dr. Rahul Patel", "Cardiology", "Cardiologist", 20, "Heart specialist with advanced treatment experience.", "Ahmedabad"),
    ("drmehul@gmail.com", "Dr. Mehul Shah", "Neurology", "Neurologist", 11, "Specialist in brain and nerve disorders.", "Rajkot"),
    ("drpooja@gmail.com", "Dr. Pooja Joshi", "Pediatrics", "Pediatrician", 10, "Focused on child healthcare and growth.", "Ahmedabad"),
    ("drvishal@gmail.com", "Dr. Vishal Trivedi", "Orthopedics", "Orthopedic Surgeon", 17, "Expert in bone and joint surgeries.", "Rajkot"),
    ("drheena@gmail.com", "Dr. Heena Desai", "Dermatology", "Dermatologist", 9, "Skin care and cosmetic specialist.", "Ahmedabad"),
    ("drmanish@gmail.com", "Dr. Manish Bhatt", "Oncology", "Oncologist", 13, "Cancer specialist with modern treatments.", "Rajkot"),
    ("drsneha@gmail.com", "Dr. Sneha Pandya", "Radiology", "Radiologist", 8, "Expert in MRI and CT scan diagnosis.", "Ahmedabad"),
    ("drnikhil@gmail.com", "Dr. Nikhil Vyas", "Emergency", "Emergency Medicine", 12, "Handles trauma and emergency cases.", "Rajkot"),
    ("drankit@gmail.com", "Dr. Ankit Dave", "Cardiology", "Cardiologist", 15, "Experienced in heart surgeries.", "Ahmedabad"),
    ("drkrunal@gmail.com", "Dr. Krunal Patel", "Dermatology", "Dermatologist", 7, "Skin specialist with modern techniques.", "Rajkot"),
]

added_count = 0
skipped_count = 0

for email, name, dept, spec, exp, desc, loc in data:
    if not User.objects.filter(username=email).exists():
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password="doctor123"
            )
            
            Doctor.objects.create(
                user=user,
                name=name,
                department=dept,
                specialization=spec,
                experience=exp,
                description=desc,
                location=loc
            )
            print(f"✓ Added: {name} ({spec})")
            added_count += 1
        except Exception as e:
            print(f"✗ Error adding {name}: {str(e)}")
    else:
        print(f"⊘ Skipped: {name} (already exists)")
        skipped_count += 1

print(f"\n✓ Successfully added: {added_count} doctors")
print(f"⊘ Skipped (already exist): {skipped_count} doctors")
print(f"Total doctors in database: {Doctor.objects.count()}")
