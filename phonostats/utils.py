import re
import os

from blick import BlickLoader

from .models import PhonoString

from .media.dictionary import word_list


def loadinPhonoStrings():
    ps = []
    for line in word_list:
        ps.append(PhonoString(Transcription=line,NoStress = re.sub('[0-9]','',line)))
    PhonoString.objects.bulk_create(ps)

any_segment = '[A-Z]{1,2}[0-2]{0,1}'

def getNeighCount(input_string,no_stress=False):
    if no_stress:
        input_string = re.sub('[0-9]','',input_string)
    phones = input_string.split(" ")
    patterns = []
    for i in range(len(phones)):
        patt = phones[:i] #Substitutions
        patt.append(any_segment)
        patt.extend(phones[i+1:])
        patterns.append('^'+' '.join(patt) +'$')
        patt = phones[:i] #Deletions
        patt.extend(phones[i+1:])
        patterns.append('^'+' '.join(patt) +'$')
        patt = phones[:i] #Insertions
        patt.append(any_segment)
        patt.extend(phones[i:])
        patterns.append('^'+' '.join(patt) +'$')
    if no_stress:
        qs = PhonoString.objects.filter(NoStress__regex = '|'.join(patterns))
    else:
        qs = PhonoString.objects.filter(Transcription__regex = '|'.join(patterns))
    return len(qs)

def getPhonotacticProb(input_string,use_blick=True,no_stress=False):
    if use_blick:
        if no_stress:
            b = BlickLoader(grammarType='NoStress')
        else:
            b = BlickLoader()
        return b.assessWord(str(input_string))
    if no_stress:
        input_string = re.sub('[0-9]','',input_string)
    SPprob = 0.0
    BPprob = 0.0
    phones = input_string.split(" ")
    for i in range(len(phones)):
        patt = [any_segment] * i
        patt.append(phones[i])
        pattern = '^'+' '.join(patt) +'.*$'
        totPattern = '^'+' '.join([any_segment] * (i+1)) +'.*$'
        if no_stress:
            count = len(PhonoString.objects.filter(NoStress__regex = pattern))
            totCount = len(PhonoString.objects.filter(NoStress__regex = totPattern))
        else:
            count = len(PhonoString.objects.filter(Transcription__regex = pattern))
            totCount = len(PhonoString.objects.filter(Transcription__regex = totPattern))
        SPprob += float(count) / float(totCount)
        if i != len(phones)-1:
            patt = [any_segment] * i
            patt.extend([phones[i],phones[i+1]])
            pattern = '^'+' '.join(patt) +'.*$'
            totPattern = '^'+' '.join([any_segment] * (i+2)) +'.*$'
            if no_stress:
                count = len(PhonoString.objects.filter(NoStress__regex = pattern))
                totCount = len(PhonoString.objects.filter(NoStress__regex = totPattern))
            else:
                count = len(PhonoString.objects.filter(Transcription__regex = pattern))
                totCount = len(PhonoString.objects.filter(Transcription__regex = totPattern))
            BPprob += float(count) / float(totCount)
    SPprob = SPprob / float(len(phones))
    BPprob = BPprob / float(len(phones)-1)
    return (SPprob,BPprob)
