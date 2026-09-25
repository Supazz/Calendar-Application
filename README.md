# StudySync

StudySync is an academic planner designed to help students organize
courses, assignments, exams, and study time in one place.

## Description

The application allows students to log academic tasks, estimate the time
needed to complete them, assign priorities, and enter available study times.
These inputs will be used to generate a personalized study schedule to help
students plan and manage their workload more effectively.


## Project Goals

- Organize courses, assignments, and exams
- Track due dates and estimated workload
- Allow students to assign priorities to tasks
- Allow students to enter available study times
- Generate a personalized study schedule
- Track completed tasks and overall progress

## Planned Features

- Course management
- Assignment and exam management
- Due dates and estimated duration
- Task priorities
- Student availability
- Automated study schedule generation
- Task completion tracking
- Progress tracking
- Calendar view
- Event management for academic or personal events
- Canvas integration
- Email integration
  

## Setup and Installation

### Prerequisites

The following software is required:

- Node.js
- Python 3
- Git

### Clone the Repository

Open a terminal and navigate to the location where you want to store the project.

Then clone the repository:

```bash
git clone https://github.com/Supazz/Calendar-Application.git
cd Calendar-Application
```

### Frontend Setup

Install the React dependencies:

```bash
npm install
```

## Running the Application

The React frontend can currently be run independently using:

```bash
npm run dev
```

Vite will provide a local URL where the application can be opened in a web browser.

To exit Vite, press Ctrl + C while in the terminal. 

The backend is currently under development and is not yet fully connected to the React frontend.

## Technology

### Frontend

- React - User interface
- Vite - Frontend development and build tool
- JavaScript - Frontend programming
- CSS - Application styling

### Backend

- Python - Backend programming and application logic
- SQLite - Database for storing application data
- Canvas REST API - Planned integration for importing courses, assignments, and due dates


## Development Workflow

The project uses Scrum and is developed through sprints and product backlog items.

Team members should:
1. Create or select an issue describing the work to be completed.
2. Create a feature branch for the work.
3. Make and test changes on the feature branch.
4. Commit changes using clear commit messages.
5. Push the branch to GitHub.
6. Open a pull request for review.
7. Merge the completed work into the main branch after review.

### Branches

- `main` - Main project branch
- Feature branches - Used for individual features and changes
- Frontend/backend branches may be used for larger areas of development

### Development Guidelines

- Keep changes related to the issue or feature being developed.
- Use descriptive commit messages.
- Test changes before creating a pull request.
- Do not commit passwords, API keys, or other sensitive information.
- Keep documentation updated when project functionality or setup requirements change.
- Communicate with the team before making major structural changes.
- Create a separate branch for new features or significant changes.
- Do not directly modify the main branch unless the team has agreed that the change should be made there.

## Current Status

StudySync is currently in the initial development phase.

The React frontend prototype has been created using React and Vite and currently includes:

- StudySync navigation
- Current date display
- Daily schedule display
- Sample calendar events
- Add Event form interface

The Python backend and React frontend are currently being developed separately. Backend integration, database functionality, and persistent event data are planned for future development.

## Future Development

- Connecting the React frontend to the Python backend
- Implementing SQLite database storage
- Adding course management
- Adding assignment and exam management
- Implementing event creation and management
- Implementing automated study schedule generation
- Adding task completion and progress tracking
- Developing the calendar interface
- Integrating the Canvas REST API
- Exploring email integration

## Team Members

- Diego Arauz
- Carlos Garcia
- Andrew Nguyen
- Jon Pack
- Zachary Pursell