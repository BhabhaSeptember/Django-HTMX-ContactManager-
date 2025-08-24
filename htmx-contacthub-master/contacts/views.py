from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_http_methods

from contacts.forms import ContactForm

# Create your views here.

# The decorator below only allows access to the view below to
# users who are logged in
@login_required
# The index view takes an HTTP request
def index(request):
    contacts = request.user.contacts.all().order_by('-created_at') 
    context = { 
        'contacts' : contacts,
        'form': ContactForm()
    }
    return render(request, 'contacts.html', context)

@login_required
def search_contacts(request):
    import time
    time.sleep(2)
    query = request.GET.get('search', '')
    
    # use the query to filter contacts by name or email
    contacts = request.user.contacts.filter(
        Q(name__icontains=query) | Q(email__icontains=query)
    )
    return render(request, 'partials/contact-list.html', {'contacts': contacts})
    
    
# Decorator allows only POST requests to this view
@login_required
@require_http_methods(['POST'])
def create_contact(request):
# Use the ContactForm and pass the POST data from htmx into that form
    form = ContactForm(request.POST, request.FILES, initial={'user' : request.user})
# After populating form, check if data is valid
# Create contact model instance (but dont commit to db yet)
# Set request body user to the foreign key of user in model
    if form.is_valid(): 
        contact = form.save(commit=False)
        contact.user = request.user 
        contact.save()
# Context with newly created contact and add it to the render function
# Return a partial containing new row for user to add to table
        context = {'contact' : contact}
        response = render(request, 'partials/contact-row.html', context)
        response['HX-Trigger'] = 'success'
        return response
    else:
        response = render(request, 'partials/add-contact-modal.html', {'form' : form})
        response['HX-Retarget'] = '#contact_modal'
        response['HX-Reswap'] = 'outerHTML'
        response['HX-Trigger-After-Settle'] = 'fail'
        return response
# Take form data from request and render the modal with the populated data
# Replace/swap entire data in modal with data from server
# Trigger fail event after response content has settled in the DOM (i.e. from populated)
        
