import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import StreamComponent from "../components/StreamComponent";
import ChatForm from "../components/shared/ChatForm";
import axios from "axios";
import { Spinner  } from "flowbite-react";


const HomePage = () => {
    const [isChatFormSubmitted, setIsChatFormSubmitted] = useState(false);

  
    return (
      <div className="w-full h-screen flex flex-col">
        <p>
            HELLO WORLD
        </p>
      </div>
    );
  };

export default HomePage