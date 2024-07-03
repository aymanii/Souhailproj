from django.db import models

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    dateNaissance = models.DateField()
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=100) 
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.nom} {self.prenom}"

class Medecin(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)
    licence = models.CharField(max_length=10)

    def _str_(self):
        return f"Dr. {self.nom} {self.prenom}"

class DossierPatient(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    traitementsEnCours = models.TextField()


    def historique_consultations(self):

        historiqueConsultations = Visite.objects.filter(dossierPatient=self)
        return historiqueConsultations
    
    def _str_(self):
        return f"Dossier de {self.patient.nom} {self.patient.prenom}"

class RendezVous(models.Model):
    id = models.AutoField(primary_key=True)
    dateHeure = models.DateTimeField()
    statut = models.CharField(max_length=50)
    symptome = models.CharField(max_length=255)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, null=True)
    checking = models.BooleanField(default=False)

    def _str_(self):
        return f"Rendez-vous {self.statut} le {self.dateHeure} avec {self.medecin.nom} {self.medecin.prenom}"

class Prescription(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medicaments = models.TextField()
    dosage = models.TextField()
    instructions = models.TextField()

    def _str_(self):
        return f"Prescription de {self.medecin.nom} pour {self.patient.nom} le {self.date}"

class Visite(models.Model):
    id = models.AutoField(primary_key=True)
    dateVisite = models.DateTimeField()
    motif = models.CharField(max_length=255)
    remarques = models.TextField(blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    dossierPatient = models.ForeignKey(DossierPatient, on_delete=models.CASCADE , null=True)

    def _str_(self):
        return f"Visite le {self.dateVisite} pour {self.motif}"