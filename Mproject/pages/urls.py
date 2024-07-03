from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('patient/inscription/',views.inscription,name='inscription'),
    path('patient/<int:idpatient>/',views.patient_page , name = 'patient'),
    path('connexion/',views.connexion_page,name='connexion'),
    path('rendez_vous/<int:id>/', views.rendez_vous, name='rendez_vous'),
    path('voir_rendez_vous/<int:idpatient>/',views.voir_rendez_vous,name='voir_rendez_vous'),
    path('delete_rendez_vous/<int:rendezvous_id>/', views.delete_rendez_vous, name='delete_rendez_vous'),
    path('doctor_login/', views.doctor_login, name='doctor_login'),
    path('doctor/<int:id>',views.doctor,name='doctor'),
    path('faire_visite/<int:id>',views.faire_visite,name='faire_visite'),
    path('rendez_vous_doctor/<int:doctor_id>',views.voir_rendez_vous_doctor,name='rendez_vous_doctor'),
    path('visite/<int:idv>',views.visite , name='visite'),
    path('creer_visite/<int:rendezvous_id>',views.creer_visite,name='creer_visite'),
    path('patients_traites_par_medecin/<int:id_doctor>',views.patients_traites_par_medecin,name='patients_traites_par_medecin'),
    path('prescription_form/<int:id_medecin>/<int:id_patient>',views.prescription_form,name='prescription_form'),
    path('afficher_preinscription/<int:id_doctor>/<int:id_patient>',views.afficher_preinscription,name='afficher_preinscriptions'),
    path('dossier_medical/',views.dossier_medical,name="dossier_medical"),
    path('delete_preinscription/<int:id>/', views.delete_preinscription, name='delete_preinscription'),
    path('visite_details/<int:idVisite>',views.visite_details,name='visite_details'),




]