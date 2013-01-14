from django.core.management import call_command
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,render_to_response
from django.template import RequestContext

from .forms import ResetForm,AnalyzeForm
from .utils import getNeighCount,getPhonotacticProb,loadinPhonoStrings

def index(request):
    return render(request,'phonostats/index.html',{})

@login_required
def reset(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ResetForm(request.POST)
            if form.is_valid() and form.cleaned_data['reset']:
                call_command('reset','phonostats', interactive=False,verbosity=0)
                loadinPhonoStrings()
                return redirect(index)
        form = ResetForm()
        return render(request,'phonostats/form.html',{'form':form})

@login_required
def analyze(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = AnalyzeForm(request.POST)
            if form.is_valid():
                segs = form.cleaned_data['segments']
                nostress = form.cleaned_data['nostress']
                neighcount = getNeighCount(segs,no_stress=nostress)
                blick = getPhonotacticProb(segs,use_blick=True,no_stress=nostress)
                spbp = getPhonotacticProb(segs,use_blick=False,no_stress=nostress)
                return render(request,'phonostats/results.html',{'segments':segs,
                                                                    'neigh_den':neighcount,
                                                                    'blick':blick,
                                                                    'phone_probs':spbp})
        form = AnalyzeForm()
        return render(request,'phonostats/form.html',{'form':form})
