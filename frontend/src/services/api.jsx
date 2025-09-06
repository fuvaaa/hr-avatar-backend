const API_BASE = process.env.REACT_APP_API_BASE || 'https://hr-avatar-backend.onrender.com';

const uploadDocuments = async (formData) => {
  const response = await fetch(`${API_BASE}/api/upload-documents`, {
    method: 'POST',
    body: formData,
  });
  return await response.json();
};

const analyzeMatch = async (formData) => {
  const response = await fetch(`${API_BASE}/api/analyze-match`, {
    method: 'POST',
    body: formData,
  });
  return await response.json();
};

const startInterview = async (formData) => {
  const response = await fetch(`${API_BASE}/api/start-interview`, {
    method: 'POST',
    body: formData,
  });
  return await response.json();
};

const nextQuestion = async (sessionId, response) => {
  const responseObj = await fetch(`${API_BASE}/api/next-question`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      session_id: sessionId,
      response: response,
    }),
  });
  return await responseObj.json();
};

const finishInterview = async (sessionId) => {
  const response = await fetch(`${API_BASE}/api/finish-interview`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      session_id: sessionId,
    }),
  });
  return await response.json();
};

const generateReport = async (sessionId) => {
  const response = await fetch(`${API_BASE}/api/generate-report`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      session_id: sessionId,
      format: 'json',
    }),
  });
  return await response.json();
};

const voiceToText = async (formData) => {
  const response = await fetch(`${API_BASE}/api/voice-to-text`, {
    method: 'POST',
    body: formData,
  });
  return await response.json();
};

const textToVoice = async (text, language = 'ru') => {
  const response = await fetch(`${API_BASE}/api/text-to-voice?text=${encodeURIComponent(text)}&language=${language}`);
  return await response.blob();
};

export {
  uploadDocuments,
  analyzeMatch,
  startInterview,
  nextQuestion,
  finishInterview,
  generateReport,
  voiceToText,
  textToVoice,
};