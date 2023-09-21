import React from "react";
import Message from "./components/Message";
import Button from "@mui/material/Button";
import SendIcon from "@mui/icons-material/Send";
import { useState } from "react";
// import axios from "axios";

const App = () => {
  const [inputValue, setInputValue] = useState("");
  // const [question, setQuestion] = useState("");
  // const [promptResponse, setPromptResponse] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    // setLoading(true);
    // setQuestion(inputValue);
    // setMessages([
    //   ...messages,
    //   { role: "assistant", content: "How can I help you?" },
    // ]);
    const url = "http://localhost:8080/api/chat";
    let tmpPromptResponse = "";
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_input: inputValue,
          conversation: messages,
        }),
      });

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
          // setPromptResponse(tmpPromptResponse);
          setMessages([
            ...messages,
            { role: "user", content: inputValue },
            { role: "assistant", content: tmpPromptResponse },
          ]);
        }
      }
    } catch (error) {
      console.log(error);
    } finally {
      setInputValue("");
      // setLoading(false);
    }
  };
  return (
    <div className="app">
      <div className="container">
        <header>
          <h1>Chat with CBN</h1>
        </header>
        <div className="messages">
          {messages.map((message, index) => (
            <Message
              key={index}
              role={message.role}
              message={message.content}
              timestamp="MM/DD 00:00"
            />
          ))}
        </div>
        <div className="form">
          <input
            onChange={(e) => setInputValue(e.target.value)}
            value={inputValue}
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
