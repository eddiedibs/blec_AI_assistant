import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import StreamComponent from "../components/StreamComponent";
import ChatForm from "../components/shared/ChatForm";
import axios from "axios";
import { Spinner  } from "flowbite-react";

const ChatUI = () => {
  const [isChatFormSubmitted, setIsChatFormSubmitted] = useState(false);
  const [requestBody, setRequestBody] = useState(null); // Add state for request body
  const [csrftoken, setCsrfToken] = useState(null);

  // Animation variants
  const formVariants = {
    hidden: { opacity: 0, y: 50 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
  };

  const getCsrfToken = async () => {
    const response = await axios.get("http://localhost:8082/api/csrf");
    // const response = await axios.get("api/csrf");
    return response.data.csrfToken; // Adjust the key based on the backend response
  };

  useEffect(() => {
    const fetchToken = async () => {
      const token = await getCsrfToken();
      setCsrfToken(token);
    };
    fetchToken();
  }, []);

  return (
    <div className="w-full h-screen flex flex-col">
      <ChatTitleText />
      <ChatActionButtons
        isChatFormSubmitted={isChatFormSubmitted}
        requestBody={requestBody} // Pass request body to ChatActionButtons
      />
      {!isChatFormSubmitted && (
        <motion.div
          variants={formVariants}
          initial="hidden"
          animate="visible"
        >
          <ChatForm
            onSubmit={(data) => {
              const requestBodyString = JSON.stringify(data); // Convert the data to a string
              setRequestBody(requestBodyString); // Set the submitted data as a string
              setIsChatFormSubmitted(true); // Mark form as submitted
            }}
          />
        </motion.div>
      )}
    </div>
  );
};

const ChatTitleText = () => (
  <div className="w-full h-full flex flex-col items-center p-6 justify-center">
    <h2 className="text-xl font-montserrat text-center font-semibold mb-4">
      ¡Hola! ¿Cómo puedo ayudarte? :)
    </h2>
    <p className="text-xl font-montserrat text-center mb-4">
      Me llamo Liz, tu asistente virtual para agenda de citas. ¿Necesitas agendar?
    </p>
  </div>
);

const ChatActionButtons = ({ isChatFormSubmitted, requestBody }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [currentBotMessageId, setCurrentBotMessageId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleStreamUpdate = (partialResponse) => {
  
    setMessages((prev) =>
      prev.map((message) => {
        if (message.sender === "chatbot") {
          return { ...message, text: message.text + partialResponse };
        }
        return message;
      })
    );
  
    setIsLoading(false);

  };

  const handleFormSubmit = (message) => {
    if (!message?.trim()) return;

    const userMessage = { id: Date.now(), text: message, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);

    // Simulate bot response
    const botMessageId = Date.now() + 1;
    setMessages((prev) => [
      ...prev,
      { id: botMessageId, text: "", sender: "chatbot" },
    ]);
    setCurrentBotMessageId(botMessageId);
    setIsLoading(true);
  };

  // Trigger form submission when requestBody contains a value
  useEffect(() => {
    if (requestBody) {
      handleFormSubmit(requestBody);
    }
  }, [requestBody]); // Runs whenever requestBody changes


  return (
    <div className="w-full h-full flex flex-col justify-end bg-white p-6 rounded-lg">
      {isLoading && (
          <div className="flex justify-center items-center">
            <Spinner aria-label="Loading spinner" />
            <span className="ml-2">Loading...</span>
          </div>
        )}
      <div className="space-y-4 overflow-auto max-h-96">
      {messages
      .filter((message) => message.sender === "chatbot")
      .map((message) => (
        <p
          key={message.id}
          className="p-2 rounded-lg bg-gray-200 self-start text-left"
        >
          {message.text}
        </p>
      ))}

        {/* {isChatFormSubmitted && requestBody && (
          <StreamComponent
            inputMsg={requestBody} // Pass the requestBody to StreamComponent
            csrftoken={csrftoken}
            onStreamUpdate={handleStreamUpdate}
          />
        )} */}

        {isChatFormSubmitted && requestBody &&(
          <StreamComponent
            inputMsg={requestBody}
            csrftoken={csrftoken}
            onStreamUpdate={handleStreamUpdate}
          />
        )}
      </div> 

      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleFormSubmit(newMessage);
          setNewMessage(""); // Clear the input field
        }}
        className={`flex space-x-4 mt-4 hidden`}
      >
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
