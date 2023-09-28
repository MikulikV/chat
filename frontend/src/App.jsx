import React from "react";
import Header from "./components/Header";
import UserInput from "./components/UserInput";
import Conversation from "./components/Conversation";
import { useState } from "react";
import { getLangchainAnswer, getMessages } from "./api/api";
import { getTimeStamp } from "./utils/dateUtils";

const App = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [model, setModel] = useState("OpenAI");

  const handleSubmit = async (inputValue) => {
    const userTimestamp = getTimeStamp();
    const userMessage = {
      role: "user",
      content: inputValue,
      timestamp: userTimestamp,
    };
    setMessages([...messages, userMessage]);
    setLoading(true);
    if (model === "OpenAI") {
      for await (const message of getMessages(inputValue, messages)) {
        const timestamp = getTimeStamp();
        setMessages([
          ...messages,
          userMessage,
          { role: "assistant", content: message, timestamp: timestamp },
        ]);
      }
    } else if (model === "Langchain") {
      let answer = await getLangchainAnswer(inputValue, messages, setMessages);
      const timestamp = getTimeStamp();
      setMessages([
        ...messages,
        userMessage,
        { role: "assistant", content: answer, timestamp: timestamp },
      ]);
    }
    setLoading(false);
  };

  const clearChat = () => {
    setMessages([]);
  };

  const changeModel = (model) => {
    setModel(model);
    clearChat();
  };

  return (
    <div className="app">
      <div className="container">
        <Header
          messages={messages}
          loading={loading}
          clearChat={clearChat}
          model={model}
          changeModel={changeModel}
        />
        <Conversation messages={messages} />
        <UserInput handleSubmit={handleSubmit} loading={loading} />
      </div>
    </div>
  );
};

export default App;
