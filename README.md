# 🚕 Kokrajhar Cab

A local cab booking web application built with Django.
Serving Kokrajhar and surrounding areas.

## Features

- Passenger registration and login
- Request a cab with pickup and drop location
- Driver dashboard to see and accept rides
- Real-time ride status (pending/confirmed/completed)
- Role-based access (passenger/driver)
- Clean Bootstrap UI

## Tech Stack

- Python 3.11
- Django 5.x
- Bootstrap 5
- SQLite

## How to Run Locally

1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install dependencies: `pip install django`
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Run server: `python manage.py runserver`
8. Visit: <http://127.0.0.1:8000>

## Project Status

Work in progress — Week 2 of 30-day build.

## Future Plans

- Google Maps integration
- WhatsApp notifications
- Payment gateway
- Mobile app
