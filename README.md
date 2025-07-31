#  Booked – Backend 

This is the backend of **Booked**, an online bookstore application inspired by the original Amazon.com. The backend is built with Django and Django REST Framework and provides secure APIs for authentication, book management, cart and order handling, and role-based access control.

---

##  Features

### Admin

* Register/login with JWT authentication
* Add, update, delete books
* View all books
* Approve/reject book purchase orders
* Approve/reject lending requests

###  User

* Register/login with JWT
* View all books
* Search and filter books
* Add to purchase/lending cart
* Checkout and view history
* Return borrowed books
* Role-based permission enforcement

---

##  Tech Stack

* **Framework:** Django
* **API:** Django REST Framework (DRF)
* **Database:** PostgreSQL
* **Auth:** JWT via `SimpleJWT`
* **Custom User Model** with email as the primary login field

---



##  Local Setup

### Requirements

* Python 3.10+
* PostgreSQL

```bash
# Clone the repository
git clone https://github.com/corenetabitha/booked-backend.git
cd booked-backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

---

## 🔐 API Authentication

* JWT tokens are used for authentication.
* After login, the frontend stores the access token and sends it in headers as:

  
---


##  Contributors

* [@vickitah](https://github.com/vickitah)
* [@Alvine9876](https://github.com/Alvine9876)
* [@corenetabitha](https://github.com/corenetabitha)
* [@hussein-ft](https://github.com/hussein-ft)
* [@christine-muigai](https://github.com/christine-muigai)

---

## License

This backend was developed for academic and demonstration purposes only. Not licensed for commercial use.
