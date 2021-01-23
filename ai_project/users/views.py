from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import userdetails  
from .models import fitnessmen
from .models import fitnesswomen
from .models import Breakfast
from .models import Lunch
from .models import Snacks
from .models import Dinner
from .models import Water
from .models import Likes
from .models import Dislikes
from django.db.models import F
from django.db.models import Prefetch
from django.http import HttpResponse

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import pyttsx3  
import speech_recognition as sr
from fuzzywuzzy import fuzz
import re
import math
from datetime import date
from sklearn.preprocessing import MinMaxScaler 
from jinja2 import Template
from django.template.defaulttags import register
from numpy import dot
from numpy.linalg import norm
from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize 
import os


@register.filter
def get_range(value):
    return range(value)


def register(request):
    if request.method == 'POST':
    #     form = UserRegisterForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         username = form.cleaned_data.get('username') 
        # user_name = request.user.get_username()
        user_name = userdetails.objects.values_list('user_name', flat=True).get(id = userdetails.objects.last().id)
        gender = userdetails.objects.values_list('gender', flat=True).get(id = userdetails.objects.last().id)
        if(gender=='Male'):
            fitnessmen.objects.filter(id = fitnessmen.objects.last().id).update(user_name = user_name)
        else:
            fitnesswomen.objects.filter(id = fitnesswomen.objects.last().id).update(user_name = user_name)
        messages.success(request, f'Your account has been created! You are now able to log in')
        return redirect('login')
      


@login_required
def profile(request):
    breakfast_list, lunch_list, dinner_list, snacks_list = [],[],[],[]
    request.session['breakfast_list'] = breakfast_list
    request.session['lunch_list'] = lunch_list
    request.session['dinner_list'] = dinner_list
    request.session['snacks_list'] = snacks_list       
    request.session['food'] = ""
    request.session['rec'] = ""
    return redirect('tdee')
    # return render(request, 'users/profile.html')

def indext(request):
    return render(request, 'users/indext.html')  


def intermediate(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data.get('username')
            request.session['user_name'] = user_name
            oref = userdetails(user_name = user_name)
            oref.save()
            # user_name = request.user.get_username()
        if(request.user.is_authenticated):
            obj = userdetails.objects.get(user_name = user_name)
            return render(request, 'users/demographics.html',{'name':obj.name,'age':obj.age,'gender':obj.gender,'state':obj.state, 'template':'blog/base1.html'})  
        else:
            
            return render(request, 'users/demographics.html', {'template':'blog/base.html'})
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form}) 



import datetime

def daterange(dates, num):
    start_date = dates

    date_list = []
    for day in range(num):
        a_date = (start_date + datetime.timedelta(days = day)).isoformat()
        date_list.append(a_date)
    return date_list


def graph(request):
    import json
    user_name = request.user.get_username()
    gender = userdetails.objects.values_list('gender', flat=True).get(user_name=user_name)
    weights=[]
    choice = request.POST.get('choice')
    if(gender == 'Male'):
        period = request.POST.get('period')
        weights=[]
        weights = list(fitnessmen.objects.filter(user_name=user_name).values_list('Weight', flat=True))
        weights = [float(x) for x in weights]
        
        obj = fitnessmen.objects.filter(user_name = user_name).values_list('Height', 'Weight', 'weekly_goal', 'Abdomen', 'Neck', 'date')
        obj_list = [list(x) for x in obj]
        dates = [str(x[-1]) for x in obj_list]
                
        year = [str(x[-1]).split('-')[0] for x in obj_list]
        month = [str(x[-1]).split('-')[1] for x in obj_list]
        day = [str(x[-1]).split('-')[2] for x in obj_list]
        
        if Water.objects.filter(user_name=user_name).exists():
            water_obj = list(Water.objects.filter(user_name=user_name).values_list('amount', 'date'))
            dates_water = [str(x[-1]) for x in water_obj]
            water = [float(x[0]) for x in water_obj]
            
            if choice=='Water':
                year = [str(x[-1]).split('-')[0] for x in water_obj]
                month = [str(x[-1]).split('-')[1] for x in water_obj]
                day = [str(x[-1]).split('-')[2] for x in water_obj]
        
        day1, month1, year1 = int(day[0]), int(month[0]), int(year[0])
        dayn, monthn, yearn = int(day[-1]), int(month[-1]), int(year[-1])

        a_date1 = datetime.date(yearn, monthn, dayn)
        a_date = a_date1 + datetime.timedelta(1)
        days = datetime.timedelta(365)
        new_date = a_date - days
        datesrange = daterange(new_date, 365)
        data = []
        bfp = [495/(1.0324 - 0.19077 * math.log10(float(i[3]) * 2.54 - float(i[4]) * 2.54)  + 0.15456 * math.log10(float(i[0]) * 2.54))- 450 for i in obj_list]
        if(choice=='Body fat percentage'):
            data = compute(datesrange, dates, bfp)
            ylab, title = 'Body Fat Percentage', 'YOUR BODY FAT PERCENTAGE'
        elif(choice=='Water'):
            ylab, title = 'Water Intake (glasses)', 'YOUR WATER INTAKE'
            if Water.objects.filter(user_name=user_name).exists():
                data = compute(datesrange, dates_water, water)
        else:
            data = compute(datesrange, dates, weights)
            ylab, title = 'Weight (in kg)', 'YOUR WEIGHT'

    if(gender == 'Female'):
        period = request.POST.get('period')
        weights=[]
        weights = list(fitnesswomen.objects.filter(user_name=user_name).values_list('Weight', flat=True))
        weights = [float(x) for x in weights]
        
        obj = fitnesswomen.objects.filter(user_name = user_name).values_list('Height', 'Weight', 'weekly_goal', 'Hip', 'Waist', 'Neck', 'date')
        obj_list = [list(x) for x in obj]
        dates = [str(x[-1]) for x in obj_list]

        year = [str(x[-1]).split('-')[0] for x in obj_list]
        month = [str(x[-1]).split('-')[1] for x in obj_list]
        day = [str(x[-1]).split('-')[2] for x in obj_list]

        if Water.objects.filter(user_name=user_name).exists():
            water_obj = list(Water.objects.filter(user_name=user_name).values_list('amount', 'date'))
            dates_water = [str(x[-1]) for x in water_obj]
            water = [float(x[0]) for x in water_obj]
            
            if choice=='Water':
                year = [str(x[-1]).split('-')[0] for x in water_obj]
                month = [str(x[-1]).split('-')[1] for x in water_obj]
                day = [str(x[-1]).split('-')[2] for x in water_obj]

        day1, month1, year1 = int(day[0]), int(month[0]), int(year[0])
        dayn, monthn, yearn = int(day[-1]), int(month[-1]), int(year[-1])

        a_date1 = datetime.date(yearn, monthn, dayn)
        a_date = a_date1 + datetime.timedelta(1)
        days = datetime.timedelta(365)
        new_date = a_date - days
        datesrange = daterange(new_date, 365)
        data = []
        bfp = [495 / (1.29579 - .35004 * math.log10(float(i[4]) * 2.54 + float(i[3]) * 2.54 - float(i[5]) * 2.54) + .22100 * math.log10(float(i[0]) * 2.54)) - 450 for i in obj_list]
        
        if(choice=='Body fat percentage'):
            data = compute(datesrange, dates, bfp)
            ylab, title = 'Body Fat Percentage', 'YOUR BODY FAT PERCENTAGE'
        elif(choice=='Water'):
            ylab, title = 'Water Intake (glasses)', 'YOUR WATER INTAKE'
            if Water.objects.filter(user_name=user_name).exists():
                data = compute(datesrange, dates_water, water)
        else:
            data = compute(datesrange, dates, weights)
            ylab, title = 'Weight (in kg)', 'YOUR WEIGHT'
        
    return render(request, 'users/graph.html', {'weights':data, 'months': datesrange, 'title':json.dumps(title), 'ylab':json.dumps(ylab) })

def compute(datesrange, dates, var):
    wts = []
    for i in datesrange:
        if str(i) in str(dates):
            wts.append(var[dates.index(i)])
        else:
            try:
                ind = [n for n,x in enumerate(dates) if str(x) < i][-1]
                wts.append(var[ind])
            except:
                wts.append(var[0])
    return wts



def update_userdets(request):
    user_name = request.user.get_username()
    
    pg = request.POST.get("page")
    name = request.POST.get("Name")   
    age = request.POST.get("Age")     
    gender = request.POST.get("Gender")
    state = request.POST.get("State")

    food_preference = request.POST.get("preference")
    food_type = request.POST.get("ftype")

    
    if(pg == 'demo'):
        a, b = ['name', 'age', 'gender', 'state'], [name, age, gender, state]
        
    elif(pg == 'demographics'):
        a, b = ['food_preference', 'food_type'], [food_preference, food_type]
        
    ob = userdetails.objects.filter(user_name = user_name).values_list(*a)
    list_ob = list(ob[0])
    dets = userdetails.objects.get(user_name=user_name)
    for i in range(len(list_ob)):
        if(list_ob[i] != b[i] and b[i] != ''):
            setattr(dets, a[i], b[i])
            dets.save()
        else:
            setattr(dets, a[i], list_ob[i])
            dets.save()
    obj = userdetails.objects.get(user_name=user_name)
    # return render(request, 'users/demographics.html',{'name':obj.name,'age':obj.age,'gender':obj.gender,'state':obj.state, 'template': 'blog/base1.html'})
    return redirect(pg)


