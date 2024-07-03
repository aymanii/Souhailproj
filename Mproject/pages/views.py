from django.shortcuts import render , redirect ,get_object_or_404
from django.contrib.auth import authenticate, login
from datetime import date
from django.contrib import messages
from .forms import PatientForm , RendezVousForm 
from .models import Patient, RendezVous , Medecin , Visite , Prescription
# Create your views here.
def index(request):
    return render(request,'pages/index.html')

def inscription(request):
    form_patient = PatientForm()

    if request.method == 'POST':
        form_patient = PatientForm(request.POST)
        if form_patient.is_valid():
            email = form_patient.cleaned_data['email']
            if Patient.objects.filter(email=email).exists():
                form_patient.add_error('email', 'Email déjà utilisé. Veuillez utiliser une autre adresse.')
            else:
                patient = form_patient.save()
                return redirect('patient', idpatient=patient.id)
    return render(request, 'pages/inscription.html', {'patient_form': form_patient})

def patient_page(request, idpatient):
    patient = get_object_or_404(Patient, id=idpatient)
    return render(request, 'pages/patient.html', {'patient': patient})

def connexion_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Verify the user exists and retrieve the user instance
        user = Patient.objects.filter(email=email).first()
        
        if user:
            # Authenticate the user
            user_auth = authenticate(request, email=email, password=password)
            if user is not None:
                # Login the user
                login(request, user_auth)
                return redirect('patient', idpatient=user.id)
            else:
                error_message = 'Email ou mot de passe incorrect.'
        else:
            error_message = 'Email ou mot de passe incorrect.'

        return render(request, 'pages/connexion.html', {'error_message': error_message})
    
    return render(request, 'pages/connexion.html')

def rendez_vous(request, id):
    patient = get_object_or_404(Patient, id=id)
    
    if request.method == 'POST':
        form = RendezVousForm(request.POST)
        if form.is_valid():
            rendezvous = form.save(commit=False)
            rendezvous.patient = patient
            rendezvous.statut = "en attente"
            rendezvous.save()
            messages.success(request, 'Rendez vous est en attente maintenant.')
            return redirect('patient', idpatient=patient.id)
        
    else:
        form = RendezVousForm()
    
    return render(request, 'pages/rendez_vous.html', {'patient': patient, 'form': form})

def voir_rendez_vous(request, idpatient):
    patient = get_object_or_404(Patient, id=idpatient)
    rendezvous_list = RendezVous.objects.filter(patient=patient)
    return render(request, 'pages/voir_rendez_vous.html', {'patient': patient, 'rendezvous_list': rendezvous_list})


def delete_rendez_vous(request, rendezvous_id):
    rendezvous = get_object_or_404(RendezVous, pk=rendezvous_id)
    if request.method == 'POST':
        id = rendezvous.patient.id
        rendezvous.delete()
        return redirect('voir_rendez_vous', id)

    return redirect('voir_rendez_vous', id=rendezvous.patient.id)

def doctor_login(request):
    if request.method == 'POST':
        license_number = request.POST.get('license_number')

        try:
            doctor = Medecin.objects.get(licence=license_number)
            
            return redirect('doctor' , id = doctor.id)
        except Medecin.DoesNotExist:

            messages.error(request, 'Numéro de licence incorrect. Veuillez réessayer.')

    return redirect('connexion')

def doctor(request , id):
    doctor = get_object_or_404(Medecin,id=id)
    return render(request,'pages/doctor.html',{'doctor' : doctor})

def faire_visite(request , id ):
    doctor = get_object_or_404(Medecin,id=id)
    return render(request, 'pages/faire_visite.html', {'doctor':doctor,'patients': Patient.objects.all()})

def voir_rendez_vous_doctor(request, doctor_id):
    doctor = get_object_or_404(Medecin, id=doctor_id)
    rendezvous_list = RendezVous.objects.filter(medecin=doctor)
    return render(request, 'pages/rendez_vous_doctor.html', {
        'doctor': doctor,
        'rendezvous_list': rendezvous_list,
    })

def creer_visite(request, rendezvous_id):
    rendezvous = get_object_or_404(RendezVous, id=rendezvous_id)
    
    if request.method == 'POST':
        remarques = request.POST.get('remarques', '')
        visite = Visite.objects.create(
            dateVisite=rendezvous.dateHeure,
            motif=rendezvous.symptome,
            patient=rendezvous.patient,
            medecin=rendezvous.medecin,
            remarques=remarques  
        )
        rendezvous.statut = 'traité'
        rendezvous.save()
        return redirect('rendez_vous_doctor', doctor_id=rendezvous.medecin.id)
    
    return render(request, 'pages/creer_visite.html', {'rendezvous': rendezvous})

def visite(request,idv):
    rendezvous = get_object_or_404(RendezVous, id=idv)
    return render(request,'pages/visite.html',{'rendezvous' : rendezvous})

def patients_traites_par_medecin(request, id_doctor):
    doctor = get_object_or_404(Medecin, id=id_doctor)
    visites_list = Visite.objects.filter(medecin=doctor)

    return render(request, 'pages/patients_traites_par_medecin.html', {
        'medecin': doctor,
        'visites_list': visites_list,
    })


def prescription_form(request, id_medecin, id_patient):
    doctor = get_object_or_404(Medecin, id=id_medecin)
    patient = get_object_or_404(Patient, id=id_patient)

    if request.method == 'POST':
        medicaments = request.POST.get('medicaments')
        dosage = request.POST.get('dosage')
        instructions = request.POST.get('instructions')

        prescription = Prescription.objects.create(
            date=date.today(),
            medecin=doctor,
            patient=patient,
            medicaments=medicaments,
            dosage=dosage,
            instructions=instructions,
        )
    
        messages.success(request, f"Préinscription pour {patient.prenom} {patient.nom} créée avec succès.")

        return redirect('patients_traites_par_medecin', id_doctor=doctor.id)

    return render(request, 'pages/prescription_form.html', {'medecin': doctor, 'patient': patient})

def afficher_preinscription(request,id_doctor, id_patient):
    patient = get_object_or_404(Patient, id=id_patient)
    preinscriptions = Prescription.objects.filter(patient=patient)
    
    context = {
        'patient': patient,
        'preinscriptions': preinscriptions,
        'id_doctor' : id_doctor ,
    }
    return render(request, 'pages/afficher_preinscription.html', context)

def dossier_medical(request):
    return render(request,'pages/dossier_medical.html')

def delete_preinscription(request, id):
    preinscription = get_object_or_404(Prescription, id=id)
    patient_id = preinscription.patient.id
    doctor_id = preinscription.medecin.id
    preinscription.delete()
    return redirect('afficher_preinscriptions',id_doctor=doctor_id , id_patient=patient_id)

def visite_details(request, idVisite):
    visite = get_object_or_404(Visite, id=idVisite)
    return render(request, 'pages/visite_details.html', {'visite': visite})
