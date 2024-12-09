export const fetchBlecAiData = async (myInput, csrftoken, onMessageReceived) => {
  const url = 'api/blec_ai'; // Adjust as necessary
  // const url = 'http://127.0.0.1:8003/api/blec_ai';
  let buffer = ''; // To store incomplete chunks

  await fetch(url, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      // 'X-CSRFToken': csrftoken, // Uncomment if CSRF token is required
    },
    body: JSON.stringify(myInput),
  }).then((res) => {
    const reader = res.body.getReader();

    const read = () => {
      reader.read().then(({ done, value }) => {
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
      });
    };

    read();
  });
};
