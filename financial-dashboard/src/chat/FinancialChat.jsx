import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import './chat.css';

export default function FinancialChat() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    const newMessages = [...messages, { role: "user", content: query, timestamp: new Date() }];
    setMessages(newMessages);
    setLoading(true);
    setQuery("");

    try {
      const res = await axios.post("http://localhost:8000/query", { query });
      setMessages([...newMessages, { role: "assistant", content: res.data.answer, timestamp: new Date() }]);
    } catch (err) {
      setMessages([...newMessages, { role: "assistant", content: "Error fetching data.", timestamp: new Date() }]);
    }
    setLoading(false);
  };

  useEffect(() => {
    document.title = "Financial Chat";
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="chat-wrapper">
      <h1 className="chat-title">Financial Chat Dashboard</h1>
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.role}`}>
            <div className="bubble">
              {msg.content}
              <div className="timestamp">{formatTime(msg.timestamp)}</div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="chat-message assistant">
            <div className="bubble">
              Typing...
              <div className="timestamp">{formatTime(new Date())}</div>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>
      <form onSubmit={handleSubmit} className="chat-input-form">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="chat-input"
          rows={2}
          placeholder="Type your financial query..."
        ></textarea>
        <button type="submit" className="chat-send">Send</button>
      </form>
    </div>
  );
}
