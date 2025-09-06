import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import AnalysisResult from './components/AnalysisResult';
import InterviewInterface from './components/InterviewInterface';
import ReportViewer from './components/ReportViewer';
import VoiceInterface from './components/VoiceInterface';

function App() {
  const [activeTab, setActiveTab] = useState('upload');
  const [analysisData, setAnalysisData] = useState(null);
  const [interviewSession, setInterviewSession] = useState(null);
  const [reportData, setReportData] = useState(null);

  const handleAnalysisComplete = (data) => {
    setAnalysisData(data);
    setActiveTab('analysis');
  };

  const handleInterviewStart = (sessionData) => {
    setInterviewSession(sessionData);
    setActiveTab('interview');
  };

  const handleInterviewComplete = (evaluation) => {
    setReportData(evaluation);
    setActiveTab('report');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="gradient-bg text-white py-6 px-4 shadow-lg">
        <div className="container mx-auto flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center mb-4 md:mb-0">
            <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center mr-3">
              <span className="text-indigo-600 font-bold text-xl">HR</span>
            </div>
            <h1 className="text-2xl font-bold">HR-Avatar</h1>
          </div>
          <p className="text-indigo-100 text-center md:text-right">
            AI-система для подбора и оценки персонала
          </p>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white shadow-sm sticky top-0 z-10">
        <div className="container mx-auto px-4">
          <div className="flex flex-wrap justify-center md:justify-start">
            {[
              { id: 'upload', label: 'Загрузка документов' },
              { id: 'analysis', label: 'Анализ соответствия' },
              { id: 'interview', label: 'Интервью' },
              { id: 'voice', label: 'Голосовое взаимодействие' },
              { id: 'report', label: 'Отчеты' }
            ].map(tab => (
              <button
                key={tab.id}
                className={`px-4 py-3 font-medium text-sm transition-colors ${
                  activeTab === tab.id 
                    ? 'text-indigo-600 border-b-2 border-indigo-600' 
                    : 'text-gray-500 hover:text-gray-700'
                }`}
                onClick={() => setActiveTab(tab.id)}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {activeTab === 'upload' && (
          <FileUpload 
            onAnalysisComplete={handleAnalysisComplete}
            onInterviewStart={handleInterviewStart}
          />
        )}
        
        {activeTab === 'analysis' && analysisData && (
          <AnalysisResult data={analysisData} />
        )}
        
        {activeTab === 'interview' && (
          <InterviewInterface 
            sessionData={interviewSession}
            onInterviewComplete={handleInterviewComplete}
          />
        )}
        
        {activeTab === 'voice' && (
          <VoiceInterface />
        )}
        
        {activeTab === 'report' && reportData && (
          <ReportViewer data={reportData} />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8 px-4 mt-12">
        <div className="container mx-auto text-center">
          <p>© 2023 HR-Avatar. Решение для хакатона.</p>
          <p className="text-gray-400 mt-2 text-sm">
            Автоматизация HR-процессов с использованием искусственного интеллекта
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;