def update_fitness(request):
    today = str(date.today())
    user_name = request.user.get_username()
    pg = request.POST.get("page")
    # a,b = [],[]
    goals = request.POST.get("goals")  
    activity = request.POST.get("activity")   
    goalweight = request.POST.get("goal_weight")
    weekly_goal = request.POST.get("weekly_goal") 

    gen = list(userdetails.objects.filter(user_name=user_name).values_list('gender', flat=True))
    
    if(gen[0] == 'Male'):
        
        Height = request.POST.get("Height")
        Weight = request.POST.get("Weight")
        Abdomen = request.POST.get("Abdomen")
        Neck = request.POST.get("Neck")
    elif(gen[0] == 'Female'):
        Height = request.POST.get("Height")
        Weight = request.POST.get("Weight")
        Waist  = request.POST.get("Waist")
        Hip = request.POST.get("Hip")
        Neck = request.POST.get("Neck")

    if(pg == 'preference'):
        a, b = ['goals', 'activity', 'goalweight', 'weekly_goal'], [goals, activity, goalweight, weekly_goal]
        if(gen[0] == 'Male'):
            c, d = ['Height', 'Weight', 'Abdomen', 'Neck'], [Height, Weight, Abdomen, Neck]
            ob = fitnessmen.objects.filter(user_name = user_name).values_list(*a)
            # ob = fitnesswomen.objects.filter(user_name = user_name).last()
            list_ob = list(ob)[-1]
            dets = fitnessmen.objects.filter(user_name = user_name).last()
            for i in range(len(list_ob)):    
                if(list_ob[i] != b[i] and b[i] != ''):
                    setattr(dets, a[i], b[i])
                    dets.save()
                else:
                    setattr(dets, a[i], list_ob[i])
                    dets.save()

            ob1 = fitnessmen.objects.filter(user_name = user_name).values_list(*c)
            # ob = fitnesswomen.objects.filter(user_name = user_name).last()
            list_ob1 = list(ob1)[-1]
            dets1 = fitnessmen.objects.filter(user_name = user_name).last()
            for i in range(len(d)):    
                setattr(dets1, c[i], list_ob1[i])
                dets1.save()

        elif(gen[0] == 'Female'):
            c, d = ['Height', 'Weight', 'Hip', 'Waist', 'Neck'], [Height, Weight, Hip, Waist, Neck]
            ob = fitnesswomen.objects.filter(user_name = user_name).values_list(*a)
            # ob = fitnesswomen.objects.filter(user_name = user_name).last()
            list_ob = list(ob)[-1]
            dets = fitnesswomen.objects.filter(user_name = user_name).last()

            for i in range(len(list_ob)):    
                if(list_ob[i] != b[i] and b[i] != ''):
                    setattr(dets, a[i], b[i])
                    dets.save()
                else:
                    setattr(dets, a[i], list_ob[i])
                    dets.save()

            ob1 = fitnesswomen.objects.filter(user_name = user_name).values_list(*c)
            # ob = fitnesswomen.objects.filter(user_name = user_name).last()
            list_ob1 = list(ob1)[-1]
            dets1 = fitnesswomen.objects.filter(user_name = user_name).last()
            for i in range(len(d)):    
                setattr(dets1, c[i], list_ob1[i])
                dets1.save()

        

    elif(pg == 'goals'):        
        if(gen[0] == 'Male'):
            a, b, x, y = ['Height', 'Weight', 'Abdomen', 'Neck'], [Height, Weight, Abdomen, Neck], ['Height', 'Weight', 'Abdomen', 'Neck'], [Height, Weight, Abdomen, Neck]
            c, d = ['goals', 'activity', 'goalweight', 'weekly_goal'], [goals, activity, goalweight, weekly_goal]
            dat = list(fitnessmen.objects.filter(user_name=user_name).values_list('date', flat=True))[-1]
            ob = fitnessmen.objects.filter(user_name = user_name).values_list(*a)
            # ob = fitnesswomen.objects.filter(user_name = user_name).last()
            list_ob = list(ob)[-1]
            dets = fitnessmen.objects.filter(user_name = user_name).last()
            for i in range(1,len(x)):
                ob2 = fitnessmen.objects.filter(user_name = user_name).values_list(*x)
                list_ob2 = list(ob2)[-1]
                if(list_ob2[i] != y[i] and y[i] != '' and str(dat) != today):
                    oref = fitnessmen(user_name=user_name)
                    oref.save()
                    dets = fitnessmen.objects.filter(user_name = user_name).last()
                    setattr(dets, x[i], y[i])
                    dets.save()
                    dets = fitnessmen.objects.get(user_name=user_name, date=today)
                    a.remove(x[i])
                    b.remove(y[i])
                    ob = fitnessmen.objects.filter(user_name = user_name).values_list(*a)
                    # ob = fitnesswomen.objects.filter(user_name = user_name).last()
                    list_ob = list(ob)[-2]

                    ob1 = fitnessmen.objects.filter(user_name = user_name).values_list(*c)
                    # ob = fitnesswomen.objects.filter(user_name = user_name).last()
                    list_ob1 = list(ob1)[-2]
                
                

            for i in range(len(list_ob)):    
                if(list_ob[i] != b[i] and b[i] != ''):
                    setattr(dets, a[i], b[i])
                    dets.save()
                else:
                    setattr(dets, a[i], list_ob[i])
                    dets.save()

            ob1 = fitnessmen.objects.filter(user_name = user_name).values_list(*c)
            # ob = fitnesswomen.objects.filter(user_name = user_name).last()
            list_ob1 = list(ob1)[-2]
            dets1 = fitnessmen.objects.filter(user_name = user_name).last()
            for i in range(len(d)):    
                setattr(dets1, c[i], list_ob1[i])
                dets1.save()
            
        elif(gen[0] == 'Female'):
            a, b, x, y = ['Height', 'Weight', 'Hip', 'Waist', 'Neck'], [Height, Weight, Hip, Waist, Neck], ['Height', 'Weight', 'Hip', 'Waist', 'Neck'], [Height, Weight, Hip, Waist, Neck]
            c, d = ['goals', 'activity', 'goalweight', 'weekly_goal'], [goals, activity, goalweight, weekly_goal]
            dat = list(fitnesswomen.objects.filter(user_name=user_name).values_list('date', flat=True))[-1]
            ob = fitnesswomen.objects.filter(user_name = user_name).values_list(*a)
            # ob = fitnesswomen.objects.filter(user_name = user_name).last()
            list_ob = list(ob)[-1]
            dets = fitnesswomen.objects.filter(user_name = user_name).last()
            for i in range(1,len(x)):
                ob2 = fitnesswomen.objects.filter(user_name = user_name).values_list(*x)
                list_ob2 = list(ob2)[-1]
                if(list_ob2[i] != y[i] and y[i] != '' and str(dat) != today):
                    oref = fitnesswomen(user_name=user_name)
                    oref.save()
                    dets = fitnesswomen.objects.filter(user_name = user_name).last()
                    setattr(dets, x[i], y[i])
                    dets.save()
                    dets = fitnesswomen.objects.get(user_name=user_name, date=today)
                    a.remove(x[i])
                    b.remove(y[i])
                    ob = fitnesswomen.objects.filter(user_name = user_name).values_list(*a)
                    # ob = fitnesswomen.objects.filter(user_name = user_name).last()
                    list_ob = list(ob)[-2]

                    ob1 = fitnesswomen.objects.filter(user_name = user_name).values_list(*c)
                    # ob = fitnesswomen.objects.filter(user_name = user_name).last()
                    list_ob1 = list(ob1)[-2]
                
                

            for i in range(len(list_ob)):    
                if(list_ob[i] != b[i] and b[i] != ''):
                    setattr(dets, a[i], b[i])
                    dets.save()
                else:
                    setattr(dets, a[i], list_ob[i])
                    dets.save()

            ob1 = fitnesswomen.objects.filter(user_name = user_name).values_list(*c)
            # ob = fitnesswomen.objects.filter(user_name = user_name).last()
            list_ob1 = list(ob1)[-2]
            dets1 = fitnesswomen.objects.filter(user_name = user_name).last()
            for i in range(len(d)):    
                setattr(dets1, c[i], list_ob1[i])
                dets1.save()
    return redirect(pg)
    


def demo(request):
    if(request.user.is_authenticated):   
        user_name = request.user.get_username() 
        obj = userdetails.objects.get(user_name=user_name)
        return render(request, 'users/demographics.html',{'name':obj.name,'age':obj.age,'gender':obj.gender,'state':obj.state, 'template': 'blog/base1.html'})  
    else:
        return render(request, 'users/demographics.html', {'template': 'blog/base.html'})

def demographics(request):  
    user_name = request.user.get_username()  
    if(request.user.is_authenticated):
        obj = userdetails.objects.get(user_name = user_name)        
        return render(request, 'users/preference.html', {'food_preference': obj.food_preference, 'food_type': obj.food_type, 'template': 'blog/base1.html'})  
    else:
        name = request.POST.get("Name")   
        age = request.POST.get("Age")     
        gender = request.POST.get("Gender")
        state = request.POST.get("State")
        userdetails.objects.filter(id = userdetails.objects.last().id).update(name=name, age=age, gender=gender, state=state)
        return render(request, 'users/preference.html', {'template': 'blog/base.html'})

