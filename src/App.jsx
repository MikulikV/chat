import React from "react";
import Message from "./components/Message";
import Button from "@mui/material/Button";
import SendIcon from "@mui/icons-material/Send";

const App = () => {
  return (
    <div className="app">
      <div className="container">
        <h1>Chat with CBN</h1>
        <div className="messages">
          <Message
            message="Hello, I'm here to help you with everything you need. Don't shy and ask any questions"
            timestamp="MM/DD 00:00"
            role="gpt"
          />
          <Message
            message="What is 2 + 2 ? and How are you? heydffffffffffff dffffffffff dffffff"
            timestamp="MM/DD 00:00"
            role="user"
          />
        </div>
        <div className="form">
          <input type="text" placeholder="Send a message" />
          <Button variant="contained" color="primary" className="button">
            <SendIcon />
          </Button>
        </div>
      </div>
    </div>
  );
};

export default App;
