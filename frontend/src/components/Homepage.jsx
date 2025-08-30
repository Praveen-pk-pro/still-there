import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
  const navigate = useNavigate();
  
  const features = [
    {
      title: "Resume Analyzer",
      description: "Upload your resume and get AI-powered analysis and improvements",
      icon: "📄",
      path: "/resume-analyzer"
    },
    {
      title: "Domain & Roadmap",
      description: "Get a personalized learning roadmap for your career domain",
      icon: "🗺️",
      path: "/roadmap"
    },
    {
      title: "Cover Letter Generator",
      description: "Create professional cover letters tailored to specific jobs",
      icon: "✉️",
      path: "/cover-letter"
    },
    {
      title: "Job Match Analyzer",
      description: "Find your ideal jobs and identify skill gaps",
      icon: "🔍",
      path: "/job-match"
    },
    {
      title: "ATS-Free Resume Maker",
      description: "Create ATS-optimized resumes from scratch",
      icon: "✅",
      path: "/resume-maker"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight lg:text-6xl">
            Career Compass <span className="text-indigo-600">🚀</span>
          </h1>
          <p className="mt-5 text-xl text-gray-600">
            AI-powered tools to accelerate your career journey
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300 cursor-pointer transform hover:-translate-y-1 transition-transform duration-200"
              onClick={() => navigate(feature.path)}
            >
              <div className="p-8">
                <div className="text-4xl mb-6">{feature.icon}</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
                <button className="mt-6 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors duration-200">
                  Get Started
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default HomePage;