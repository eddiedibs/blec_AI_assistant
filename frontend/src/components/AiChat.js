import React, { useState } from 'react';
import { fetchBlecAiData } from '../logic/sendRequest'; // Adjust the import path as needed
import { motion } from 'framer-motion';
import StreamComponent from '../components/StreamComponent';
import ChatForm from '../components/shared/ChatForm';

const ChatUI = () => {
  const [isChatFormSubmitted, setIsChatFormSubmitted] = useState(false);
    // Animation variants
  const formVariants = {
    hidden: { opacity: 0, y: 50 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
  };
  return (
    <div className='w-full h-screen flex flex-col'>
      <ChatTitleText />
      <ChatActionButtons isChatFormSubmitted={isChatFormSubmitted} />
      {!isChatFormSubmitted && (
          <motion.div
          variants={formVariants}
          initial="hidden"
          animate="visible"
        >
        <ChatForm onSubmit={() => setIsChatFormSubmitted(true)} />
       </motion.div>
      )}
    </div>
  );
};

const ChatTitleText = () => (
  <div className='w-full h-full flex flex-col items-center p-6 justify-center'>
    <h2 className="text-xl font-montserrat text-center font-semibold mb-4">¡Hola! ¿Cómo puedo ayudarte? :)</h2>
    <p className="text-xl font-montserrat text-center mb-4">Me llamo Liz, tu asistente virtual para agenda de citas con la Dr. Belinda. ¿Necesitas agendar?</p>
  </div>
);

const ChatActionButtons = ({ isChatFormSubmitted }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [currentBotMessageId, setCurrentBotMessageId] = useState(null);

  const sendMessage = async (e) => {
    e.preventDefault();

    if (!newMessage.trim()) return;

    const userMessage = { id: Date.now(), text: newMessage, sender: 'user' };
    setMessages((prev) => [...prev, userMessage]);
    setNewMessage('');

    const botMessageId = Date.now() + 1;
    setMessages((prev) => [
      ...prev,
      { id: botMessageId, text: '', sender: 'chatbot' },
    ]);
    setCurrentBotMessageId(botMessageId);
  };

  const handleStreamUpdate = (partialResponse) => {
    setMessages((prev) =>
      prev.map((message) =>
        message.id === currentBotMessageId
          ? { ...message, text: message.text + partialResponse }
          : message
      )
    );
  };



  return (
    <div className="w-full h-full flex flex-col justify-end bg-white p-6 rounded-lg">
      <div className="space-y-4 overflow-auto max-h-96">
        {messages.map((message) => (
          <p
            key={message.id}
            className={`p-2 rounded-lg ${
              message.sender === 'user'
                ? 'bg-blue-100 self-end text-right'
                : 'bg-gray-200 self-start text-left'
            }`}
          >
            {message.text}
          </p>
        ))}

        {currentBotMessageId && (
          <StreamComponent
            inputMsg={messages[messages.length - 2]?.text}
            csrftoken={csrftoken}
            onStreamUpdate={handleStreamUpdate}
          />
        )}

        {/* Add animation to ChatForm */}
        
      </div>

      <form onSubmit={sendMessage} className={`flex space-x-4 mt-4 ${isChatFormSubmitted ? '' : 'hidden'}`}>
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type a message..."
          className="flex-grow px-5 py-3 border rounded-lg focus:outline-none"
        />
        <button type="submit" className="send-btn">
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatUI;
