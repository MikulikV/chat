import React from "react";
import Message from "./components/Message";
import Button from "@mui/material/Button";
import SendIcon from "@mui/icons-material/Send";
import { useState } from "react";
// import axios from "axios";

const App = () => {
  const [inputValue, setInputValue] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setInputValue("");
    const url = "http://localhost:8080/api/chat";
    let currentAnswer = "";

    // Timestamp
    const currentDate = new Date();
    const MM = String(currentDate.getMonth() + 1).padStart(2, "0");
    const DD = String(currentDate.getDate()).padStart(2, "0");
    const HH = currentDate.getHours();
    const ampm = HH >= 12 ? "PM" : "AM";
    const H =
      HH > 12 ? String(HH - 12).padStart(2, "0") : String(HH).padStart(2, "0");
    const M = String(currentDate.getMinutes()).padStart(2, "0");
    const timestamp = `${MM}/${DD} ${H}:${M} ${ampm}`;

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

      let decoder = new TextDecoderStream();
      if (!response.body) {
        setMessages([
          ...messages,
          { role: "user", content: inputValue, timestamp: timestamp },
          {
            role: "assistant",
            content: "No response received. Please try again.",
            timestamp: timestamp,
          },
        ]);
        return;
      }

      const reader = response.body.pipeThrough(decoder).getReader();

      while (true) {
        let { value, done } = await reader.read();

        if (done) {
          break;
        } else {
          currentAnswer += value;
          setMessages([
            ...messages,
            { role: "user", content: inputValue, timestamp: timestamp },
            { role: "assistant", content: currentAnswer, timestamp: timestamp },
          ]);
        }
      }
    } catch (error) {
      console.log(error);
      setMessages([
        ...messages,
        { role: "user", content: inputValue, timestamp: timestamp },
        {
          role: "assistant",
          content: "An error occurred. Please try again.",
          timestamp: timestamp,
        },
      ]);
    } finally {
      setLoading(false);
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
              timestamp={message.timestamp}
            />
          ))}
        </div>
        <div className="form">
          <input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && inputValue !== "") {
                handleSubmit(e);
              }
            }}
            type="text"
            placeholder="Send a message"
          />
          <Button
            onClick={handleSubmit}
            variant="contained"
            color="primary"
            className="button"
            disabled={inputValue === "" || loading}
          >
            <SendIcon />
          </Button>
        </div>
      </div>
    </div>
  );
};

export default App;
