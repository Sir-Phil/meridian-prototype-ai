"use client";

import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2 } from 'lucide-react';

export default function MeridianChat() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I am the Meridian AI Assistant. How can I help you with inventory or orders today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to latest message
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // const response = await fetch('http://127.0.0.1:8000/api/chat', { ... })
      const API_URL = process.env.NODE_ENV === 'development' 
      ? 'http://127.0.0.1:8000/api/chat' 
      : '/api/chat';

      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error: Could not connect to the Meridian backend.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-50 font-sans">
      {/* Header */}
      <header className="bg-slate-900 text-white p-4 shadow-md">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <div className="bg-blue-500 p-2 rounded-lg">
            <Bot size={24} />
          </div>
          <div>
            <h1 className="font-bold text-lg">Meridian Support Portal</h1>
            <p className="text-xs text-slate-400 font-mono">Agentic Inventory v1.0</p>
          </div>
        </div>
      </header>

      {/* Chat Window */}
      <main ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4">
        <div className="max-w-4xl mx-auto">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} mb-4`}>
              <div className={`flex gap-3 max-w-[80%] ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                <div className={`p-2 rounded-full h-10 w-10 flex items-center justify-center shrink-0 ${msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-slate-200 text-slate-600'}`}>
                  {msg.role === 'user' ? <User size={20} /> : <Bot size={20} />}
                </div>
                <div className={`p-4 rounded-2xl shadow-sm ${msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-white text-slate-800'}`}>
                  <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                </div>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start items-center gap-3 text-slate-400 italic text-sm">
              <Loader2 className="animate-spin" size={16} />
              AI is checking inventory...
            </div>
          )}
        </div>
      </main>

      {/* Input Area */}
      <footer className="p-4 bg-white border-t border-slate-200">
        <div className="max-w-4xl mx-auto flex gap-2">
          <input
            type="text"
            className="flex-1 border border-slate-300 rounded-xl px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
            placeholder="Ask about inventory or check an order..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          />
          <button 
            onClick={handleSend}
            disabled={isLoading}
            className="bg-blue-600 text-white p-3 rounded-xl hover:bg-blue-700 transition-colors disabled:bg-slate-400"
          >
            <Send size={20} />
          </button>
        </div>
      </footer>
    </div>
  );
}