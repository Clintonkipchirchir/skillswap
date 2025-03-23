# Skill Swap Platform

A community-driven web application built with Django and Django Rest Framework that connects users who want to exchange skills. Whether you want to learn a new language, master a programming language, or explore a new hobby, Skill Swap Platform makes it easy to connect with others who share your interests.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture & ERD](#architecture--erd)
- [Tech Stack](#tech-stack)

## Overview

The Skill Swap Platform is designed to facilitate skill exchange among users. Users can create profiles, list the skills they offer and want to learn, create posts (offers or requests), match with other users, schedule sessions, and communicate via an in-app messaging system. The platform also includes a feedback system to build trust and reputation among participants.

## Features

- **User Authentication & Profiles**:  
  - Secure registration, login, and logout functionality.
  - User profiles with extended information (bio, location, and skills offered/desired).

- **Skill Listings & Posts**:  
  - CRUD operations for posts, which can be either skill offers or requests.
  - Integration with a skill database to standardize available skills.

- **Matching System**:  
  - A matching algorithm that connects users with complementary skills.

- **Messaging**:  
  - In-app messaging system for users to coordinate skill swaps.

- **Scheduling**:  
  - Schedule sessions for skill exchanges (with optional calendar integration).

- **Feedback & Ratings**:  
  - Users can leave feedback and ratings after sessions to help build credibility.

## Architecture

The platform follows a modular architecture built on Django, with a RESTful API provided by Django Rest Framework. The ERD (Entity Relationship Diagram) outlines the following key entities:
- **User & Profile**: Each user has a one-to-one profile.
- **Skill**: A many-to-many relationship with profiles.
- **Post**: Represents skill offers or requests.
- **Match**: Connects complementary posts.
- **Message**: Enables communication between users.
- **Schedule**: Organizes session details.
- **Feedback**: Captures session reviews.

A complete ERD diagram can be generated using the provided Mermaid code (see documentation or `/docs` folder).

## Tech Stack

- **Backend:**  
  - Python
  - Django & Django Rest Framework

- **Frontend:**  
  - Django Templates (or a modern frontend framework like React, if desired)

- **Database:**  
  - PostgreSQL (or your choice of relational database)

- **Other Tools & Integrations:**  
  - JWT for token-based authentication
  - Tailwind CSS (or any CSS framework) for responsive design
  - Optional: Google Calendar API for scheduling integration
