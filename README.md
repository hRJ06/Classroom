# Google Classroom API Documentation

[![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=for-the-badge&logo=cloudinary&logoColor=white)](https://cloudinary.com/)

A Flask-based REST API implementation of core Google Classroom features.

## HTTP Methods
![GET](https://img.shields.io/badge/GET-4AB9F9?style=for-the-badge)
![POST](https://img.shields.io/badge/POST-49CC90?style=for-the-badge)
![PUT](https://img.shields.io/badge/PUT-FCA130?style=for-the-badge)
![DELETE](https://img.shields.io/badge/DELETE-F93E3E?style=for-the-badge)

## Authentication

| Endpoint | Method | Description | Request Body | Response |
|----------|:--------:|-------------|--------------|-----------|
| `/` | ![GET](https://img.shields.io/badge/GET-4AB9F9?style=flat-square) | Welcome endpoint | None | Welcome message |
| `/signup` | ![POST](https://img.shields.io/badge/POST-49CC90?style=flat-square) | Register new user | `{"name": string, "email": string, "password": string, "role": string}` | Success/Error message |
| `/login` | ![POST](https://img.shields.io/badge/POST-49CC90?style=flat-square) | Login user | `{"email": string, "password": string}` | JWT token |
| `/profile` | ![GET](https://img.shields.io/badge/GET-4AB9F9?style=flat-square) | Get user profile | None | User profile details |

## Course Management

| Endpoint | Method | Description | Request Body | Response |
|----------|:--------:|-------------|--------------|-----------|
| `/course` | ![POST](https://img.shields.io/badge/POST-49CC90?style=flat-square) | Create new course | `{"name": string, "code": string}` | Success/Error message |
| `/course` | ![GET](https://img.shields.io/badge/GET-4AB9F9?style=flat-square) | Get all courses | None | List of courses |
| `/course/<course_id>` | ![GET](https://img.shields.io/badge/GET-4AB9F9?style=flat-square) | Get course by ID | None | Course details |
| `/course/enroll/<course_id>` | ![PUT](https://img.shields.io/badge/PUT-FCA130?style=flat-square) | Enroll in course | `{"code": string}` | Success/Error message |
| `/course/unenroll/<course_id>` | ![PUT](https://img.shields.io/badge/PUT-FCA130?style=flat-square) | Unenroll from course | None | Success/Error message |
| `/course/archive/<course_id>` | ![PUT](https://img.shields.io/badge/PUT-FCA130?style=flat-square) | Archive course | None | Success/Error message |
| `/course/unarchive/<course_id>` | ![PUT](https://img.shields.io/badge/PUT-FCA130?style=flat-square) | Unarchive course | None | Success/Error message |

## Assignment Management

| Endpoint | Method | Description | Request Body | Response |
|----------|:--------:|-------------|--------------|-----------|
| `/assignment/create-assignment/<course_id>` | ![POST](https://img.shields.io/badge/POST-49CC90?style=flat-square) | Create assignment | Form data with: `name`, `description`, `graded`, `marks`, `deadline`, `files` | Success/Error message |
| `/assignment/get-assignment/<course_id>` | ![GET](https://img.shields.io/badge/GET-4AB9F9?style=flat-square) | Get course assignments | None | List of assignments |
| `/assignment/add-submission/<assignment_id>` | ![POST](https://img.shields.io/badge/POST-49CC90?style=flat-square) | Submit assignment | Form data with `files` | Success/Error message |

## Submission Management

| Endpoint | Method | Description | Request Body | Response |
|----------|:--------:|-------------|--------------|-----------|
| `/submission/delete-submission/<submission_id>` | ![DELETE](https://img.shields.io/badge/DELETE-F93E3E?style=flat-square) | Delete submission | None | Success/Error message |
| `/submission/grade-submission/<submission_id>` | ![PUT](https://img.shields.io/badge/PUT-FCA130?style=flat-square) | Grade submission | `{"grade": number}` | Success/Error message |

## Announcement Management

| Endpoint | Method | Description | Request Body | Response |
|----------|:--------:|-------------|--------------|-----------|
| `/announcement/create-announcement/<course_id>` | ![POST](https://img.shields.io/badge/POST-49CC90?style=flat-square) | Create announcement | TBD | Success/Error message |
| `/announcement/get-announcement/<course_id>` | ![GET](https://img.shields.io/badge/GET-4AB9F9?style=flat-square) | Get course announcements | None | List of announcements |

## Authentication Requirements

- All endpoints except `/`, `/signup`, and `/login` require JWT authentication
- Role-based access control is implemented:
  - `@role_instructor`: Only instructors can access
  - `@role_student`: Only students can access

## File Upload

- File uploads are supported for assignments and submissions
- Files are stored using Cloudinary
- Multiple files can be uploaded simultaneously

## Error Handling

- All endpoints return appropriate HTTP status codes
- Error messages are returned in JSON format
- Server errors are logged using Flask's logging system

## Transactions

- MongoDB transactions are used for operations requiring multiple database updates
- Sessions are properly managed and cleaned up

## Response Format

All API responses follow this general format:
```json
{
    "message": "Status message",
    "data": {} // Optional data object
}
```

Error responses:
```json
{
    "message": "Error description"
}
```