def preference(request): 
    user_name = request.user.get_username()
    if(request.user.is_authenticated):
        gender = userdetails.objects.values_list('gender', flat=True).get(user_name = user_name)
        if(gender=='Male'):  
            obj = fitnessmen.objects.filter(user_name = user_name).last()
            return render(request, 'users/goals.html', {'activity': obj.activity, 'goals': obj.goals,'goalweight':obj.goalweight,'weeklygoal':obj.weekly_goal, 'template': 'blog/base1.html'})
        else:   
            obj = fitnesswomen.objects.filter(user_name = user_name).last()
            return render(request, 'users/goals.html', {'activity': obj.activity, 'goals': obj.goals,'goalweight':obj.goalweight,'weeklygoal':obj.weekly_goal, 'template': 'blog/base1.html'})  
    else:
        food_preference = request.POST.get("preference")
        food_type = request.POST.get("type")
        userdetails.objects.filter(id = userdetails.objects.last().id).update(food_preference=food_preference, food_type=food_type)
        return render(request, 'users/goals.html', {'template': 'blog/base.html'}) 

def goals(request): 
    
    if(request.user.is_authenticated):
        user_name = request.user.get_username()
        gender = userdetails.objects.values_list('gender', flat=True).get(user_name = user_name)
        if(gender=='Male'):  
            obj = fitnessmen.objects.filter(user_name = user_name).last()
            return render(request, 'users/measurements.html', {'height':obj.Height,'weight':obj.Weight,'abdomen':obj.Abdomen,'neck':obj.Neck, 'gender':gender, 'template': 'blog/base1.html'})
        else:   
            obj = fitnesswomen.objects.filter(user_name = user_name).last()
            return render(request, 'users/measurements.html', {'height':obj.Height,'weight':obj.Weight,'waist':obj.Waist,'neck':obj.Neck,'hip':obj.Hip, 'gender':gender, 'template': 'blog/base1.html'})
    else:
        goals = request.POST.get("goals")  
        activity = request.POST.get("activity")   
        goalweight = request.POST.get("goal_weight")
        weekly_goal = request.POST.get("weekly_goal")  
        # user_name = request.user.get_username()
        user_name = request.session['user_name']
        # user_name = userdetails.objects.values_list('user_name', flat=True).get(id = userdetails.objects.last().id)
        gender = userdetails.objects.values_list('gender', flat=True).get(id = userdetails.objects.last().id)
        if(gender=="Male"):  
            o_ref = fitnessmen(user_name = user_name)
            o_ref.save()
            fitnessmen.objects.filter(id = fitnessmen.objects.last().id).update(goals=goals, activity=activity, goalweight=goalweight, weekly_goal=weekly_goal)
        if(gender=="Female"):
            # o_ref = fitnesswomen(user_name = user_name)
            # o_ref.save()
            fitnesswomen.objects.filter(id = fitnesswomen.objects.last().id).update(goals=goals, activity=activity, goalweight=goalweight, weekly_goal=weekly_goal)
        return render(request, 'users/measurements.html', {'gender':gender, 'template': 'blog/base.html'})  


def measurements(request):
    user_name = request.user.get_username()
    gender = userdetails.objects.values_list('gender', flat=True).get(id = userdetails.objects.last().id)  
    if(gender=="Male"):  
        Height = request.POST.get("Height")
        Weight = request.POST.get("Weight")
        Abdomen = request.POST.get("Abdomen")
        Neck = request.POST.get("Neck")
        # oref = fitnessmen(user_name = user_name)
        # oref.save()
        fitnessmen.objects.filter(id = fitnessmen.objects.last().id).update(Height = Height, Weight=Weight, Abdomen=Abdomen, Neck=Neck)
        
    if(gender=="Female"):
        Height = request.POST.get("Height")
        Weight = request.POST.get("Weight")
        Waist  = request.POST.get("Waist")
        Hip = request.POST.get("Hip")
        Neck = request.POST.get("Neck")
        # oref = fitnesswomen(user_name = user_name)
        # oref.save()
        fitnesswomen.objects.filter(id = fitnesswomen.objects.last().id).update(Height = Height, Weight=Weight, Waist=Waist, Hip=Hip, Neck=Neck)
        
    return register(request)

def tdee(request):
    user_name = request.user.get_username()
    gender = userdetails.objects.values_list('gender', flat=True).get(user_name = user_name)  
    act_dict = {'Sedentary':1.53, 'Moderately Active':1.76, 'Highly Active':2.25}
    
    if(gender=="Male"):
        obj = fitnessmen.objects.filter(user_name = user_name).last()
        cal_diff = (float(obj.weekly_goal) * 3500)/(0.45 * 7)             
    if(gender=="Female"):                                     
        obj = fitnesswomen.objects.filter(user_name = user_name).last()
        cal_diff = (float(obj.weekly_goal) * 3500)/(0.45 * 7)
        
    try:
        bfp = 495 / (1.29579 - .35004 * math.log10(float(obj.Waist) * 2.54 + float(obj.Hip) * 2.54 - float(obj.Neck) * 2.54) + .22100 * math.log10(float(obj.Height) * 2.54)) - 450
    except:
        bfp = 495/(1.0324 - 0.19077 * math.log10(float(obj.Abdomen) * 2.54 - float(obj.Neck) * 2.54)  + 0.15456 * math.log10(float(obj.Height) * 2.54))- 450
    
    lean_mass = float(obj.Weight) * (1 - (bfp/100))
    bmr = 370 + (21.6 * lean_mass)
    tdee = bmr * act_dict[obj.activity]  
    diff_dict = {'Lose Weight': tdee - cal_diff , 'Gain Weight': tdee + cal_diff, 'Maintain Weight': tdee}
    request.session['cons'] = int(diff_dict[obj.goals])
    return render(request, 'users/profile.html', {'bfp': round(bfp,2),'tdee':int(tdee), 'cons':int(diff_dict[obj.goals]), 'username':user_name})

def food_items(request):
    today = str(date.today())
    user_name = request.user.get_username()
    # try:
    #     bf_prev_user = Breakfast.objects.last().user_name
    #     lu_prev_user = Lunch.objects.last().user_name
    #     sn_prev_user = Snacks.objects.last().user_name
    #     di_prev_user = Dinner.objects.last().user_name
    #     if((today > str(Breakfast.objects.order_by('-date').first().date)) or (user_name != bf_prev_user)):
    #         if(Breakfast.objects.filter(user_name=user_name).order_by('-date').first() != today):
    #             request.session['breakfast_list'] = []
    #     if((today > str(Lunch.objects.order_by('-date').first().date)) or (user_name != lu_prev_user)):
    #         if(Lunch.objects.filter(user_name=user_name).order_by('-date').first() != today):
    #             request.session['lunch_list'] = []
    #     if((today > str(Snacks.objects.order_by('-date').first().date)) or (user_name != sn_prev_user)):
    #         if(Snacks.objects.filter(user_name=user_name).order_by('-date').first() != today):
    #             request.session['snacks_list'] = []
    #     if((today > str(Dinner.objects.order_by('-date').first().date)) or (user_name != di_prev_user)):
    #         if(Dinner.objects.filter(user_name=user_name).order_by('-date').first() != today):
    #             request.session['dinner_list'] = []
    # except:
    #     request.session['breakfast_list'] = []
    #     request.session['lunch_list'] = []
    #     request.session['snacks_list'] = []
    #     request.session['dinner_list'] = []
    

    request.session['food'] = ""
    request.session['rec'] = ""
    request.session['foods'] = []
    request.session['unit'] = []
    return render(request,'users/food_items.html')


def record(request):  
    rec= request.POST.get('record')  
    request.session['rec'] = rec
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'nutri1.csv')
    data = pd.read_csv(file_path)
    clean_data = preprocess(data)
    r= sr.Recognizer()
    with  sr.Microphone() as source:
        print(" Speak something you like: ")
        audio = r.adjust_for_ambient_noise(source, duration = 1)
        audio_text = r.listen(source)
    
    try:
        output = " " + r.recognize_google(audio_text)
        matches = similar_words(output, clean_data, count = 0)
    except:
        output = "Could not understand audio"
        
    dict1 = {'output': output, 'rec':rec}
    dict1['name'] = rec.upper()
    if(output != 'Could not understand audio'):
        food = matches.iloc[:5,0].values.tolist()
        count = range(0,5)
        dict1['food'] = dict(zip(count, food)) 
        request.session['foods'] = food
        request.session['amount'] = matches.iloc[:5,1].values.tolist()
        request.session['cals'] = matches.iloc[:5, 2].values.tolist()      
        request.session['carbs'] = matches.iloc[:5,3].values.tolist()
        request.session['fats'] = matches.iloc[:5,4].values.tolist()
        request.session['protein'] = matches.iloc[:5,5].values.tolist()
        
        # request.session['success'] = 'true'
        # success = request.session['success']
    return render(request,'users/voicereg.html', dict1)


def voicereg(request):
    return render(request, 'users/voicereg.html')


    
