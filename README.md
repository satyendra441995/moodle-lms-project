# Multi-Teacher Learning Management System (LMS)

A fully functional, web-based Learning Management System inspired by platforms like Moodle. This project is built using Python and Django to support multiple teachers and students with secure, role-based access.

## Features

**🔑 Robust Authentication & Roles**
- Centralized user authentication system.
- Three distinct user roles: `Admin`, `Teacher`, and `Student`, ensuring strict data boundaries.

**👨‍🏫 Teacher Workflow**
- Dedicated teacher dashboard.
- Create and manage independent subjects/courses.
- Publish assignments with titles, descriptions, specific deadlines, and optional material attachments.
- View enrolled students and download their assignment submissions.
- Assign grades (out of 100) and provide rich feedback.

**🎓 Student Workflow**
- Dedicated student dashboard.
- Browse a global course catalog and intuitively enroll in courses.
- View specific assignments linked to enrolled courses.
- Upload assignment files.
- Stay updated on assignment statuses and review grades/feedback seamlessly.

**✨ Premium UI/UX Design**
- Built without CSS frameworks for maximum control.
- Implements "Glassmorphism" UI trends, smooth gradients, and micro-animations.
- Fully responsive on desktop, tablet, and mobile.
- Utilizes the Django Messages framework for toast/flash notifications.

## Technology Stack
- **Backend Framework**: Python 3 / Django 6.0
- **Database**: SQLite (Configurable to PostgreSQL for Production)
- **Frontend**: Django Templates, Vanilla HTML5, and CSS3
- **File Management**: Pillow (Image parsing / Upload Support)
- **Server Deployment**: Waitress/Gunicorn & WhiteNoise

---

## Local Development Setup

To run this project on your local machine, follow these steps:

1. **Clone the repository**
   ```bash
   git clone https://github.com/satyendra441995/moodle-lms-project.git
   cd moodle-lms-project
   ```

2. **Set up Virtual Environment**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```
   Navigate to `http://127.0.0.1:8000` in your web browser.

---

## Deployment (Render.com)

This application is configured for seamless deployment on **Render**.

1. Go to Render.com and Create a **New Web Service**.
2. Connect this repository.
3. Configure the settings:
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn lms_project.wsgi:application`
4. Click **Deploy**.

*(Note: On Render's free tier, local disk storage is ephemeral. For a permanent production environment, it is highly recommended to provision a PostgreSQL database securely.)*
