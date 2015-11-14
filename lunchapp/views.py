from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import logging
logger = logging.getLogger(__name__)

import json

from lunchapp.models import Month, Person
from lunchapp.utils import email_utils

months = ('january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december')
    
valid_years = tuple(range(2014, 2020))

def home(request):
    """Render the home page"""
    template = loader.get_template('lunchapp/home.html')
    context = RequestContext(request, {
        'valid_years': valid_years
    })
    return HttpResponse(template.render(context))
    
def update_lists(request, year, month):
    """Add or remove a person to the program for a given month and year  
    Update the lists of those signed_up and those not signed up dynamically
    Recalculate the best grouping of the new participant list
    """
    if month in months:
        month = months.index(month) + 1 # month is the index of the list of months
    else:
        month = int(month)  # came in as unicode
    month = Month.objects.get(month=month, year=year)
    try:
        email = request.POST['chosen_person']
        request_type = request.POST['request_type']
        person = Person.objects.get(email=email)
        if request_type == 'add':
            month.add_person(person)
            message = 'successfully signed up %s for %s; email confirmation sent' % (person, month)
        else:
            month.remove_person(person)  # remove person to the signed_up list
            message = 'successfully unsubscribed %s for %s; email confirmation sent' % (person, month)
    except:
        person = Person()
        person.name=''
        person.email=''
        message = 'Cannot select a person from an empty listl' 
    #email_utils.send_removal_success_email(person, month)
    
    groups = month.make_grouping()
    not_signed_up = list(set(Person.objects.all()).difference(month.signed_up.all()))

    if request.is_ajax():
        logger.debug('this is an ajax request')
    else:
        logger.debug('this is a regular POST request; no ajax')

    not_su_context = RequestContext(request, {
        'not_signed_up': not_signed_up
    })
    su_context = RequestContext(request, {
        'signed_up': month.signed_up.all()
    })
    group_context = RequestContext(request, {
        'groups': groups
    })
    
    return HttpResponse(
        json.dumps({
        'name': person.name, 
        'email': person.email, 
        'signed_up_selector': loader.render_to_string('lunchapp/signed_up_selector.html', context_instance=su_context),
        'not_signed_up_selector': loader.render_to_string('lunchapp/not_signed_up_selector.html', context_instance=not_su_context),
        'signed_up_list': loader.render_to_string('lunchapp/signed_up_list.html', context_instance=su_context),
        'groups': loader.render_to_string('lunchapp/groups.html', context_instance=group_context),
        'message': message
        }),
        content_type="application/json")

def sign_up(request, year, month):
    """Render the sign-up view
    """
    if month in months:
        month = months.index(month) + 1 # month is the index of the list of months
    else:
        month = int(month)  # came in as unicode
    month_object = Month.objects.get(year=year, month=month)
    template = loader.get_template('lunchapp/month.html')
    signed_up = month_object.signed_up.all()
    not_signed_up = list(set(Person.objects.all()).difference(signed_up))
    groups = month_object.make_grouping()

    context = RequestContext(request, {
        'month': months[month-1],
        'year': year,
        'signed_up': signed_up,
        'not_signed_up': not_signed_up,
        'groups': groups
    })
    return HttpResponse(template.render(context))
    
    
