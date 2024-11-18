import React, { useEffect, useState } from 'react';
import { fetchBlecAiData } from '../logic/sendRequest'; // Adjust path as needed

function StreamComponent({ inputMsg, csrftoken }) {
    const [messages, setMessages] = useState('');

    useEffect(() => {
        if (inputMsg) {
            console.log("PASSED:: ", inputMsg)
            fetchBlecAiData({ request_instruction: inputMsg }, csrftoken, (newMessage) => {
                setMessages((prevMessages) => prevMessages + '\n' + newMessage); // Append new messages
            });
        }
    }, [inputMsg, csrftoken]);

    return <p>{messages}</p>;
}

export default StreamComponent;
