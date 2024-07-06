import React, { useState } from 'react';





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
    <h2 className="text-xl font-montserrat text-center font-semibold mb-4">Hola! Como puedo ayudarte? :)</h2>
    <p className="text-xl font-montserrat text-center mb-4">Me llamo BLEC, tu asistente virtual para agenda de citas con la Dr. Belinda, necesitas agendar?</p>
  </div>
);

const ChatActionButtons = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');

  const sendMessage = (e) => {
    e.preventDefault();
    if (newMessage.trim()) {
      setMessages([...messages, { id: Date.now(), text: newMessage }]);
      setNewMessage('');
    }
  };
  return (
    <div className="w-full h-full flex flex-col justify-end bg-white p-6 rounded-lg">
      <div className="space-y-4 overflow-auto max-h-96">
          {messages.map((message) => (
          <p key={message.id} className="p-2 bg-blue-100 rounded-lg">{message.text}</p>
          ))}
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
  )
  
};

export default ChatUI;
