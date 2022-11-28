# Varsity-Sports-Auction
Built a Sports Gear Auction Website, developed using Django (using PostgresSQL) where fans can financially support their favourite NCAA athlete by purchasing their items

## Table of Contents 
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Run the application](#run-the-application)


## Features

### Login Page
<img src="https://user-images.githubusercontent.com/91244148/202900905-de402e18-77c8-453d-b0c4-195710c652c3.gif" width="750">

### Registration Page
<img src="https://user-images.githubusercontent.com/91244148/202896782-7cd1fc39-c39e-454d-978b-c9be38a84b12.gif" width="750">

### Bidding
<img src="https://user-images.githubusercontent.com/91244148/202897567-a56dc405-e09e-41fa-a384-81c3f581441a.gif" width="750">

### Close Bid
<img src="https://user-images.githubusercontent.com/91244148/202900534-a1d8c003-c9bc-4e7f-8b6e-b3dd1f3abc2a.gif" width="750">

### Razorpay
<img src="https://user-images.githubusercontent.com/91244148/202902118-acfece42-cce3-45ff-a22d-6fdced486a3a.png" width="750">

### Comment
<img src="https://user-images.githubusercontent.com/91244148/202897398-75aca6e6-02a0-4147-bef5-5e8e3463479f.gif" width="750">

### Create Auction
<img src="https://user-images.githubusercontent.com/91244148/202897975-7b8ed53f-7d4a-43b1-9ed8-e6f21be0bc59.gif" width="750">

### Watch List
<img src="https://user-images.githubusercontent.com/91244148/202898558-0b91bc2f-f17e-4d79-82bd-14619794ec7e.gif" width="750">

### Category Page
<img src="https://user-images.githubusercontent.com/91244148/202898229-5ae86920-c0bd-40ed-91c7-89580139d0fe.gif" width="750">

### Winner Page
<img src="https://user-images.githubusercontent.com/91244148/202898342-20184fca-79b4-4e0c-aa21-f3c7fdbd3f3c.gif" width="750">

### Search Products
<img src="https://user-images.githubusercontent.com/91244148/202897644-cae44110-ffc3-4c95-9e99-e9fe95966ef4.gif" width="750">

### Dashboard
<img src="https://user-images.githubusercontent.com/91244148/202898869-5bbc4d19-301f-43e8-85e0-ba010075e548.gif" width="750">

### Logout
<img src="https://user-images.githubusercontent.com/91244148/202897211-9a84f9c3-4032-43f0-96ce-e2b3ea65dd11.gif" width="750">


## Prerequisites

Install the following prerequisites:

1. [Python 3.8.13 or higher](https://www.python.org/downloads/)
2. [PostgreSQL](https://www.postgresql.org/download/)
3. [Razorpay](https://razorpay.com/docs/#home-payments)
4. [Visual Studio Code](https://code.visualstudio.com/download)


## Installation

### 1. Create a virtual environment

From the **root** directory run:

```bash
python -m venv venv
```

### 2. Activate the virtual environment

From the **root** directory run:

On macOS or Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\scripts\activate
```

### 3. Install required dependencies

From the **root** directory run:

```bash
pip install -r requirements.txt
```

### 4. Set up a PostgreSQL database

With **PostgreSQL** up and running, in a new Terminal window run:

```bash
dropdb --if-exists auction
```

Start **psql**, which is a terminal-based front-end to PostgreSQL, by running the command:

```bash
psql postgres
```

Create a new PostgreSQL database:

```sql
CREATE DATABASE auction;
```

Create a new database admin user:

```sql
CREATE USER yourusername WITH SUPERUSER PASSWORD 'yourpassword';
```

Install pg_trgm extension in postgres:

```sql
\c auction
CREATE EXTENSION pg_trgm;
```

To quit **psql**, run:

```bash
\q
```

### 5. Set up environment variables

From the **root** directory run:

```bash
touch .env
```

The **touch** command will create the **.env** file in the **root** directory. This command works on Mac and Linux but not on Windows. If you are a Windows user, instead of using the command line, you can create the **.env** file manually by navigating in Visual Studio Code to the Explorer, and selecting the option **New File**.


Next, declare environment variables in the **.env** file. Make sure you don't use quotation marks around the strings.

```bash
SECRET_KEY = yourSecretKey
USER_NAME = yourUserame
DATABASE_PASSWORD = yourPassword
KEY_ID = yourRazorpayKeyId
KEY_SECRET = yourRazorpayKeySecret
```

### 6. Run migrations

From the **root** directory run:

```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

### 7. Create an admin user to access the Django Admin interface

From the **root** directory run:

```bash
python manage.py createsuperuser
```

When prompted, enter a username, email, and password.


## Run the application

From the **root** directory run:

```bash
python manage.py runserver
```

### View the application

Go to http://127.0.0.1:8000/ to view the application.