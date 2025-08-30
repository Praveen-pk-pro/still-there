# Career Compass 🚀

AI-powered career helper web application with resume analysis, roadmap generation, cover letter creation, job matching, and ATS-optimized resume building.

## Features

- Resume Analyzer with AI-powered feedback
- Domain-specific Learning Roadmaps
- Personalized Cover Letter Generator
- Job Match and Skill Gap Analyzer
- ATS-Free Resume Maker
- User Authentication with Supabase

## Tech Stack

- **Backend**: Python with FastAPI
- **Frontend**: React with TailwindCSS
- **Database**: Supabase (PostgreSQL)
- **AI**: DeepSeek API
- **Authentication**: Supabase Auth
- **Deployment**: Vercel (Frontend) + Render (Backend)

## Prerequisites

- Node.js (v16 or higher)
- Python (v3.9 or higher)
- Git
- Supabase account ([supabase.com](https://supabase.com))
- DeepSeek API account ([platform.deepseek.com](https://platform.deepseek.com))

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/career-compass.git
cd career-compass

2. Backend Setup
bash
# Navigate to backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

Edit the .env file with your actual credentials:

env
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url_here
SUPABASE_KEY=your_supabase_anon_key_here

# DeepSeek API
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Application
SECRET_KEY=your_secret_key_here
ENVIRONMENT=development

# File Upload
MAX_FILE_SIZE=10485760
UPLOAD_DIR=./uploads

3. Frontend Setup
bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
Edit the .env file with your actual credentials:

env
REACT_APP_SUPABASE_URL=your_supabase_project_url_here
REACT_APP_SUPABASE_ANON_KEY=your_supabase_anon_key_here
REACT_APP_API_URL=http://localhost:8000

4. Database Setup
Create a new project at supabase.com

Go to Settings > API to find your URL and anon key

Go to the SQL Editor and run the SQL schema from supabase/sql.txt

5. Run the Application
bash
# Start the backend (from backend directory)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# In a new terminal, start the frontend (from frontend directory)
npm start
The application will be available at:

Frontend: http://localhost:3000

Backend API: http://localhost:8000

API Documentation: http://localhost:8000/docs


Online Deployment
Frontend Deployment (Vercel)
Push your code to a GitHub repository

Go to vercel.com and sign in with your GitHub account

Click "New Project" and import your Career Compass repository

Configure the project settings:

Framework Preset: Create React App

Root Directory: frontend

Build Command: npm run build

Output Directory: build

Install Command: npm install

Add environment variables in Vercel dashboard:

REACT_APP_SUPABASE_URL: your_supabase_project_url_here

REACT_APP_SUPABASE_ANON_KEY: your_supabase_anon_key_here

REACT_APP_API_URL: your_backend_deployment_url_here

Click "Deploy"

Backend Deployment (Render)
Go to render.com and sign up/login

Click "New +" and select "Web Service"

Connect your GitHub repository

Configure the service:

Name: career-compass-backend

Environment: Python 3

Region: Select the closest to your users

Branch: main (or your preferred branch)

Root Directory: backend

Build Command: pip install -r requirements.txt

Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT

Add environment variables:

SUPABASE_URL: your_supabase_project_url_here

SUPABASE_KEY: your_supabase_anon_key_here

DEEPSEEK_API_KEY: your_deepseek_api_key_here

SECRET_KEY: your_secret_key_here

ENVIRONMENT: production

MAX_FILE_SIZE: 10485760

UPLOAD_DIR: ./uploads

Click "Create Web Service"

Environment Variables for Production
Update your frontend environment variables in Vercel to use the deployed backend URL:

env
REACT_APP_API_URL=https://your-backend-service.onrender.com
Database Setup for Production
In your Supabase project, go to Settings > Database

Add connection pooling for better performance

Set up appropriate security settings for production

Configuration Details
Getting Supabase Credentials
Create a project at supabase.com

Go to Settings > API

Find your Project URL and anon/public key

Getting DeepSeek API Key
Sign up at platform.deepseek.com

Go to API Keys section

Create a new API key

Setting Up File Storage
For production, you'll want to use a proper file storage solution instead of local filesystem:

Set up Supabase Storage or AWS S3

Update the file handling functions to use your cloud storage

Update environment variables accordingly

Troubleshooting
Common Issues
CORS errors:

Ensure your backend CORS settings include your frontend domain

Check that environment variables are correctly set

Database connection issues:

Verify your Supabase credentials

Check if your database tables are properly created

File upload issues:

Ensure the upload directory has proper permissions

For production, use cloud storage instead of local filesystem

API errors:

Verify your DeepSeek API key is valid

Check your API quota and billing

Build failures:

Ensure all dependencies are correctly specified

Check Python and Node.js versions

Debugging Tips
Check application logs on Render dashboard

Use browser developer tools to debug frontend issues

Test API endpoints using the Swagger UI at /docs

Verify environment variables are correctly set in both environments

Maintenance
Updating the Application
Make changes to your code

Test locally

Push to GitHub

Vercel and Render will automatically redeploy

Monitoring
Use Render's metrics to monitor backend performance

Use Vercel Analytics for frontend monitoring

Set up error tracking with services like Sentry

Backup Strategy
Regularly backup your Supabase database

Keep your code in GitHub for version control

Store environment variables securely

Support
If you encounter issues:

Check the troubleshooting section above

Review Render and Vercel documentation

Check Supabase status at status.supabase.com

Create an issue in the GitHub repository

License
MIT License - see LICENSE file for details

text

## Additional Deployment Files

### frontend/vercel.json (for Vercel deployment)

```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/favicon.ico",
      "dest": "/favicon.ico"
    },
    {
      "src": "/manifest.json",
      "dest": "/manifest.json"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "env": {
    "REACT_APP_SUPABASE_URL": "@react_app_supabase_url",
    "REACT_APP_SUPABASE_ANON_KEY": "@react_app_supabase_anon_key",
    "REACT_APP_API_URL": "@react_app_api_url"
  }
}


backend/render.yaml (for Render deployment)
yaml
services:
  - type: web
    name: career-compass-backend
    env: python
    plan: free
    branch: main
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: SUPABASE_URL
        fromSecret: SUPABASE_URL
      - key: SUPABASE_KEY
        fromSecret: SUPABASE_KEY
      - key: DEEPSEEK_API_KEY
        fromSecret: DEEPSEEK_API_KEY
      - key: SECRET_KEY
        fromSecret: SECRET_KEY
      - key: ENVIRONMENT
        value: production
      - key: MAX_FILE_SIZE
        value: 10485760
      - key: UPLOAD_DIR
        value: ./uploads