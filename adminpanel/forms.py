from accounts.models import Patient
from appointments.models import Appointment
from django import forms
from doctors.models import Doctor


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'user',
            'name',
            'department',
            'specialization',
            'experience',
            'description',
            'image',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['user', 'name', 'gender', 'blood_group','phone', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })


from django import forms
from appointments.models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'patient',
            'doctor',
            'patient_name',
            'email',
            'phone',
            'appointment_date',
            'appointment_time',
            'status',
        ]

        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