def food_info(request):
    food_index = int(request.POST.get('food_index'))   
    food = request.session['foods'][food_index]
    request.session['food'] = food
    amount = float(request.session['amount'][food_index].split()[0])  
    unit = request.session['amount'][food_index].split()[1]   
    request.session['unit'] = unit
    cals = int(request.session['cals'][food_index])
    carbs = int(request.session['carbs'][food_index])
    fats = int(request.session['fats'][food_index])
    protein = int(request.session['protein'][food_index])
    rec = request.session['rec']
    # food_details = [food, amount, unit, cals, carbs, protein, fats]
    # request.session['food_details'] = food_details
    
    return render(request, 'users/food_info.html', {'rec': rec, 'food': food, 'amount': amount, 'unit': unit, 'cals':cals,'carbs':carbs,'fats':fats,'protein':protein})

def weighted_distance(user_name, dict2, n_neighbors):
    # X_test = ['Karnataka', 22, 'F', 'Veg', 'South Indian']
    X_test = userdetails.objects.filter(user_name = user_name).values_list('state', 'age', 'gender', 'food_type', 'food_preference')
    
    X_test = list(X_test[0])
    # df = userdetails.objects.exclude(user_name = user_name).values_list('Breakfast__food_names', 'Lunch__food_names', 'Snacks__food_names', 'Dinner__food_names')   
    X_train = userdetails.objects.exclude(user_name = user_name).values_list('user_name', 'state', 'age', 'gender', 'food_type', 'food_preference')    
    X_train = [list(x) for x in X_train]
    X_train = pd.DataFrame(X_train, columns = ['Username', 'State', 'Age', 'Gender', 'Type', 'Preference'])
    
    # y = df.iloc[:,len(X_test)] 
    dataset = X_train.drop('Username', axis=1).append(pd.Series(X_test, index = X_train.columns[1:]), ignore_index = True)
    user_features = pd.concat([pd.get_dummies(dataset['State'], prefix='State'), dataset['Age'], pd.get_dummies(dataset['Gender'], prefix='Gender'), pd.get_dummies(dataset['Type'], prefix='Type'),pd.get_dummies(dataset["Preference"],prefix='Preference') ],axis=1)
       
    dataset_preprocessed = MinMaxScaler().fit_transform(user_features) 
    train = user_features[:len(X_train)]   
    test = user_features[len(X_train):]
    train_preprocessed = dataset_preprocessed[:len(X_train)]
    test_preprocessed = dataset_preprocessed[len(X_train):]
    row_no=[]
    dum_col = user_features.columns
    dist = []
    for i in range(len(train)):
        row_no.append(i)
        sq_dist = []
        dict_col = {"State":10 ,"Age":1, "Gender":0.5, "Type":50, "Preference":20}
        for j in range(len(dum_col)):
            sq_dist.append(((test_preprocessed[0][j] - train_preprocessed[i][j]) ** 2) * dict_col[dum_col[j].split("_")[0]])
        dist.append(sq_dist) 

    weighted_dist = [[np.sqrt(sum(dist[x])), x] for x in range(len(dist))]
    indices = np.array(sorted(weighted_dist))[:,1].astype(int)
    distances = np.array(sorted(weighted_dist))[:,0]
    return indices[:n_neighbors], X_train, X_test


def content(request, user_name, flag, rec):
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'nutri.csv')
    flag = 0
    flag = request.POST.get('flag')
    rec1 = eval(rec)
    df = pd.read_csv(file_path)
    df = df.dropna()
    df.drop_duplicates(inplace = True)
    ty = list(userdetails.objects.filter(user_name=user_name).values_list('food_type', flat=True))
    if(ty[0]=='Vegetarian'):
        ty = ['Eggetarian', 'Vegetarian']
        df = df.loc[(df['Type'].isin(ty)),:]
    meal = df['Meal_type'].str.split('/').apply(lambda x: str(x))
    df = df.loc[meal.apply(lambda x: rec in x)].reset_index(drop=True)
    df = df.loc[df.Categories == 'Healthy'].reset_index(drop=True)
    for row in range(len(df)): 
        df.iat[row, 1] = re.sub('[^a-zA-Z]+', ' ', df.iat[row, 1])
        df.iat[row, 0] = re.sub('[^a-zA-Z]+', ' ', df.iat[row, 0])
        df.iat[row, 1] = re.sub('[0-9]+[^0-9]', ' ', df.iat[row, 1])
        df.iat[row, 0] = re.sub('[0-9]+[^0-9]', ' ', df.iat[row, 0])

        if(df.iat[row, 1].lower() == df.iat[row, 0].lower()):
            df.iat[row, 1] = 'Generic'
    df['Food'] = df['Food'] + '-' + df['Category']

    if not rec1.objects.filter(user_name=user_name).exists():
        foo = list(rec1.objects.exclude(user_name=user_name).values_list('food_names', flat=True))
        like = list(Likes.objects.exclude(user_name=user_name).values_list('food_names', flat=True))
        food = [x for x in foo + like if x in list(df['Food'])]
        foods = pd.Series(sorted(food,key=food.count,reverse=True)).drop_duplicates()[:7]
        df_new = pd.concat([df['Food'], pd.get_dummies(df['Region']), pd.get_dummies(df['Type'])], axis=1) 

        stop_words = stopwords.words('english') 
        newStopWords = ['ac','accurate', 'used']
        stop_words.extend(newStopWords)
        stop_words = set(stop_words)
        tok = df['Food'].str.replace('-', ' ').str.lower().str.rstrip().apply(word_tokenize)
        b=[]
        for x in tok: 
            a = [i for i in x if i not in stop_words]
            b.append(a)
        
        dums = pd.Series(b).apply(set).apply(list).apply(' '.join).str.split(expand=True)
        dums = pd.get_dummies(dums, prefix="").groupby(level=0, axis=1).sum()
        data = pd.concat([df_new.reset_index(drop=True), pd.get_dummies(dums, prefix="")], axis=1)
        data['total'] = data.drop('Food', axis=1).apply(sum, axis=1)
        docf = data.drop('Food', axis=1).apply(sum, axis=0)
        idf = docf.apply(lambda x: np.log(len(data)/x))
        features = data.drop(['Food', 'total'], axis=1).div(np.sqrt(data.total), axis=0)
        food_likes, food_dislikes = [], []

        if(flag=='1'):
            likes=''
            likes = request.POST.get('like')
            dislikes=''
            dislikes = request.POST.get('dislike')
            
            if Likes.objects.filter(user_name=user_name).exists():
                food_likes = list(Likes.objects.filter(user_name=user_name).values_list('food_names', flat=True))
            else:
                food_likes = []

            if Dislikes.objects.filter(user_name=user_name).exists():
                food_dislikes = list(Dislikes.objects.filter(user_name=user_name).values_list('food_names', flat=True))
            else:
                food_dislikes = []
            
            if(likes != '' and likes not in food_likes):
                if(likes in food_dislikes):
                    Dislikes.objects.filter(food_names=likes, user_name=user_name).delete()
                oref = Likes(user_name=user_name, food_names=likes)
                oref.save()
            
            
            if(dislikes != '' and dislikes not in food_dislikes):
                if(dislikes in food_likes):
                    Likes.objects.filter(food_names=dislikes, user_name=user_name).delete()
                oref = Dislikes(user_name=user_name, food_names=dislikes)
                oref.save()

        
        if Likes.objects.filter(user_name=user_name).exists():
            food_likes = list(Likes.objects.filter(user_name=user_name).values_list('food_names', flat=True))
        if Dislikes.objects.filter(user_name=user_name).exists():
            food_dislikes = list(Dislikes.objects.filter(user_name=user_name).values_list('food_names', flat=True))
            # data['user_pref'] = data['Food'].apply(lambda x: 1 if x in foo else 0)

        data['user_pref'] = data['Food'].apply(lambda x: 1 if x in food_likes else(-1 if x in food_dislikes else 0))

        user_pro = features.apply(lambda x: pd.Series(x).dot(pd.Series(data['user_pref'])), axis=0)
        recom = features.apply(lambda x: np.sum(x * user_pro * idf), axis=1)
        food_rec = data.loc[recom.nlargest(40).index, 'Food'].str.lower().apply(lambda x: x.split('-')[0])
        foods = data.loc[food_rec.drop_duplicates().index,'Food']
        foods = data.loc[foods.str.replace('-',' ').str.replace(' ', ',').str.lower().str.rstrip().str.split(',').apply(lambda x: x[0]).drop_duplicates().index, 'Food'][:7]

    else:
        df_new = pd.concat([df['Food'], pd.get_dummies(df['Region']), pd.get_dummies(df['Type'])], axis=1) 

        stop_words = stopwords.words('english') 
        newStopWords = ['ac','accurate', 'used']
        stop_words.extend(newStopWords)
        stop_words = set(stop_words)
        tok = df['Food'].str.replace('-', ' ').str.lower().str.rstrip().apply(word_tokenize)
        b=[]
        for x in tok: 
            a = [i for i in x if i not in stop_words]
            b.append(a)
        
        dums = pd.Series(b).apply(set).apply(list).apply(' '.join).str.split(expand=True)
        dums = pd.get_dummies(dums, prefix="").groupby(level=0, axis=1).sum()
        data = pd.concat([df_new.reset_index(drop=True), pd.get_dummies(dums, prefix="")], axis=1)
        data['total'] = data.drop('Food', axis=1).apply(sum, axis=1)
        docf = data.drop('Food', axis=1).apply(sum, axis=0)
        idf = docf.apply(lambda x: np.log(len(data)/x))
        features = data.drop(['Food', 'total'], axis=1).div(np.sqrt(data.total), axis=0)
        food_likes, food_dislikes = [], []

        if(flag=='1'):
            likes=''
            likes = request.POST.get('like')
            dislikes=''
            dislikes = request.POST.get('dislike')
            
            if(likes != '' and likes not in list(Likes.objects.filter(user_name=user_name).values_list('food_names', flat=True))):
                if(likes in list(Dislikes.objects.filter(user_name=user_name).values_list('food_names', flat=True))):
                    Dislikes.objects.filter(food_names=likes, user_name=user_name).delete()
                oref = Likes(user_name=user_name, food_names=likes)
                oref.save()
            
            if(dislikes != '' and dislikes not in list(Dislikes.objects.filter(user_name=user_name).values_list('food_names', flat=True))):
                if(dislikes in list(Likes.objects.filter(user_name=user_name).values_list('food_names', flat=True))):
                    Likes.objects.filter(food_names=dislikes, user_name=user_name).delete()
                oref = Dislikes(user_name=user_name, food_names=dislikes)
                oref.save()

        
        if Likes.objects.filter(user_name=user_name).exists():
            food_likes = list(Likes.objects.filter(user_name=user_name).values_list('food_names', flat=True))
        if Dislikes.objects.filter(user_name=user_name).exists():
            food_dislikes = list(Dislikes.objects.filter(user_name=user_name).values_list('food_names', flat=True))
            # data['user_pref'] = data['Food'].apply(lambda x: 1 if x in foo else 0)

        
        foo = list(rec1.objects.filter(user_name=user_name).values_list('food_names', flat=True))
        foo = [x for x in foo if x not in food_dislikes]
        data['user_pref'] = data['Food'].apply(lambda x: 1 if x in foo + food_likes else(-1 if x in food_dislikes else 0))

        user_pro = features.apply(lambda x: pd.Series(x).dot(pd.Series(data['user_pref'])), axis=0)
        recom = features.apply(lambda x: np.sum(x * user_pro * idf), axis=1)
        food_rec = data.loc[recom.nlargest(40).index, 'Food'].str.lower().apply(lambda x: x.split('-')[0])
        foods = data.loc[food_rec.drop_duplicates().index,'Food']
        foods = data.loc[foods.str.replace('-',' ').str.replace(' ', ',').str.lower().str.rstrip().str.split(',').apply(lambda x: x[0]).drop_duplicates().index, 'Food'][:7]

    return foods




