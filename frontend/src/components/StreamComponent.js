import React, { useEffect, useState, useRef } from 'react';
import { fetchBlecAiData } from '../logic/sendRequest'; // Adjust path as needed

function StreamComponent({ inputMsg, csrftoken, onStreamUpdate  }) {
    const lastProcessedMsg = useRef(null);

    useEffect(() => {
        if (inputMsg && lastProcessedMsg.current !== inputMsg) {
            lastProcessedMsg.current = inputMsg; // Mark the current inputMsg as processed
            fetchBlecAiData(
                { request_instruction: inputMsg },
                csrftoken,
                (chunk) => {
                    if (onStreamUpdate) {
                        onStreamUpdate(chunk); // Pass each chunk to the parent
                    }
                }
            );
        }
    }, [inputMsg, csrftoken, onStreamUpdate]);

    return null; // This component does not render anything
}


export default StreamComponent;
