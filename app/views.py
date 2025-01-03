from django.conf import settings
from django.http import FileResponse,Http404
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from .models import ContactMessage,Paste
import os
# Create your views here.
def homepage(request):
    return render(request,"index.html")

def contactview(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Validate the data (optional but recommended)
        if not name or not email or not message:
            messages.error(request, 'All fields are required.')
        else:
            # Save the data to the database
            contact_message = ContactMessage(name=name, email=email, message=message)
            contact_message.save()
            messages.success(request, 'Your message has been sent successfully.')
            return redirect('contact')  # Redirect to a success page or the contact page

    return render(request, 'index.html')

def print(request):
    messages = ContactMessage.objects.all()
    return render(request, 'print.html', {'messages': messages})


def register_view(request):
    if request.method == 'POST':
        username= request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password1')
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                return redirect('homepage') 
        else:
            messages.error(request, 'Passwords do not match')
    
    return render(request, 'register.html')


def view_pdf(request, file_name):
    file_path = os.path.join(settings.STATIC_ROOT, 'assets/pdf', file_name)
    if not os.path.exists(file_path):
        raise Http404(f"File {file_name} not found")
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')


def user_details(request):
    users = User.objects.all()  # Fetch all users from the database
    return render(request, 'students.html', {'users': users})

SPECIFIC_PASTE_ID = 1

def create_paste(request):
    # Retrieve the paste by its ID or create it if it does not exist
    paste, created = Paste.objects.get_or_create(id=SPECIFIC_PASTE_ID)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            # Update the paste
            paste.title = title
            paste.content = content
            paste.save()

            return redirect('show_paste', paste_id=paste.id)  # Redirect to the paste details page

    # Render the template with the paste details
    return render(request, 'pastedetails.html', {'paste': paste})
def show_paste(request, paste_id):
    # Retrieve the paste by its ID or return a 404 error if not found
    paste = get_object_or_404(Paste, id=1)

    # Render the template and pass the paste object to it
    return render(request, 'paste.html', {'paste': paste})