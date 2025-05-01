import React from 'react';
import { FaComments } from 'react-icons/fa';
import '../chat/chat.css'; 

const ChatIcon = () => {
  const handleClick = () => {
    window.location.href = '/chatbot';
  };

  return (
    <div className="chat-icon" onClick={handleClick} title="Open Chatbot">
      <FaComments size={24} />
    </div>
  );
};

export default ChatIcon;
