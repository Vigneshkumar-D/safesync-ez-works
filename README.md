# SafeSync EZ Works Backend

This is the backend for the **SafeSync EZ Works** project, built using **FastAPI**. The API allows for user signup, email verification, and more. It integrates email services to send verification emails to newly registered users.

## Features

- **User Signup**: Allows users to register with email and password.
- **Email Verification**: Sends an email with a verification link upon successful signup.
- **Background Task for Email**: Utilizes FastAPI's background tasks to send emails asynchronously.
- **Role-based Access**: Users can register with specific roles (e.g., "Ops").
- **Security**: Passwords are hashed before being stored in the database.

## Setup Instructions

### Prerequisites

1. **Python 3.8+**: Make sure you have Python installed on your machine.
2. **Email Configuration**: Set up a Gmail account and generate an App Password for sending emails.

### Install Dependencies

First, clone the repository:

```bash
git clone https://github.com/your-username/safesync-ez-works.git
cd safesync-ez-works
```

Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

### Environment Variables

You will need to set up the following environment variables for email sending:

- `SMTP_SERVER`: The SMTP server address (e.g., `smtp.gmail.com`).
- `SMTP_PORT`: The port used for SMTP (usually `587`).
- `EMAIL_ADDRESS`: The email address from which emails will be sent (e.g., `your-email@gmail.com`).
- `EMAIL_PASSWORD`: The App Password generated in your Google account.

Make sure to store these in a `.env` file or set them as environment variables.

### Running the Application

To run the application locally, use the following command:

```bash
uvicorn app.main:app --reload
```

The server will be available at `http://127.0.0.1:8000`. You can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

### API Endpoints

- **POST `/signup`**: Allows users to register by providing email, password, and role.

#### Request Body (Signup)

```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "role": "Ops"
}
```

#### Response (Signup)

```json
{
  "message": "User created",
  "encrypted_url": "encrypted_verification_link_here"
}
```

After signing up, a verification email will be sent to the provided email address.

### Testing

To run tests, make sure you have all dependencies installed, and then use:

```bash
pytest
```

### Deployment

For production deployment, you can use Docker or deploy to platforms like **Heroku**, **AWS**, or **DigitalOcean**.

#### Example with Docker

1. Build the Docker image:

    ```bash
    docker build -t safesync-backend .
    ```

2. Run the container:

    ```bash
    docker run -p 8000:8000 safesync-backend
    ```

This will run the app in a Docker container and expose it on port `8000`.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements

- FastAPI for building the backend.
- Pydantic for data validation.
- Uvicorn for the ASGI server.
- SMTP and background task handling for email delivery.


### Explanation:

- **Features**: Lists the core features of your application.
- **Setup Instructions**: Describes how to install dependencies and configure environment variables.
- **API Endpoints**: Documents the `POST /signup` endpoint, which is essential for user registration.
- **Testing**: Explains how to run tests with `pytest`.
- **Deployment**: Briefly describes Docker deployment as an example.
- **Contributing**: Standard steps for contributing to the project.

Make sure to customize the README further based on specific details such as your repository's URL, specific deployment steps, and test cases.