def rules(dict2, user_name):
    tab = eval(dict2['tab'])
    if not tab.objects.filter(user_name=user_name).exists():
        dict2['rec_food'] = []
    # dict2 = request.session['dict2']
    else:
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'nutri.csv')
        df = pd.read_csv(file_path)
        df = df.dropna()
        df.drop_duplicates(inplace = True)
        reg = list(userdetails.objects.filter(user_name=user_name).values_list('food_preference', flat=True))[0]
        # df = df.loc[df['Region']==reg, :]
        df = df.loc[df['Categories']=='Healthy',:]
        ty = list(userdetails.objects.filter(user_name=user_name).values_list('food_type', flat=True))[0]
        if(ty == 'Vegetarian'):
            df = df.loc[df['Type']=='Vegetarian',:]
        # foods.fillna('Nil', inplace = True)
        for row in range(len(df)): 
            df.iat[row, 1] = re.sub('[^a-zA-Z]+', ' ', df.iat[row, 1])
            df.iat[row, 0] = re.sub('[^a-zA-Z]+', ' ', df.iat[row, 0])
            df.iat[row, 1] = re.sub('[0-9]+[^0-9]', ' ', df.iat[row, 1])
            df.iat[row, 0] = re.sub('[0-9]+[^0-9]', ' ', df.iat[row, 0])

            if(df.iat[row, 1].lower() == df.iat[row, 0].lower()):
                df.iat[row, 1] = 'Generic'
        df['Food'] = df['Food'] + '-' + df['Category']
        
        # meal = df['Meal_type'].str.split('/').apply(lambda x: str(x))
        # df = df.loc[meal.apply(lambda x: rec in x)]
        indices, X_train, X_test = weighted_distance(user_name, dict2, n_neighbors = 10)
        
        # foo = list(tab.objects.exclude(user_name = user_name).values_list('food_names', flat=True))
        recom_users = X_train.loc[indices, 'Username'].tolist()
        foo = list(tab.objects.filter(user_name__in = recom_users).values_list('food_names', flat=True))
        like = list(Likes.objects.filter(user_name__in = recom_users).values_list('food_names', flat=True))
        food = foo + like
        fo = [] 
        for i in food:
            if(i in list(df['Food'])):
                fo.append(i)
                
        dict2['rec_food'] = fo[:6]

    
    return dict2

def preprocess(data):
    data.dropna(inplace = True)
    for row in range(len(data)): 
        data.iat[row, 1] = re.sub('[^a-zA-Z]+', ' ', data.iat[row, 1])
        data.iat[row, 0] = re.sub('[^a-zA-Z]+', ' ', data.iat[row, 0])
        data.iat[row, 1] = re.sub('[0-9]+[^0-9]', ' ', data.iat[row, 1])
        data.iat[row, 0] = re.sub('[0-9]+[^0-9]', ' ', data.iat[row, 0])

        if(data.iat[row, 1].lower() == data.iat[row, 0].lower()):
            data.iat[row, 1] = 'Generic'
    data['Food'] = data['Food'] + '-' + data['Category']
    return data[['Food', 'Amount', 'Calories', 'Carbs(in g)', 'Fat(in g)', 'Protein(in g)']]

def water(request):
    today = date.today()
    user_name = request.user.get_username()
    flag = 0
    amt = request.POST.get('water')
    
    if Water.objects.filter(user_name=user_name).exists():
        flag = 1
        obj = list(Water.objects.filter(user_name=user_name))
        if(str(obj[-1].date) != str(today)):
            if(amt is not None):
                oref = Water(user_name=user_name, amount=amt)
                oref.save()

            
        else:
            if(amt is not None):
                Water.objects.filter(user_name=user_name, date=today).update(amount=amt)
        amount = list(Water.objects.filter(user_name=user_name).values_list('amount', flat=True))
        return render(request, 'users/water.html', {'amt':amount[-1], 'flag': flag, 'per': amount[-1]/8*100})

    else:
        if(amt is not None):
            flag = 1
            oref = Water(user_name=user_name, amount=amt)
            oref.save()
            obj = Water.objects.get(user_name=user_name)
            return render(request, 'users/water.html', {'flag': flag, 'amt': obj.amount, 'per': obj.amount/8*100})
        
    return render(request, 'users/water.html', {'flag': flag})

