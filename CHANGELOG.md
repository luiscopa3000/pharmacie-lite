# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-09-16

### Added
- Initial project setup for the Pharmacie Management System Backend.
- Core FastAPI application with standard HTTP error handling and middleware setup.
- Database settings validation configuration (`.env` validation).
- Authentication flow using JWT tokens (POST `/auth/companies/{id_compania}/access-token`).
- User creation and security workflows (POST `/security/users`).
- Basic project documentation, requirements, and `.gitignore`.
