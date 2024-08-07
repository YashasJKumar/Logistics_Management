# Logistics Management System

This is a logistics management system built with Flask, SQLAlchemy, and Flask-Login. The application allows users to register, log in, and manage bookings. An admin interface is also provided for dispatch management.

![image](https://miro.medium.com/v2/resize:fit:1400/1*wuG1_riJHs3hKFVHnMGB2w.gif)


## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Usage](#usage)
  - [User Registration](#user-registration)
  - [User Login](#user-login)
  - [Booking](#booking)
  - [Admin Login](#admin-login)
- [Email Notifications](#email-notifications)
- [Admin Interface](#admin-interface)
- [Contributing](#contributing)

## Features

- User registration and login with email confirmation
- Password hashing for security
- Booking management
- Admin interface for managing dispatches
- Email notifications for registration and booking confirmations

## Requirements

Ensure you have Python installed. The required packages are specified in `requirements.txt`.

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/YashasJKumar/Logistics-Management.git
    cd Logistics-Management
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables for email credentials:**
    ```sh
    export EMAIL='your-email@gmail.com'
    export PASSWORD='your-email-password'
    ```

## Database Setup

1. **Initialize the database:**
    ```sh
    flask shell
    from your_application import db
    db.create_all()
    exit()
    ```

## Running the Application

1. **Run the Flask application:**
    ```sh
    flask run
    ```

2. **Access the application in your browser:**
    ```sh
    http://127.0.0.1:5000
    ```

## Usage

### User Registration

Users can register by providing their email, password, name, city, and contact number.

### User Login

Users can log in using their email and password.

### Booking

After logging in, users can make a booking by providing the necessary details such as source, destination, product, and delivery deadline.

### Admin Login

Admin can log in using specific credentials to access the dispatch management interface.

## Email Notifications

Email notifications are sent to users for:
- Successful registration
- Booking confirmation

## Admin Interface

The admin can manage dispatches and view booking details. The admin interface includes:
- Viewing all bookings
- Dispatch management

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