def breakfast(request):
    flag = request.POST.get('flag')
    if(flag == ''):
        flag = 0
    today = str(date.today())
    success = 'false'
    user_name = request.user.get_username()
    success = request.POST.get('success')
    food = request.session['food']
    cons = request.session['cons']
    
    carb_cal = 0.6 * cons  
    pro_cal = 0.2 * cons
    fat_cal = 0.2 * cons
    carb_grams = carb_cal/4
    pro_grams = pro_cal/4
    fat_grams = fat_cal/9


    foods = list(Breakfast.objects.filter(user_name = user_name, date=today).values_list('food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats'))
    if(len(foods) != 0):
        success = 'true'
        request.session['rec'] = 'Breakfast'
    status = request.POST.get('status')
     
    rec = request.session['rec']
    dict2 = {'rec': rec}
    dict2['tab'] = 'Breakfast'
    # dict2['user'] = user_name
    if(success == 'true'):
        request.session['success'] = 'false'
        
        # food_details = request.session['food_details'] 
        amount = request.POST.get('amount')
        cals = request.POST.get('cal')
        carbs = request.POST.get('carb')
        protein = request.POST.get('pro')
        fats = request.POST.get('fat')
        unit = request.POST.get('unit')

        if(status == 'delete'):
            ind = int(request.POST.get('ind'))   
            Breakfast.objects.filter(food_id=ind, user_name=user_name, date=today).delete()  
            Breakfast.objects.filter(food_id__gt=ind, user_name=user_name, date=today).update(food_id=F('food_id')-1)
            foods = list(Breakfast.objects.filter(user_name = user_name, date=today).values_list('food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats'))
            # del foods[ind]
            # request.session['snacks_list'] = foods     
            if(len(foods) == 0): 
                dict22 = rules(dict2, user_name) 
                dict22['content'] = content(request, user_name, flag, rec='Breakfast')
                return render(request, 'users/breakfast.html', dict22) 
                 
            dict_keys = ['food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats']
            foodlist = [dict(zip(dict_keys, a)) for a in foods]
            shakal = sum([x['calories'] for x in foodlist])
            shakcarb = sum([x['carbs'] for x in foodlist])
            shakpro = sum([x['proteins'] for x in foodlist])
            shakfat = sum([x['fats'] for x in foodlist])
            calper = int(shakal/(cons/4)*100)  
            carbper = int(shakcarb/(carb_grams/4)*100)
            proper = int(shakpro/(pro_grams/4)*100)
            fatper = int(shakfat/(fat_grams/4)*100)
            # foods.append(food)
            index = range(len(foodlist))                             
            # index = range(len(foods))
            dict2['food_dict'] = dict(zip(index, foodlist))
            dict2['cum'] = {'calories':calper,'carbs':carbper,'prot':proper,'fat':fatper, 'gcarb':shakcarb, 'gpro':shakpro, 'gfat':shakfat, 'gcal':shakal, 'tcarb':int(carb_grams/4), 'tpro':int(pro_grams/4), 'tfat':int(fat_grams/4), 'tcal':int(cons/4), 'name': 'BREAKFAST'}
            dict22 = rules(dict2, user_name)
            dict22['content'] = content(request, user_name, flag, rec='Breakfast')
            return render(request, 'users/displayfood.html', dict22)     
         
        elif(status == 'add'):
            ind = len(foods)
            o_ref = Breakfast(food_id = ind, user_name=user_name, food_names=food, amount = amount, unit = unit, calories = cals, carbs = carbs,proteins=protein,fats=fats) 
            o_ref.save()  
            foods = Breakfast.objects.filter(user_name = user_name, date=today).values_list('food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats')
            dict_keys = ['food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats']
            foodlist = [dict(zip(dict_keys, a)) for a in foods]
            shakal = sum([x['calories'] for x in foodlist])
            shakcarb = sum([x['carbs'] for x in foodlist])
            shakpro = sum([x['proteins'] for x in foodlist])
            shakfat = sum([x['fats'] for x in foodlist])
            calper = int(shakal/(cons/4)*100)  
            carbper = int(shakcarb/(carb_grams/4)*100)
            proper = int(shakpro/(pro_grams/4)*100)
            fatper = int(shakfat/(fat_grams/4)*100)
            # foods.append(food)
            index = range(len(foodlist))                             
            # index = range(len(foods))
            dict2['food_dict'] = dict(zip(index, foodlist))
            dict2['cum'] = {'calories':calper,'carbs':carbper,'prot':proper,'fat':fatper, 'gcarb':shakcarb, 'gpro':shakpro, 'gfat':shakfat, 'gcal':shakal, 'tcarb':int(carb_grams/4), 'tpro':int(pro_grams/4), 'tfat':int(fat_grams/4), 'tcal':int(cons/4), 'name': 'BREAKFAST'}
            dict22 = rules(dict2, user_name)      
            dict22['content'] = content(request, user_name, flag, rec='Breakfast')
            return render(request, 'users/displayfood.html', dict22)
       
        dict_keys = ['food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats']
        foodlist = [dict(zip(dict_keys, a)) for a in foods]
        shakal = sum([x['calories'] for x in foodlist])
        shakcarb = sum([x['carbs'] for x in foodlist])
        shakpro = sum([x['proteins'] for x in foodlist])
        shakfat = sum([x['fats'] for x in foodlist])
        calper = int(shakal/(cons/4)*100)  
        carbper = int(shakcarb/(carb_grams/4)*100)
        proper = int(shakpro/(pro_grams/4)*100)
        fatper = int(shakfat/(fat_grams/4)*100)


        # foods.append(food)
        index = range(len(foodlist))                             
        # index = range(len(foods))
        dict2['food_dict'] = dict(zip(index, foodlist))
        dict2['cum'] = {'calories':calper,'carbs':carbper,'prot':proper,'fat':fatper, 'gcarb':shakcarb, 'gpro':shakpro, 'gfat':shakfat, 'gcal':shakal, 'tcarb':int(carb_grams/4), 'tpro':int(pro_grams/4), 'tfat':int(fat_grams/4), 'tcal':int(cons/4), 'name': 'BREAKFAST'}
        dict22 = rules(dict2, user_name)
        dict22['content'] = content(request, user_name, flag, rec='Breakfast')
        return render(request, 'users/displayfood.html', dict22)
    else:
        request.session['success'] = success
        dict22 = rules(dict2, user_name)
        dict22['content'] = content(request, user_name, flag, rec='Breakfast')
        # dict2['user_name'] = user_name  
        return render(request,'users/breakfast.html', dict22)



def lunch(request):
    flag = request.POST.get('flag')
    if(flag == ''):
        flag = 0
    today = str(date.today())
    success = 'false'
    user_name = request.user.get_username()
    success = request.POST.get('success')
    food = request.session['food']
    cons = request.session['cons']
    
    carb_cal = 0.6 * cons  
    pro_cal = 0.2 * cons
    fat_cal = 0.2 * cons
    carb_grams = carb_cal/4
    pro_grams = pro_cal/4
    fat_grams = fat_cal/9


    foods = list(Lunch.objects.filter(user_name = user_name, date=today).values_list('food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats'))
    if(len(foods) != 0):
        success = 'true'
        request.session['rec'] = 'Lunch'
    status = request.POST.get('status')
     
    rec = request.session['rec']
    dict2 = {'rec': rec}
    dict2['tab'] = 'Lunch'
    # dict2['user'] = user_name
    if(success == 'true'):
        request.session['success'] = 'false'
        
        # food_details = request.session['food_details'] 
        amount = request.POST.get('amount')
        cals = request.POST.get('cal')
        carbs = request.POST.get('carb')
        protein = request.POST.get('pro')
        fats = request.POST.get('fat')
        unit = request.POST.get('unit')

        if(status == 'delete'):
            ind = int(request.POST.get('ind'))   
            Lunch.objects.filter(food_id=ind, user_name=user_name, date=today).delete()  
            Lunch.objects.filter(food_id__gt=ind, user_name=user_name, date=today).update(food_id=F('food_id')-1)
            foods = list(Lunch.objects.filter(user_name = user_name, date=today).values_list('food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats'))
            # del foods[ind]
            # request.session['snacks_list'] = foods     
            if(len(foods) == 0):  
                dict22 = rules(dict2, user_name)
                dict22['content'] = content(request, user_name, flag, rec='Lunch')
                # dict2['user_name'] = user_name  
                return render(request,'users/lunch.html', dict22)
                        
            dict_keys = ['food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats']
            foodlist = [dict(zip(dict_keys, a)) for a in foods]
            shakal = sum([x['calories'] for x in foodlist])
            shakcarb = sum([x['carbs'] for x in foodlist])
            shakpro = sum([x['proteins'] for x in foodlist])
            shakfat = sum([x['fats'] for x in foodlist])
            calper = int(shakal/(cons/4)*100)  
            carbper = int(shakcarb/(carb_grams/4)*100)
            proper = int(shakpro/(pro_grams/4)*100)
            fatper = int(shakfat/(fat_grams/4)*100)
            # foods.append(food)
            index = range(len(foodlist))                             
            # index = range(len(foods))
            dict2['food_dict'] = dict(zip(index, foodlist))
            dict2['cum'] = {'calories':calper,'carbs':carbper,'prot':proper,'fat':fatper, 'gcarb':shakcarb, 'gpro':shakpro, 'gfat':shakfat, 'gcal':shakal, 'tcarb':int(carb_grams/4), 'tpro':int(pro_grams/4), 'tfat':int(fat_grams/4), 'tcal':int(cons/4), 'name': 'LUNCH'}
            dict22 = rules(dict2, user_name)
            dict22['content'] = content(request, user_name, flag, rec='Lunch')
            return render(request, 'users/displayfood.html', dict22)     
         
        elif(status == 'add'):
            ind = len(foods)
            o_ref = Lunch(food_id = ind, user_name=user_name, food_names=food, amount = amount, unit = unit, calories = cals, carbs = carbs,proteins=protein,fats=fats) 
            o_ref.save()  
            foods = Lunch.objects.filter(user_name = user_name, date=today).values_list('food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats')
            dict_keys = ['food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats']
            foodlist = [dict(zip(dict_keys, a)) for a in foods]
            shakal = sum([x['calories'] for x in foodlist])
            shakcarb = sum([x['carbs'] for x in foodlist])
            shakpro = sum([x['proteins'] for x in foodlist])
            shakfat = sum([x['fats'] for x in foodlist])
            calper = int(shakal/(cons/4)*100)  
            carbper = int(shakcarb/(carb_grams/4)*100)
            proper = int(shakpro/(pro_grams/4)*100)
            fatper = int(shakfat/(fat_grams/4)*100)
            # foods.append(food)
            index = range(len(foodlist))                             
            # index = range(len(foods))
            dict2['food_dict'] = dict(zip(index, foodlist))
            dict2['cum'] = {'calories':calper,'carbs':carbper,'prot':proper,'fat':fatper, 'gcarb':shakcarb, 'gpro':shakpro, 'gfat':shakfat, 'gcal':shakal, 'tcarb':int(carb_grams/4), 'tpro':int(pro_grams/4), 'tfat':int(fat_grams/4), 'tcal':int(cons/4), 'name': 'LUNCH'}
            dict22 = rules(dict2, user_name)      
            dict22['content'] = content(request, user_name, flag, rec='Lunch') 
            return render(request, 'users/displayfood.html', dict22)
       
        dict_keys = ['food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats']
        foodlist = [dict(zip(dict_keys, a)) for a in foods]
        shakal = sum([x['calories'] for x in foodlist])
        shakcarb = sum([x['carbs'] for x in foodlist])
        shakpro = sum([x['proteins'] for x in foodlist])
        shakfat = sum([x['fats'] for x in foodlist])
        calper = int(shakal/(cons/4)*100)  
        carbper = int(shakcarb/(carb_grams/4)*100)
        proper = int(shakpro/(pro_grams/4)*100)
        fatper = int(shakfat/(fat_grams/4)*100)


        # foods.append(food)
        index = range(len(foodlist))                             
        # index = range(len(foods))
        dict2['food_dict'] = dict(zip(index, foodlist))
        dict2['cum'] = {'calories':calper,'carbs':carbper,'prot':proper,'fat':fatper, 'gcarb':shakcarb, 'gpro':shakpro, 'gfat':shakfat, 'gcal':shakal, 'tcarb':int(carb_grams/4), 'tpro':int(pro_grams/4), 'tfat':int(fat_grams/4), 'tcal':int(cons/4), 'name': 'LUNCH'}
        dict22 = rules(dict2, user_name)
        dict22['content'] = content(request, user_name, flag, rec='Lunch')
        return render(request, 'users/displayfood.html', dict22)
    else:
        request.session['success'] = success
        dict22 = rules(dict2, user_name)
        dict22['content'] = content(request, user_name, flag, rec='Lunch')
        # dict2['user_name'] = user_name  
        return render(request,'users/lunch.html', dict22)


