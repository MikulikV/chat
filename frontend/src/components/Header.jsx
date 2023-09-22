import React from "react";
import IconButton from "@mui/material/IconButton";
import DeleteIcon from "@mui/icons-material/Delete";

const Header = (props) => {
  return (
    <header>
      <h1 className="title">Chat with CBN</h1>
      {props.messages.length !== 0 && (
        <div className="delete-btn">
          <IconButton
            onClick={props.clearChat}
            variant="outlined"
            color="primary"
            aria-label="Clear chat"
            sx={{ padding: 0 }}
            size="large"
            disabled={props.loading}
          >
            <DeleteIcon fontSize="inherit" />
          </IconButton>
        </div>
      )}
    </header>
  );
};

export default Header;
