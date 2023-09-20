import React from "react";
import Message from "./components/Message";
import Button from "@mui/material/Button";
import SendIcon from "@mui/icons-material/Send";
import { useState } from "react";

const App = () => {
  const [promptArea, setPromptArea] = useState("");
  const [question, setQuestion] = useState("");
  const [promptResponse, setPromptResponse] = useState("");

  const handleSubmit = async () => {
    setQuestion(promptArea);
    const url = "http://localhost:8080/api/prompt";
    let tmpPromptResponse = "";
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: promptArea,
        }),
      });
      setPromptArea("");

      // eslint-disable-next-line no-undef
      let decoder = new TextDecoderStream();
      if (!response.body) return;
      const reader = response.body.pipeThrough(decoder).getReader();

      while (true) {
        let { value, done } = await reader.read();

        if (done) {
          break;
        } else {
          tmpPromptResponse += value;
          setPromptResponse(tmpPromptResponse);
        }
      }
    } catch (error) {
      console.log(error);
    }
  };
  return (
    <div className="app">
      <div className="container">
        <h1>Chat with CBN</h1>
        <div className="messages">
          <Message message={question} timestamp="MM/DD 00:00" role="user" />
          <Message
            message={promptResponse}
            timestamp="MM/DD 00:00"
            role="gpt"
          />
        </div>
        <div className="form">
          <input
            onChange={(e) => setPromptArea(e.target.value)}
            value={promptArea}
            type="text"
            placeholder="Send a message"
          />
          <Button
            onClick={handleSubmit}
            variant="contained"
            color="primary"
            className="button"
          >
            <SendIcon />
          </Button>
        </div>
      </div>
    </div>
  );
};

export default App;
