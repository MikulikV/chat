import React from "react";
import { useState } from "react";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import SendIcon from "@mui/icons-material/Send";

const UserInput = (props) => {
  const [inputValue, setInputValue] = useState("");

  const sendMessage = (e) => {
    e.preventDefault();
    props.handleSubmit(inputValue);
    setInputValue("");
  };

  return (
    <div className="user-input">
      <TextField
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && inputValue !== "") {
            sendMessage(e);
          }
        }}
        id="outlined-multiline-flexible"
        label="Send a message"
        multiline
        maxRows={4}
        className="input"
      />
      <Button
        onClick={(e) => {
          sendMessage(e);
        }}
        variant="contained"
        color="primary"
        disabled={inputValue === "" || props.loading}
      >
        <SendIcon />
      </Button>
    </div>
  );
};

export default UserInput;
