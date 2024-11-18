import React, { useState } from 'react';
import { fetchBlecAiData } from '../logic/sendRequest'; // Adjust the import path as needed
import StreamComponent from '../components/StreamComponent';

const ChatUI = () => {

  return (
    <div className='w-full h-screen flex flex-col'>
      <ChatTitleText />
      <ChatActionButtons />
    </div>
  );
};

const ChatTitleText = () => (
  <div className='w-full h-full flex flex-col items-center p-6 justify-center'>
    <h2 className="text-xl font-montserrat text-center font-semibold mb-4">¡Hola! ¿Cómo puedo ayudarte? :)</h2>
    <p className="text-xl font-montserrat text-center mb-4">Me llamo Liz, tu asistente virtual para agenda de citas con la Dr. Belinda. ¿Necesitas agendar?</p>
  </div>
);

const ChatActionButtons = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [isMessageSent, setIsMessageSent] = useState(false); // To track whether the message has been sent

  const sendMessage = (e) => {
    e.preventDefault();
    if (newMessage.trim()) {
      setMessages([...messages, { id: Date.now(), text: newMessage }]);
      setNewMessage('');
      setIsMessageSent(true);  // Mark that a message is sent
    }
  };

  return (
    <div className="w-full h-full flex flex-col justify-end bg-white p-6 rounded-lg">
      <div className="space-y-4 overflow-auto max-h-96">
        {messages.map((message) => (
          <p key={message.id} className="p-2 bg-blue-100 rounded-lg">{message.text}</p>
        ))}
        
        {/* Render StreamComponent only after message is sent */}
        {isMessageSent && (
          <StreamComponent inputMsg={messages[messages.length - 1].text} csrftoken={csrftoken} />
        )}
      </div>

      <form onSubmit={sendMessage} className="flex space-x-4">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type a message..."
          className="flex-grow px-5 py-3 border rounded-lg focus:outline-none"
        />
        <button type="submit" className="send-btn">Send</button>
      </form>
    </div>
  );
};

export default ChatUI;
