from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Medecin)
admin.site.register(Patient)
admin.site.register(DossierPatient)
admin.site.register(Prescription)
admin.site.register(RendezVous)
admin.site.register(Visite)

