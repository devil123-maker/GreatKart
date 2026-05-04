# 🛒 Django E-Commerce Web App


A full-featured **E-Commerce Web Application** built with Django, supporting product browsing, cart management, secure checkout, and Stripe payment integration.

---

## 🌟 Features

✅ User Authentication (Login/Register/Logout)  
✅ Product Listing & Category Filtering  
✅ Search Functionality  
✅ Shopping Cart System  
✅ Secure Checkout Flow  
✅ Stripe Payment Integration (with Webhooks)  
✅ Order Management  
✅ Admin Panel for Product Control  

---

## 🧠 Tech Stack

| Category       | Technology |
|---------------|------------|
| Backend       | Django |
| Language      | Python |
| Database      | SQLite (Dev) |
| Payments      | Stripe |
| Frontend      | HTML, CSS, Bootstrap |
| Environment   | python-dotenv |

---

## 📸 Screenshots

> *(Add your screenshots here — this boosts your portfolio a LOT)*

### 🏠 Homepage
/screenshots/home.png

### 🛍️ Product Page
/screenshots/product.png

### 🛒 Cart
/screenshots/cart.png

### 💳 Checkout
/screenshots/checkout.png

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

git clone https://github.com/your-username/ecommerce-django.git
cd ecommerce-django

### 2️⃣ Create Virtual Environment

python -m venv myenv
source myenv/bin/activate  # Mac/Linux
myenv\Scripts\activate     # Windows

### 3️⃣ Install Dependencies

pip install -r requirements.txt

or

pip install django python-dotenv stripe

### 4️⃣ Setup Environment Variables

Create `.env` file:

STRIPE_SECRET_KEY=your_secret_key
STRIPE_PUBLIC_KEY=your_public_key
STRIPE_WEBHOOK_SECRET=your_webhook_secret

### 5️⃣ Run Migrations

python manage.py migrate

### 6️⃣ Create Superuser

python manage.py createsuperuser

### 7️⃣ Run Server

python manage.py runserver

Open: http://127.0.0.1:8000/

---

## 💳 Stripe Payment Workflow

1. User adds items to cart  
2. Proceeds to checkout  
3. Stripe Checkout session is created  
4. Payment stored as `pending`  
5. Stripe webhook triggers on success  
6. Payment marked **completed**  


---

## 📁 Project Structure

e-commerce/
│
├── Ecommerce/
├── accounts/
├── carts/
├── category/
├── greatkart/
├── orders/
├── store/
│
├── templates/
├── static/
├── media/
│
├── manage.py
├── db.sqlite3
├── .env
└── myenv/

---

## 🔐 Security Notes

- Never expose `.env` file  
- Keep Stripe keys private  
- Set `DEBUG = False` in production  
- Configure `ALLOWED_HOSTS` properly  

---

## 🚀 Future Improvements
- After Payment Cart Cleared
- Product Reviews & Ratings  
- Order Tracking System  
- Email Notifications  
- Docker Deployment  
- PostgreSQL Integration  
- Mobile Responsive Enhancements  

---

## 🤝 Contributing

# Fork repo
# Create branch
git checkout -b feature-name

# Commit changes
git commit -m "Added feature"

# Push
git push origin feature-name

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Dev Chauhan

GitHub: https://github.com/your-username  
LinkedIn: (add your link)

---

## ⭐ Show Your Support

If you like this project:

Give it a star on GitHub  
Share it  
Use it in your portfolio