def snacks(request):
    flag = request.POST.get('flag')
    if(flag == ''):
        flag = 0
    today = str(date.today())
    success = 'false'
    user_name = request.user.get_username()
    success = request.POST.get('success')
    food = request.session['food']
    cons = request.session['cons']
    
    carb_cal = 0.6 * cons  
    pro_cal = 0.2 * cons
    fat_cal = 0.2 * cons
    carb_grams = carb_cal/4
    pro_grams = pro_cal/4
    fat_grams = fat_cal/9


    foods = list(Snacks.objects.filter(user_name = user_name, date=today).values_list('food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats'))
    if(len(foods) != 0):
        success = 'true'
        request.session['rec'] = 'Snacks'
    status = request.POST.get('status')
     
    rec = request.session['rec']
    dict2 = {'rec': rec}
    dict2['tab'] = 'Snacks'
    # dict2['user'] = user_name
    if(success == 'true'):
        request.session['success'] = 'false'
        
        # food_details = request.session['food_details'] 
        amount = request.POST.get('amount')
        cals = request.POST.get('cal')
        carbs = request.POST.get('carb')
        protein = request.POST.get('pro')
        fats = request.POST.get('fat')
        unit = request.POST.get('unit')

        if(status == 'delete'):
            ind = int(request.POST.get('ind'))   
            Snacks.objects.filter(food_id=ind, user_name=user_name, date=today).delete()  
            Snacks.objects.filter(food_id__gt=ind, user_name=user_name, date=today).update(food_id=F('food_id')-1)
            foods = list(Snacks.objects.filter(user_name = user_name, date=today).values_list('food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats'))
            # del foods[ind]
            # request.session['snacks_list'] = foods     
            if(len(foods) == 0):  
                dict22 = rules(dict2, user_name)
                dict22['content'] = content(request, user_name, flag, rec='Snacks')
                # dict2['user_name'] = user_name  
                return render(request,'users/snacks.html', dict22)
                 
            dict_keys = ['food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats']
            foodlist = [dict(zip(dict_keys, a)) for a in foods]
            shakal = sum([x['calories'] for x in foodlist])
            shakcarb = sum([x['carbs'] for x in foodlist])
            shakpro = sum([x['proteins'] for x in foodlist])
            shakfat = sum([x['fats'] for x in foodlist])
            calper = int(shakal/(cons/4)*100)  
            carbper = int(shakcarb/(carb_grams/4)*100)
            proper = int(shakpro/(pro_grams/4)*100)
            fatper = int(shakfat/(fat_grams/4)*100)
            # foods.append(food)
            index = range(len(foodlist))                             
            # index = range(len(foods))
            dict2['food_dict'] = dict(zip(index, foodlist))
            dict2['cum'] = {'calories':calper,'carbs':carbper,'prot':proper,'fat':fatper, 'gcarb':shakcarb, 'gpro':shakpro, 'gfat':shakfat, 'gcal':shakal, 'tcarb':int(carb_grams/4), 'tpro':int(pro_grams/4), 'tfat':int(fat_grams/4), 'tcal':int(cons/4), 'name': 'SNACKS'}
            dict22 = rules(dict2, user_name)
            dict22['content'] = content(request, user_name, flag, rec='Snacks')
            return render(request, 'users/displayfood.html', dict22)     
         
        elif(status == 'add'):
            ind = len(foods)
            o_ref = Snacks(food_id = ind, user_name=user_name, food_names=food, amount = amount, unit = unit, calories = cals, carbs = carbs,proteins=protein,fats=fats) 
            o_ref.save()  
            foods = Snacks.objects.filter(user_name = user_name, date=today).values_list('food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats')
            dict_keys = ['food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats']
            foodlist = [dict(zip(dict_keys, a)) for a in foods]
            shakal = sum([x['calories'] for x in foodlist])
            shakcarb = sum([x['carbs'] for x in foodlist])
            shakpro = sum([x['proteins'] for x in foodlist])
            shakfat = sum([x['fats'] for x in foodlist])
            calper = int(shakal/(cons/4)*100)  
            carbper = int(shakcarb/(carb_grams/4)*100)
            proper = int(shakpro/(pro_grams/4)*100)
            fatper = int(shakfat/(fat_grams/4)*100)
            # foods.append(food)
            index = range(len(foodlist))                             
            # index = range(len(foods))
            dict2['food_dict'] = dict(zip(index, foodlist))
            dict2['cum'] = {'calories':calper,'carbs':carbper,'prot':proper,'fat':fatper, 'gcarb':shakcarb, 'gpro':shakpro, 'gfat':shakfat, 'gcal':shakal, 'tcarb':int(carb_grams/4), 'tpro':int(pro_grams/4), 'tfat':int(fat_grams/4), 'tcal':int(cons/4), 'name': 'SNACKS'}
            dict22 = rules(dict2, user_name)      
            dict22['content'] = content(request, user_name, flag, rec='Snacks') 
            return render(request, 'users/displayfood.html', dict22)
       
        dict_keys = ['food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats']
        foodlist = [dict(zip(dict_keys, a)) for a in foods]
        shakal = sum([x['calories'] for x in foodlist])
        shakcarb = sum([x['carbs'] for x in foodlist])
        shakpro = sum([x['proteins'] for x in foodlist])
        shakfat = sum([x['fats'] for x in foodlist])
        calper = int(shakal/(cons/4)*100)  
        carbper = int(shakcarb/(carb_grams/4)*100)
        proper = int(shakpro/(pro_grams/4)*100)
        fatper = int(shakfat/(fat_grams/4)*100)


        # foods.append(food)
        index = range(len(foodlist))                             
        # index = range(len(foods))
        dict2['food_dict'] = dict(zip(index, foodlist))
        dict2['cum'] = {'calories':calper,'carbs':carbper,'prot':proper,'fat':fatper, 'gcarb':shakcarb, 'gpro':shakpro, 'gfat':shakfat, 'gcal':shakal, 'tcarb':int(carb_grams/4), 'tpro':int(pro_grams/4), 'tfat':int(fat_grams/4), 'tcal':int(cons/4), 'name': 'SNACKS'}
        dict22 = rules(dict2, user_name)
        dict22['content'] = content(request, user_name, flag, rec='Snacks')
        return render(request, 'users/displayfood.html', dict22)
    else:
        request.session['success'] = success
        dict22 = rules(dict2, user_name)
        dict22['content'] = content(request, user_name, flag, rec='Snacks')
        # dict2['user_name'] = user_name  
        return render(request,'users/snacks.html', dict22)
    

