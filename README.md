# TRACK-YOUR-CLASS

This is a TrackYourClass implemented using Django. The system includes functionality for student registration, teacher management, attendance tracking, and more.

## Project Structure

The project is organized into several Django applications:

- **core**: Contains the main settings and configurations for the project.

- **accounts**: Manages user authentication and includes views for student and teacher registration.

- **admin_panel**: Provides views and functionalities for administrators, including user management, approval of student registrations, and uploading notices.

- **teacher_panel**: Manages teacher-specific functionalities, such as marking attendance, assigning marks, and viewing student lists.

- **student_panel**: Handles student-specific functionalities, including viewing marks, tracking attendance, and viewing announcements.

- **models**: Defines the database models for the project.

- **templates**: Contains HTML templates for rendering views.

## Features

1. **User Authentication**
   - Different user roles: Admin, Teacher, and Student.
   - User login and registration.

2. **Admin Panel**
   - Approve or reject student registrations.
   - Upload notices.
   - Check and manage teacher and student lists.
   - View and manage attendance.

3. **Teacher Panel**
   - Mark attendance for students.
   - Assign marks to students.
   - View and manage student lists.
   - Make announcements.

4. **Student Panel**
   - View marks for different subjects.
   - Track attendance.
   - View announcements.

## How to Run

 Clone the repository:

   ```bash
   git clone <repository-url>
  ```
 Install dependencies:
 
  ```bash
  pip install -r requirements.txt
  ```
Apply database migrations:

```bash
python manage.py migrate
```

Run the development server:

```bash
python manage.py runserver
```

The application will be accessible at http://127.0.0.1:8000/

## Contributing

Contributions are welcome! 
