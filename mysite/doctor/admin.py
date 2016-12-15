from django.contrib import admin

from .models import Diagnose, Medicine, Price, Patient, Register

admin.site.register((Diagnose, Medicine, Price, Patient, Register))
