Objective:

Expand your knowledge and practical skills with FastAPI by adding new features to an existing FastAPI application. This exercise will help you understand RESTful service conventions and deepen your experience with database operations using FastAPI.

Setup Instructions:

Fork and Clone Repository: Start by forking the provided repository available at https://github.com/p1v2/hillel-fastapi-3. Once forked, clone your fork to your local machine.
Set Up Your Development Environment:
If you're familiar with virtual environments, set one up using python -m venv env and activate it with source env/bin/activate (Linux/macOS) or env\Scripts\activate (Windows).
Install the required packages using pipenv install.
Database Setup:
MySQL Option: If you have MySQL installed, create a new database and configure the database settings in database.py to connect to your MySQL instance.
SQLite Option: If setting up MySQL is an issue, modify the database connection in database.py to use SQLite instead by setting the connection string to something like sqlite:///./test.db.
Check the Products Table:
Check SQLAlchemy model for products in models.py. and add few more table columns. Create a products table in your DB
Assignment Tasks:

Implement"Update Product' API:
Create a new API endpoint to handle PATCH requests at /products/{product_id}.
This endpoint should allow partial updates to a product, such as updating the name or price.
Implement 'Delete Product' API:
Create a new API endpoint to handle DELETE requests at /products/{product_id}.
This endpoint should remove a product from the database based on its ID.
Testing:

Ensure that you test your API endpoints using a tool like Postman or Swagger UI to make sure they work as expected.
Submission:

Once you have completed the modifications, commit your changes to your local git repository and push them to your forked repository on GitHub.
Submit a pull request from your repository to the original repository at https://github.com/p1v2/hillel-fastapi-3. Make sure to provide a clear description of the changes you've implemented.
Evaluation Criteria:

Correct implementation of the PATCH and DELETE endpoints following RESTful principles.
Proper handling of database interactions and error conditions.
Clear and concise code that follows Python coding standards.
Take this assignment as an opportunity to demonstrate your ability to work with FastAPI, handle database connections, and follow good practices in API development. 
