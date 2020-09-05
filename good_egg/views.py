from django.shortcuts import render, redirect
from .models import Incident
from .models import Officer
from django.contrib.auth.decorators import login_required

# Create your views here.
def landing_page(request):
    return render(request, 'landing_page.html')

def incident_list(req):
  incidents = Incident.objects.all()
  return render(req, 'good_egg/incident_list.html', {'incidents': incidents}) 

def officer_list(req):
  officers = Officer.objects.all()
  return render(req, 'good_egg/officer_list.html', {'officers': officers})

def incident_detail(req, pk):
  incident = Incident.objects.get(id=pk)
  return render(req, 'good_egg/incident_detail.html', {'incident': incident})

def officer_detail(req, pk):
  officer = Officer.objects.get(id=pk)
  return render(req, 'good_egg/officer_detail.html', {'officer': officer})

@login_required
def incident_create(req):
    if req.method == 'POST':
        form = IncidentForm(req.POST)
        if form.is_valid():
            incident = form.save()
            return redirect('incident_detail', pk=incident.pk)
    else:
        form = IncidentForm()
    return render(req, 'good_egg/incident_form.html', {'form': form})

# Admin Auth
# @login_required  
# def officer_create(req):
#     if req.method == 'POST':
#         form = officerForm(req.POST)
#         if form.is_valid():
#             officer = form.save()
#             return redirect('officer_detail', pk=officer.pk)
#     else:
#         form = officerForm()
#     return render(req, 'good_egg/officer_form.html', {'form': form})

@login_required  
def incident_edit(req, pk):
    incident = Incident.objects.get(pk=pk)
    if req.method == 'POST':
      form = IncidentForm(req.POST, instance=incident)
      if form.is_valid():
        incident = form.save()
        return redirect('incident_detail', pk=incident.pk)
    else:
        form = IncidentForm(instance=incident)
    return render(req, 'good_egg/incident_form.html', {'form': form})
  
#  Admin Auth 
# @login_required  
# def officer_edit(req, pk):
#     officer = officer.objects.get(pk=pk)
#     if req.method == "POST":
#       form = officerForm(req.POST, instance=officer)
#       if form.is_valid():
#         officer = form.save()
#         return redirect('officer_detail', pk=officer.pk)
#     else:
#         form = officerForm(instance=officer)
#     return render(req, 'good_egg/officer_form.html', {'form': form})
  
@login_required  
def incident_delete(req, pk):
  Incident.objects.get(id=pk).delete()
  return redirect('incident_list')

# Admin auth
# @login_required
# def officer_delete(req, pk):
#   officer.objects.get(id=pk).delete()
#   return redirect('officer_list')