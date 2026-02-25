from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from datetime import datetime
import re

from .models import (
    Contact,
    Gallery,
    Price,
    ServiceCategory,
    Product,
    Hairstyle,
    Appointment,
    AboutUsCategory,
    Makeup,
    Artist
)

# =========================
# Home Page
# =========================
from .models import Artist, Product  # make sure Artist is imported

def home(request):
    products = Product.objects.all()
    artists = Artist.objects.all()  # get all artists
    return render(request, 'home.html', {
        'products': products,
        'artists': artists
    })


# =========================
# About / Services
# =========================
def about(request):
    categories = AboutUsCategory.objects.all()
    return render(request, 'about.html', {'categories': categories})


def AboutUsCategory_detail(request, id):
    category = get_object_or_404(AboutUsCategory, id=id)
    template_name = f"aboutus/{category.name.lower()}.html"
    return render(request, template_name, {'category': category})


def services(request):
    return render(request, 'services.html')


# =========================
# Gallery
# =========================
def gallery(request):
    images = Gallery.objects.filter(is_active=True)
    return render(request, 'gallery.html', {'images': images})


def gallery_search(request):
    query = request.GET.get('q', '').strip()
    if query:
        words = query.split()
        q_objects = Q()
        for word in words:
            regex = rf'\b{re.escape(word)}\b'
            q_objects |= Q(title__iregex=regex)
        images = Gallery.objects.filter(q_objects).distinct()
    else:
        images = Gallery.objects.all()

    return render(request, 'gallery.html', {'images': images, 'query': query})


# =========================
# Hairstyles
# =========================
def hairstyle(request):
    hairstyles = Hairstyle.objects.filter(is_active=True)
    return render(request, 'services/hairstyling.html', {
        'hairstyles': hairstyles
    })

def makeup(request):
    makeups = Makeup.objects.filter(is_active=True)
    return render(request, 'services/makeups.html', {'makeups': makeups})


# =========================
# Contact Page
# =========================
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Contact.objects.create(
            name=name,
            email=email,
            message=message,
            date=datetime.today()
        )

        send_mail(
            subject=f"New Contact Message from {name}",
            message=f"Name: {name}\nEmail: {email}\nMessage:\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['prabeshkhatakho88@gmail.com'],
            fail_silently=False,
        )

        messages.success(request, "Your message has been sent!")
        return redirect('contact')

    return render(request, 'contact.html')


# =========================
# Authentication
# =========================
def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

        messages.error(request, "Invalid username or password!")

    return render(request, 'login.html')


def registerUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirmpassword = request.POST.get('password2')

        if password != confirmpassword:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        original_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, f"Account created successfully! Your username is {username}")
        return redirect('home')

    return render(request, 'register.html')


def logoutUser(request):
    logout(request)
    return redirect('home')


# =========================
# Products
# =========================
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


# =========================
# Book Appointment
# =========================
def book_appointment(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        service = request.POST['service']
        date = request.POST['date']
        time = request.POST['time']
        notes = request.POST.get('notes', '')

        if Appointment.objects.filter(date=date, time=time).exists():
            messages.error(request, "An appointment already exists at this date and time.")
            return redirect('book_appointment')

        Appointment.objects.create(
            name=name, email=email, phone=phone, service=service,
            date=date, time=time, notes=notes
        )

        # Email to admin
        send_mail(
            subject=f"New Appointment Booked: {name}",
            message=f"Name: {name}\nEmail: {email}\nPhone: {phone}\nService: {service}\nDate: {date}\nTime: {time}\nNotes: {notes}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["yourgmail@gmail.com"],
            fail_silently=False
        )

        # Email confirmation to customer
        send_mail(
            subject="Your Appointment is Confirmed",
            message=f"Hi {name},\n\nYour appointment for {service} is confirmed on {date} at {time}.\n\nThank you!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )

        messages.success(request, "Your appointment has been booked successfully!")
        return redirect('book_appointment')

    return render(request, 'book_appointment.html')


def contact_artist(request, artist_id):
    from .models import Artist  # make sure Artist is imported at top

    artist = get_object_or_404(Artist, id=artist_id)

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Optional: Save message in Contact model
        Contact.objects.create(
            name=name,
            email=email,
            message=message,
            date=datetime.today()
        )

        # Send email to the specific artist
        send_mail(
            subject=f"New Message for {artist.name}",
            message=f"Name: {name}\nEmail: {email}\nMessage:\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[artist.email],
            fail_silently=False,
        )

        messages.success(request, f"Your message has been sent to {artist.name}!")
        return redirect('home')  # or redirect to a success page

    return render(request, 'contact_artist.html', {'artist': artist})