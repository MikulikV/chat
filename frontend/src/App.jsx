import React from "react";
import { useState } from "react";
import { getLangchainAnswer, getMessages } from "./api/api";
import Header from "./components/Header";
import UserInput from "./components/UserInput";
import Conversation from "./components/Conversation";

const App = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [model, setModel] = useState("OpenAI");

  const handleSubmit = async (inputValue) => {
    setLoading(true);
    if (model === "OpenAI") {
      await getMessages(inputValue, messages, setMessages);
    } else if (model === "Langchain") {
      await getLangchainAnswer(inputValue, messages, setMessages);
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
