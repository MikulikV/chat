import React from "react";
import { useState } from "react";
import { getMessages } from "./api/api";
import Header from "./components/Header";
import UserInput from "./components/UserInput";
import Conversation from "./components/Conversation";

const App = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (inputValue) => {
    await getMessages(inputValue, messages, setMessages, setLoading);
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="app">
      <div className="container">
        <Header messages={messages} loading={loading} clearChat={clearChat} />
        <Conversation messages={messages} />
        <UserInput handleSubmit={handleSubmit} loading={loading} />
      </div>
    </div>
  );
};

export default App;
