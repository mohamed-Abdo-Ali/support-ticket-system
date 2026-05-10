# Installation

1. Install requirements:
pip install -r requirements.txt


2. Configure your MySQL database in `config/settings.py`.

3. Run migrations:
python manage.py migrate


4. Create an admin user:
python manage.py createsuperuser


5. Run the server:
python manage.py runserver


Open `http://127.0.0.1:8000/` in your browser.
