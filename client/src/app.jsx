import React, { useState, useRef, useEffect } from 'react';
import { Send, Trash2, Bot, User } from 'lucide-react';

const MathTutorChat = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hola, soy tu tutor de matemáticas. ¿En qué puedo ayudarte hoy?'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleClearChat = () => {
    setMessages([
      { role: 'assistant', content: 'Hola, soy tu tutor de matemáticas. ¿En qué puedo ayudarte hoy?' }
    ]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8001/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: [...messages, { role: 'user', content: userMessage }] })
      });

      const data = await response.json();
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: data.message || 'No pude procesar tu solicitud.' }
      ]);
    } catch {
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: 'Ocurrió un error al procesar tu mensaje.' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0e0e0e] text-gray-100 flex flex-col items-center justify-center font-sans">
      <div className="w-full max-w-4xl flex flex-col h-screen md:h-[90vh]">
        <div className="flex-1 overflow-y-auto p-6 space-y-6 mt-12">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              {msg.role === 'assistant' && (
                <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center mr-3">
                  <Bot className="w-5 h-5 text-white" />
                </div>
              )}
              <div
                className={`max-w-[75%] px-5 py-3 rounded-2xl ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-[#1a1a1a] text-gray-100 border border-[#2a2a2a]'
                }`}
              >
                <p className="leading-relaxed whitespace-pre-wrap">{msg.content}</p>
              </div>
              {msg.role === 'user' && (
                <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center ml-3">
                  <User className="w-5 h-5 text-white" />
                </div>
              )}
            </div>
          ))}
          {loading && (
            <div className="flex gap-3 justify-start">
              <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div className="bg-[#1a1a1a] rounded-2xl px-5 py-3 border border-[#2a2a2a]">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="fixed bottom-10 left-1/2 transform -translate-x-1/2 w-[90%] max-w-3xl">
          <form onSubmit={handleSubmit} className="flex bg-[#1a1a1a] border border-[#2a2a2a] rounded-2xl overflow-hidden shadow-lg">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Pregunta a tu tutor..."
              className="flex-1 bg-transparent text-gray-100 px-5 py-3 focus:outline-none"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 transition-colors disabled:bg-gray-600"
            >
              <Send className="w-5 h-5 text-white" />
            </button>
            <button
              type="button"
              onClick={handleClearChat}
              className="px-4 bg-transparent text-gray-400 hover:text-gray-200 transition-colors"
            >
              <Trash2 className="w-5 h-5" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default MathTutorChat;
