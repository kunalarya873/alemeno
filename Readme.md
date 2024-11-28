**Credit Approval System**
==========================

This is a backend system built with Django and Django REST Framework for a Credit Approval application. The system allows customers to register, check loan eligibility, and apply for loans. It also integrates PostgreSQL as the database and supports background tasks for data ingestion.

**Features**
------------

*   **Customer Registration**: Allows adding a new customer and calculates an approved credit limit based on their monthly income.
*   **Loan Eligibility Check**: Based on the customer's credit history and current debt.
*   **Loan Application**: Allows customers to apply for loans, calculating the monthly installments based on the loan amount and tenure.
*   **Database Integration**: Uses PostgreSQL as the primary database for customer and loan data.
*   **Dockerized Setup**: The entire application and database are dockerized, making it easy to deploy and manage.

* * *

**Table of Contents**
---------------------

*   [Installation](#installation)
*   [Usage](#usage)
    *   [Running the Project](#running-the-project)
    *   [API Endpoints](#api-endpoints)
*   [Docker Setup](#docker-setup)
*   [Testing](#testing)
*   [License](#license)

* * *

**Installation**
----------------

### **1\. Clone the Repository**

Clone the project from GitHub:

`git clone https://github.com/your-username/credit-approval-system.git`

`cd credit-approval-system` 

### **2\. Set Up Virtual Environment**

Create and activate a virtual environment:

``python3 -m venv venv`

`source venv/bin/activate`  
 On Windows use `venv\Scripts\activate` 

### **3\. Install Dependencies**

Install the required Python packages using `pip`:

`pip install -r requirements.txt` 

* * *

**Usage**
---------

### **Running the Project**

1.  **Database Setup**: Ensure your PostgreSQL container is running (if using Docker).
    
    If you haven’t already set up the database, run the following commands to apply the migrations:
    
    `python manage.py makemigrations`

    `python manage.py migrate` 
    
2.  **Start the Development Server**:
    
    `python manage.py runserver` 
    
    The server will be running at `http://127.0.0.1:8000`.
    

* * *

### **API Endpoints**

The following API endpoints are available for interacting with the system:

#### **1\. Register Customer**

**POST /register**

Registers a new customer with the following required fields:

*   `first_name`: Customer's first name (string)
*   `last_name`: Customer's last name (string)
*   `phone_number`: Customer's phone number (string)
*   `age`: Customer's age (integer)
*   `monthly_income`: Customer's monthly income (integer)

**Response**:

*   `customer_id`: Unique ID of the customer
*   `name`: Full name of the customer
*   `age`: Customer's age
*   `monthly_income`: Monthly income of the customer
*   `approved_limit`: Approved credit limit
*   `phone_number`: Phone number of the customer

* * *

#### **2\. Check Loan Eligibility**

**POST /check-eligibility**

Checks the loan eligibility based on the customer’s credit history. The request body should include:

*   `customer_id`: Customer's ID
*   `loan_amount`: Requested loan amount
*   `interest_rate`: Interest rate for the loan
*   `tenure`: Loan tenure (in months)

**Response**:

*   `approval`: Boolean indicating loan approval status
*   `interest_rate`: Original interest rate
*   `corrected_interest_rate`: Adjusted interest rate based on eligibility
*   `monthly_installment`: Monthly EMI for the loan

* * *

#### **3\. Create Loan**

**POST /create-loan**

Allows the creation of a new loan for the customer. The request body should include:

*   `customer_id`: Customer's ID
*   `loan_amount`: Requested loan amount
*   `interest_rate`: Interest rate for the loan
*   `tenure`: Loan tenure (in months)

**Response**:

*   `loan_id`: ID of the approved loan (null if not approved)
*   `customer_id`: Customer's ID
*   `loan_approved`: Boolean indicating whether the loan was approved
*   `message`: Message indicating loan status
*   `monthly_installment`: Monthly installment for the loan

* * *

#### **4\. View Loan Details**

**GET /view-loan/<loan\_id>**

Fetch details of a specific loan, including customer information.

**Response**:

*   `loan_id`: Loan ID
*   `customer`: Customer's details (ID, name, phone number, etc.)
*   `loan_amount`: Approved loan amount
*   `interest_rate`: Interest rate of the loan
*   `monthly_installment`: Monthly repayment
*   `tenure`: Loan tenure

* * *

**Docker Setup**
----------------

### **1\. Docker Compose**

The project is set up to run using Docker Compose, which will manage both the Django web app and the PostgreSQL database. Here's how to get everything running with Docker.

1.  **Build the Docker Containers**:
    
    `docker-compose up --build` 
    
2.  **Run the Containers**:
    
    This will start both the `web` and `db` services.
    
    `docker-compose up` 
    
    The Django app should now be available at `http://localhost:8000`.
    

* * *

### **Testing**

*   **Unit Tests**: You can run the unit tests for the application using the following command:
    
    `python manage.py test` 
    
    This will run all the test cases, including those for API endpoints and business logic.
    

### **Notes**

*   Ensure that you have `PostgreSQL` and `Docker` installed if you're running the project locally.
*   You can modify the `docker-compose.yml` and `settings.py` if you want to configure the application for a different environment or use a different database.
