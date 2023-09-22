import React from "react";
import Message from "./Message";

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
    </div>
  );
};

export default Conversation;
