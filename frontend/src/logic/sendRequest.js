import axios from 'axios';

export const fetchBlecAiData = async (myInput, csrftoken, onMessageReceived) => {
  const url = 'http://localhost:8082/api/blec_ai';
  let buffer = ''; // To store incomplete chunks

  try {
    const response = await axios.post(url, myInput, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken, // Uncomment if CSRF token is required
      },
      responseType: 'stream', // Ensure Axios expects a stream
    });

    const reader = response.data.getReader(); // Access the stream reader

    const read = async () => {
      const { done, value } = await reader.read();
      if (done) {
        console.log("[END]");
        return;
      }

      const decoder = new TextDecoder();
      buffer += decoder.decode(value); // Accumulate the chunks in buffer

      // Process complete JSON objects
      let boundary = buffer.indexOf('}'); // Find the end of the first JSON object
      while (boundary !== -1) {
        const jsonString = buffer.slice(0, boundary + 1); // Extract complete JSON
        buffer = buffer.slice(boundary + 1); // Keep the remaining buffer
        try {
          console.log("jsonString OUTPUT:", jsonString);
          const json = JSON.parse(jsonString + "}"); // Parse JSON
          if (json.message && json.message.content) {
            onMessageReceived(json.message.content); // Pass the content to the callback
          }
        } catch (err) {
          console.error("Failed to parse JSON:", err, jsonString);
        }
        boundary = buffer.indexOf('}'); // Check for the next JSON object
      }

      read(); // Continue reading
    };

    read();
  } catch (error) {
    console.error("Error during the request:", error);
  }
};
