**Jaitaw** API by Django

## Introduction

This repository provides a mini Django REST Framework API for building a social media application. It offers essential features like user accounts, posts, comments, notifications, and tag-based post retrieval.

## Features

- **User Accounts:**
  - Login and registration
  - Profile management
  - Follower/following functionality
  - Secure authentication with JSON Web Tokens (JWT)
- **Posts:**
  - Create, read, update, and delete posts
  - Like and save posts
  - Retrieve posts by code and liked/saved posts for a user
- **Comments:**
  - Create, read, update, and delete comments
  - Like comments
  - Get comments for a specific post
- **Notifications:**
  - View inbox notifications
  - Get notification badge count
  - Mark all notifications as read
- **Tags:**
  - Retrieve posts by tag name

## Installation

### Prerequisites

- Python (version 3.7 or later recommended)
- pip (package installer for Python)

### Setting Up a Virtual Environment (Recommended)

**Mac/Linux:**

1. Open your terminal.
2. Create a virtual environment using `python3 -m venv venv`
3. Activate the environment: `source venv/bin/activate`

**Windows:**

1. Open your command prompt.
2. Create a virtual environment using `python -m venv venv`.
3. Activate the environment: `venv\Scripts\activate`

### Installing Dependencies

1. Inside the activated virtual environment, run:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Clone this repository:

   ```bash
   git clone https://github.com/maokimkorng/jaitaw.git
   ```

2. Navigate to the project directory:

   ```bash
   cd jaitaw
   ```

3. Create a local copy of the `.env` file (located in the project root) and add environment variables.

   ```
   SECRET_KEY=your_secret_key
   ALLOWED_HOSTS=localhost,127.0.0.1  # Add additional allowed hosts if needed
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

   This will typically start the server at `http://127.0.0.1:8000/`. Access the API documentation at the root path for detailed usage instructions.

## API Documentation

Detailed API documentation is available at `http://127.0.0.1:8000/` when the development server is running. It provides comprehensive information about endpoints, request methods, parameters, responses, and authentication requirements.