import React from "react";
import Message from "./Message";
import LinearProgress from "@mui/material/LinearProgress";

const Conversation = (props) => {
  return (
    <div className="messages">
      {props.messages.map((message, index) => (
        <Message
          key={index}
          role={message.role}
          message={message.content}
          timestamp={message.timestamp}
        />
      ))}
      {props.loading && (
        <div className="loading-bar">
          <LinearProgress />
        </div>
      )}
    </div>
  );
};

export default Conversation;
