import React from "react";
import Avatar from "@mui/material/Avatar";
import user_logo from "../assets/img/user.png";
import cbn_logo from "../assets/img/favicon.ico";

const Message = (props) => {
  return (
    <div className={props.role}>
      {props.role === "assistant" ? (
        <div className="avatar">
          <Avatar alt="CBN Assistant" src={cbn_logo}>
            CA
          </Avatar>
        </div>
      ) : (
        ""
      )}
      <div className="message">
        <p>{props.message}</p>
        <div className="timestamp">{props.timestamp}</div>
      </div>
      {props.role === "user" ? (
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
