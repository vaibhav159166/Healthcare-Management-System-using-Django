from django.db import models
'''
class Appointment(models.Model):
    name = models.CharField(max_length=100) 
    doctor_id = models.IntegerField()
    clinic_username = models.CharField(max_length=100)
    appointment_date = models.DateField()
    time_slot = models.TimeField()
    reason_for_visit = models.TextField()


    class Meta:
        db_table = ''  # Explicitly set the table name

    def __str__(self):
        return f"Appointment for {self.name} with Doctor {self.doctor_id}"
'''