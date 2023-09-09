# Django Campaign Management Project

The Django Campaign Management Project is a versatile web application designed to facilitate effective email campaign management. It offers a comprehensive set of features for creating, managing, and sending email campaigns to a targeted subscriber base. Whether you're a marketer, content creator, or business owner, this project can streamline your email marketing efforts.

## Features

### 1. User-Friendly Admin Panel

- **Admin Login**: Secure login functionality ensures that only authorized personnel can access and manage campaigns.
  

  ![admin login](https://github.com/Blankita21/Email-Campaign-Manager/assets/59385327/94d59d9e-a61e-4842-8fd3-03aa352d81b5)


### 2. Subscriber Management

- **Add Subscribers**: Easily add new subscribers to your database via a user-friendly form. Collect subscriber emails and their first names for personalized campaigns.
- **Unsubscribe**: Subscribers have the option to unsubscribe from email campaigns, ensuring compliance with email marketing regulations.
  

  ![homepage](https://github.com/Blankita21/Email-Campaign-Manager/assets/59385327/7fc83055-18c1-443f-9ed6-8334aec9a770)



![add subscriber](https://github.com/Blankita21/Email-Campaign-Manager/assets/59385327/272b967a-9aeb-4fdb-a5fb-93b75ed07588)


### 3. Campaign Creation and Sending

- **Create Campaigns**: Craft compelling email campaigns using the provided form. Specify the subject, preview text, article URL, HTML content, plain text content, and published date.
  

![send campaign](https://github.com/Blankita21/Email-Campaign-Manager/assets/59385327/2f7bd797-9ad1-4de3-b2a0-6a0031e79f9a)


### 4. Email Sending

- **SMTP Integration**: Seamlessly integrate with SMTP email servers (e.g., Gmail) for sending email campaigns.
- **Email Sending Queue**: Utilize Celery for asynchronous email sending, ensuring efficient processing of large email lists.

## Getting Started

### Requirements

- Python 3.9+
- Django 4.2+
- Redis (for Celery task queue)
- SMTP email server (e.g., Gmail for sending emails)
- Celery for asynchronous task processing

### Installation

1. Clone the repository to your local machine.
2. Create a virtual environment and install project dependencies.
3. Configure your Django settings for email, database, and Celery (as specified in the README).
4. Run database migrations.
5. Start the Django development server and access the project in your web browser.

## Usage

The project provides a seamless interface for adding subscribers, creating campaigns, and managing your email marketing efforts. The admin panel offers easy navigation and robust tools for campaign creation and subscriber management.

## Folder Structure

- `campaigns/`: Django app for campaign management.
- `Campaign_manager/`: Project settings and configuration.
- `static/`: Static files (CSS, JavaScript, images).
- `templates/`: HTML templates used in the project.


