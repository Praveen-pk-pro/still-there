import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';

const ResumeAnalyzer = () => {
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const { user } = useAuth();

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      const validTypes = ['application/pdf', 'image/png', 'image/jpeg', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
      if (validTypes.includes(selectedFile.type)) {
        setFile(selectedFile);
        setError('');
      } else {
        setError('Please select a PDF, PNG, JPG, or DOCX file');
      }
    }
  };

  const analyzeResume = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setIsLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/resume/analyze', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${user.token}`
        },
        body: formData
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError('Server down, please try again later');
    } finally {
      setIsLoading(false);
    }
  };

  const downloadImprovedResume = async () => {
    try {
      const response = await fetch(`/api/resume/download-improved/${result.resume_id}`, {
        headers: {
          'Authorization': `Bearer ${user.token}`
        }
      });

      if (!response.ok) {
        throw new Error('Download failed');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `improved_resume.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError('Download failed, please try again');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Resume Analyzer</h1>
        
        <div className="bg-white shadow rounded-lg p-6 mb-8">
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Upload Your Resume
            </label>
            <input
              type="file"
              accept=".pdf,.png,.jpg,.jpeg,.docx"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
            />
            <p className="mt-1 text-sm text-gray-500">
              PDF, PNG, JPG, or DOCX files accepted
            </p>
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-50 text-red-700 rounded-md">
              {error}
            </div>
          )}

          <button
            onClick={analyzeResume}
            disabled={isLoading || !file}
            className="w-full bg-indigo-600 text-white py-3 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Analyzing...
              </div>
            ) : (
              'Analyze Resume'
            )}
          </button>
        </div>

        {result && (
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Analysis Results</h2>
            
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-700 mb-2">Resume Score</h3>
              <div className="w-full bg-gray-200 rounded-full h-4">
                <div 
                  className="bg-indigo-600 h-4 rounded-full" 
                  style={{ width: `${result.score}%` }}
                ></div>
              </div>
              <p className="mt-2 text-sm text-gray-600">{result.score}/100</p>
            </div>

            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-700 mb-2">Analysis</h3>
              <p className="text-gray-600">{result.analysis}</p>
            </div>

            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-700 mb-2">Suggested Improvements</h3>
              <ul className="list-disc list-inside text-gray-600 space-y-2">
                {result.improvements.map((imp, index) => (
                  <li key={index}>{imp}</li>
                ))}
              </ul>
            </div>

            <button
              onClick={downloadImprovedResume}
              className="w-full bg-green-600 text-white py-3 px-4 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
            >
              Download Improved Resume
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResumeAnalyzer;