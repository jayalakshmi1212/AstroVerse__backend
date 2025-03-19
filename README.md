# Astroverse - E-learning Platform for Astronomy

Astroverse is a modern e-learning platform designed for astronomy enthusiasts. It offers interactive courses, real-time communication, and secure payments for premium content. Built with **React** for the frontend and **Django** for the backend, Astroverse ensures a seamless learning experience with JWT-based authentication, real-time chat, video calling, and cloud-based media storage.

---

## Features
- **User Authentication** - Secure signup and login with JWT token verification.
- **Interactive Courses** - Learn astronomy through structured lessons and video content.
- **Real-Time Chat & Video Call** - Engage with instructors and peers using WebSockets.
- **Cloud Storage** - Images and videos are stored using **Cloudinary**.
- **Secure Payments** - Pay for premium courses via **Razorpay**.
- **Admin Dashboard** - Manage users, content, and payments.

---

## Tech Stack

### **Frontend (React.js)**
- React.js (with Redux for state management)
- React Router for navigation
- WebSockets for real-time communication
- Axios for API requests

### **Backend (Django & Django REST Framework)**
- Django REST Framework (DRF) for APIs
- JWT Authentication for secure access
- Django Channels & WebSockets for real-time communication
- PostgreSQL for database management

### **Other Technologies**
- Cloudinary for media storage (images/videos)
- Razorpay for payment integration
- WebSockets for real-time chat and video calls

---

## Installation

### **Backend (Django)**
1. Clone the repository and navigate to the backend:
   ```sh
   git clone https://github.com/your-username/astroverse.git
   cd astroverse/backend
   ```
2. Create a virtual environment and install dependencies:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```
3. Run database migrations:
   ```sh
   python manage.py migrate
   ```
4. Create a `.env` file and add your **Cloudinary** and **Razorpay** credentials.
5. Start the Django server:
   ```sh
   python manage.py runserver
   ```

### **Frontend (React.js)**
1. Navigate to the frontend folder:
   ```sh
   cd ../frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the React development server:
   ```sh
   npm start
   ```

---

## Usage
1. Visit `http://localhost:3000` in your browser.
2. Sign up or log in.
3. Explore courses and enroll in astronomy lessons.
4. Use the real-time chat to interact with peers and instructors.
5. Join video calls for live discussions.
6. Purchase premium content securely via Razorpay.

---

## API Endpoints (Example)
| Method | Endpoint                | Description               |
|--------|------------------------|---------------------------|
| POST   | /api/auth/signup/       | User registration         |
| POST   | /api/auth/login/        | User login (JWT)          |
| GET    | /api/courses/           | Fetch all courses         |
| POST   | /api/chat/send/         | Send chat message         |
| POST   | /api/payment/checkout/  | Initiate payment via Razorpay |

---

## Contributors
- [Your Name](https://github.com/jayalakshmi1212)

---

## License
This project is licensed under the **MIT License**.

