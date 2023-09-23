import React from "react";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import IconButton from "@mui/material/IconButton";
import DeleteIcon from "@mui/icons-material/Delete";

const Header = (props) => {
  const handleChange = (e) => {
    props.changeModel(e.target.value);
  };

  return (
    <header>
      <h1 className="title">Chat with CBN</h1>
      <div className="btn-group">
        <FormControl>
          <Select
            value={props.model}
            onChange={handleChange}
            defaultValue="OpenAI"
            sx={{ fontSize: "12px" }}
            autoWidth
            disabled={props.loading}
          >
            <MenuItem value={"OpenAI"} sx={{ fontSize: "12px" }}>
              OpenAI
            </MenuItem>
            <MenuItem value={"Langchain"} sx={{ fontSize: "12px" }}>
              Langchain
            </MenuItem>
          </Select>
        </FormControl>
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
      </div>
    </header>
  );
};

export default Header;
