import React from "react";
import Avatar from "@mui/material/Avatar";
import user_logo from "../assets/img/user.png";
import cbn_logo from "../assets/img/favicon.ico";

const Message = (props) => {
  const message = props.message;
  const timestamp = props.timestamp ? props.timestamp : "";
  const role = props.role;
  return (
    <div className={role}>
      {role === "assistant" ? (
        <div className="avatar">
          <Avatar alt="CBN Assistant" src={cbn_logo}>
            CA
          </Avatar>
        </div>
      ) : (
        ""
      )}
      <div className="message">
        <p>{message}</p>
        <div className="timestamp">{timestamp}</div>
      </div>
      {role === "user" ? (
        <div className="avatar">
          <Avatar alt="You" src={user_logo}>
            U
          </Avatar>
        </div>
      ) : (
        ""
      )}
    </div>
  );
};

export default Message;
