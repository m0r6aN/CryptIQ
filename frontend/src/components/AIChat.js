import React, { useState } from 'react';
import API from '../services/api';

function AIChat() {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const res = await API.post('ai/chat/', { prompt });
      setResponse(res.data.response);
    } catch (error) {
      console.error('Error getting AI response:', error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-xl mb-4">AI Assistant</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={prompt}
          onChange={e => setPrompt(e.target.value)}
          placeholder="Ask me anything..."
          className="w-full p-2 mb-2"
        />
        <button type="submit" className="bg-blue-500 text-white p-2">Send</button>
      </form>
      {response && (
        <div className="mt-4 p-4 bg-gray-800 text-white">
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}

export default AIChat;