def dinner(request):
    flag = request.POST.get('flag')
    if(flag == ''):
        flag = 0
    today = str(date.today())
    success = 'false'
    user_name = request.user.get_username()
    success = request.POST.get('success')
    food = request.session['food']
    cons = request.session['cons']
    
    carb_cal = 0.6 * cons  
    pro_cal = 0.2 * cons
    fat_cal = 0.2 * cons
    carb_grams = carb_cal/4
    pro_grams = pro_cal/4
    fat_grams = fat_cal/9


    foods = list(Breakfast.objects.filter(user_name = user_name, date=today).values_list('food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats'))
    if(len(foods) != 0):
        success = 'true'
        request.session['rec'] = 'Dinner'
    status = request.POST.get('status')
     
    rec = request.session['rec']
    dict2 = {'rec': rec}
    dict2['tab'] = 'Dinner'
    # dict2['user'] = user_name
    if(success == 'true'):
        request.session['success'] = 'false'
        
        # food_details = request.session['food_details'] 
        amount = request.POST.get('amount')
        cals = request.POST.get('cal')
        carbs = request.POST.get('carb')
        protein = request.POST.get('pro')
        fats = request.POST.get('fat')
        unit = request.POST.get('unit')

        if(status == 'delete'):
            ind = int(request.POST.get('ind'))   
            Dinner.objects.filter(food_id=ind, user_name=user_name, date=today).delete()  
            Dinner.objects.filter(food_id__gt=ind, user_name=user_name, date=today).update(food_id=F('food_id')-1)
            foods = list(Dinner.objects.filter(user_name = user_name, date=today).values_list('food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats'))
            # del foods[ind]
            # request.session['snacks_list'] = foods     
            if(len(foods) == 0):  
                dict22 = rules(dict2, user_name)
                dict22['content'] = content(request, user_name, flag, rec='Dinner') 
                return render(request,'users/dinner.html', dict22)
                 
            dict_keys = ['food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats']
            foodlist = [dict(zip(dict_keys, a)) for a in foods]
            shakal = sum([x['calories'] for x in foodlist])
            shakcarb = sum([x['carbs'] for x in foodlist])
            shakpro = sum([x['proteins'] for x in foodlist])
            shakfat = sum([x['fats'] for x in foodlist])
            calper = int(shakal/(cons/4)*100)  
            carbper = int(shakcarb/(carb_grams/4)*100)
            proper = int(shakpro/(pro_grams/4)*100)
            fatper = int(shakfat/(fat_grams/4)*100)
            # foods.append(food)
            index = range(len(foodlist))                             
            # index = range(len(foods))
            dict2['food_dict'] = dict(zip(index, foodlist))
            dict2['cum'] = {'calories':calper,'carbs':carbper,'prot':proper,'fat':fatper, 'gcarb':shakcarb, 'gpro':shakpro, 'gfat':shakfat, 'gcal':shakal, 'tcarb':int(carb_grams/4), 'tpro':int(pro_grams/4), 'tfat':int(fat_grams/4), 'tcal':int(cons/4), 'name': 'DINNER'}
            dict22 = rules(dict2, user_name)
            dict22['content'] = content(request, user_name, flag, rec='Dinner')
            return render(request, 'users/displayfood.html', dict22)     
         
        elif(status == 'add'):
            ind = len(foods)
            o_ref = Dinner(food_id = ind, user_name=user_name, food_names=food, amount = amount, unit = unit, calories = cals, carbs = carbs,proteins=protein,fats=fats) 
            o_ref.save()  
            foods = Dinner.objects.filter(user_name = user_name, date=today).values_list('food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats')
            dict_keys = ['food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats']
            foodlist = [dict(zip(dict_keys, a)) for a in foods]
            shakal = sum([x['calories'] for x in foodlist])
            shakcarb = sum([x['carbs'] for x in foodlist])
            shakpro = sum([x['proteins'] for x in foodlist])
            shakfat = sum([x['fats'] for x in foodlist])
            calper = int(shakal/(cons/4)*100)  
            carbper = int(shakcarb/(carb_grams/4)*100)
            proper = int(shakpro/(pro_grams/4)*100)
            fatper = int(shakfat/(fat_grams/4)*100)
            # foods.append(food)
            index = range(len(foodlist))                             
            # index = range(len(foods))
            dict2['food_dict'] = dict(zip(index, foodlist))
            dict2['cum'] = {'calories':calper,'carbs':carbper,'prot':proper,'fat':fatper, 'gcarb':shakcarb, 'gpro':shakpro, 'gfat':shakfat, 'gcal':shakal, 'tcarb':int(carb_grams/4), 'tpro':int(pro_grams/4), 'tfat':int(fat_grams/4), 'tcal':int(cons/4), 'name': 'DINNER'}
            dict22 = rules(dict2, user_name)      
            dict22['content'] = content(request, user_name, flag, rec='Dinner')
            return render(request, 'users/displayfood.html', dict22)
       
        dict_keys = ['food_names', 'amount', 'unit', 'calories', 'carbs', 'proteins', 'fats']
        foodlist = [dict(zip(dict_keys, a)) for a in foods]
        shakal = sum([x['calories'] for x in foodlist])
        shakcarb = sum([x['carbs'] for x in foodlist])
        shakpro = sum([x['proteins'] for x in foodlist])
        shakfat = sum([x['fats'] for x in foodlist])
        calper = int(shakal/(cons/4)*100)  
        carbper = int(shakcarb/(carb_grams/4)*100)
        proper = int(shakpro/(pro_grams/4)*100)
        fatper = int(shakfat/(fat_grams/4)*100)


        # foods.append(food)
        index = range(len(foodlist))                             
        # index = range(len(foods))
        dict2['food_dict'] = dict(zip(index, foodlist))
        dict2['cum'] = {'calories':calper,'carbs':carbper,'prot':proper,'fat':fatper, 'gcarb':shakcarb, 'gpro':shakpro, 'gfat':shakfat, 'gcal':shakal, 'tcarb':int(carb_grams/4), 'tpro':int(pro_grams/4), 'tfat':int(fat_grams/4), 'tcal':int(cons/4), 'name': 'DINNER'}
        dict22 = rules(dict2, user_name)
        dict22['content'] = content(request, user_name, flag, rec='Dinner')
        return render(request, 'users/displayfood.html', dict22)
    else:
        request.session['success'] = success
        dict22 = rules(dict2, user_name)
        dict22['content'] = content(request, user_name, flag, rec='Dinner') 
        return render(request,'users/dinner.html', dict22)

def total(request):
    user_name = request.user.get_username()
    today = str(date.today())
    cons = request.session['cons']
    
    carb_cal = 0.6 * cons  
    pro_cal = 0.2 * cons
    fat_cal = 0.2 * cons
    carb_grams = carb_cal/4
    pro_grams = pro_cal/4
    fat_grams = fat_cal/9

    all_foods = []
    for i in ['Breakfast', 'Lunch', 'Snacks', 'Dinner']:
        foods = list(eval(i).objects.filter(user_name = user_name, date=today).values_list('calories', 'carbs', 'proteins', 'fats'))
        dict_keys = ['calories', 'carbs', 'proteins', 'fats']
        foodlist = [dict(zip(dict_keys, a)) for a in foods]
        all_foods += foodlist
    
    
    shakal = sum([x['calories'] for x in all_foods])
    shakcarb = sum([x['carbs'] for x in all_foods])
    shakpro = sum([x['proteins'] for x in all_foods])
    shakfat = sum([x['fats'] for x in all_foods])

    calper = int(shakal/cons*100)  
    carbper = int(shakcarb/carb_grams*100)
    proper = int(shakpro/pro_grams*100)
    fatper = int(shakfat/fat_grams*100)
    
    return render(request, 'users/total.html', {'calories':calper,'carbs':carbper,'prot':proper,'fat':fatper, 'gcarb':shakcarb, 'gpro':shakpro, 'gfat':shakfat, 'gcal':shakal, 'tcarb':int(carb_grams), 'tpro':int(pro_grams), 'tfat':int(fat_grams), 'tcal':cons})



def preprocess(data):
    data.dropna(inplace = True)
    for row in range(len(data)): 
        data.iat[row, 1] = re.sub('[^a-zA-Z]+', ' ', data.iat[row, 1])
        data.iat[row, 0] = re.sub('[^a-zA-Z]+', ' ', data.iat[row, 0])
        data.iat[row, 1] = re.sub('[0-9]+[^0-9]', ' ', data.iat[row, 1])
        data.iat[row, 0] = re.sub('[0-9]+[^0-9]', ' ', data.iat[row, 0])

        if(data.iat[row, 1].lower() == data.iat[row, 0].lower()):
            data.iat[row, 1] = 'Generic'
    data['Food'] = data['Food'] + '-' + data['Category']
    return data[['Food', 'Amount', 'Calories', 'Carbs(in g)', 'Fat(in g)', 'Protein(in g)']]


def similar_words(text, data, count):    
    # fuzzywuzzy
    fuzzy_ratio = [fuzz.token_set_ratio(text.lower(), data.iat[i,0].lower()) for i in range(len(data))]
    data['ratio'] = fuzzy_ratio
    data.sort_values(by = ['ratio'], ascending = False, inplace = True)

    if ((sum(data['ratio'].head() > 80) < 3) and (count==0)):
        data.drop('ratio', axis = 1, inplace = True)   
        for num in ['1', '2']:
            count += 1
            url = "https://www.myfitnesspal.com/food/search?page=" + num + "&search=" + text
            new_data = scrape(url)
            data = data.append(preprocess(new_data), ignore_index = True)
        
        similar_words(text, data, count)
    data.drop_duplicates(subset = ['Food', 'Amount'], inplace = True)
    return data

# Function to scrape data and store in a csv file
def scrape(url):
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'nutri1.csv')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    soup.findChildren
    cats = soup.find_all(attrs = {'class':'jss11'})
    cals = soup.find_all(attrs = {'class':'jss16'})
    foods = soup.find_all(attrs = {'class':'jss10'})
    food = [x.text for x in foods]
    food_list = [[name.getText(), cal.getText()] for name, cal in zip(cats, cals)]
    df = pd.DataFrame(food_list, columns = ['Food', 'Calories'])
    category = df['Food'].str.findall('(.+),').str[0]
    amount = df['Food'].str.findall(',(.+)').str[0]
    cal_info = df['Calories'].str.findall(r'\d+')
    df['Food'] = food
    df['Category'] = category
    df['Amount'] = amount
    df['Calories'] = cal_info.str[0]
    df['Carbs(in g)'] = cal_info.str[1]
    df['Fat(in g)'] = cal_info.str[2]
    df['Protein(in g)'] = cal_info.str[3]
    nutri = df[['Food', 'Category', 'Amount', 'Calories', 'Carbs(in g)', 'Fat(in g)', 'Protein(in g)']]
    nutri.to_csv(file_path, index = False, header = False, mode = 'a')
    return nutri



    
    