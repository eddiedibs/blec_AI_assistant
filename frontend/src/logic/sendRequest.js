// Modify the function to accept a callback for processing each incoming message.
export const fetchBlecAiData = async (myInput, csrftoken, onMessageReceived) => {
  const url = 'api/blec_ai';
  console.log("HELLO")
  await fetch(url, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      // 'X-CSRFToken': csrftoken,
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
        const message = decoder.decode(value);
        console.log("[Received]: " + message);

        // Call the callback to update messages in the component
        onMessageReceived(message);
        read();
      });
    };
    read();
  });
};
