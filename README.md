# Proctoring Web Application

![unnamed](https://github.com/ayushrawat9/Proctoring-Software/assets/75422096/921bdd90-55b8-45ba-9b0f-9d7dff98749e)


## Table of Contents
- [Introduction](#introduction)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction
This is a Django-based proctoring web application designed to maintain the integrity of online exams. It provides a secure environment for students and teachers to conduct and monitor online assessments.

## Key Features
### Registration
- Students register on a portal, providing personal details stored in the database for verification.
- Verification is done by designated authorities.

### User Login
- After registration, students log in.
- A webcam captures the student's image, and face verification is required for access.

### Exam Module
- Teachers can create tests from templates, assigning test IDs and passwords.
- Students use these credentials to access and take the test.

### Face Detection
- Webcam continuously captures the student's image during the exam.
- If the face is not detected, this is logged in the database.
- Utilizes the deepface library for login and the mediapipe library for proctoring.

### Gaze Detection
- Continuous image capture checks for cheating behaviors such as looking away.
- Logs are sent to the live stream and the database using websockets.

### Multiple Face Detection
- If more than one person is detected in the frame, it is logged as malpractice.
- Logs are sent to the live stream and the database via websockets.

### Browser Tab Switch Detection
- Tab switching during the exam is considered malpractice and is logged.
- Logs are sent to the live stream and the database using websockets.

### Exam Logs
- Detailed logs of each student's exam are recorded.
- Instructors can review these logs to assess malpractice.
- Each exam log includes a flag and an image of the student at that instant.
- Reliability is ensured through DeepFace and MediaPipe Python libraries.

### Student-Teacher Management
- Features a student dashboard.
- Allows student test login before exams.
- Manages student and teacher verifying authorities.
- Provides the functionality for students to take tests.
- Saves proctoring logs for teachers to review post-exam.

### Examination Module
- Teachers can create both objective and subjective tests.
- Ensures authenticity verification of students.
- Enables students to take tests after verification.

### Django Apps
Two apps were created in the Django framework:
1. Student app - Contains routing for student activities.
2. Teachers app - Contains routing for teacher activities.

## Technologies Used
- Django
- Python
- deepface library
- mediapipe library
- Websockets

## Installation
1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Configure your database settings in `settings.py`.
4. Migrate the database using `python manage.py migrate`.
5. Run the application using `python manage.py runserver`.

## Usage
1. Register as a student or teacher.
2. Log in to your account.
3. Create or take exams.
4. Enjoy secure proctoring during exams.

## Contributing
We welcome contributions from the open-source community. If you'd like to contribute, please follow our [contributing guidelines](CONTRIBUTING.md).

## License
This project is licensed under the [MIT License](LICENSE).

