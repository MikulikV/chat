import { getTimeStamp } from "../utils/dateUtils";
import axios from "axios";

export const getMessages = async (inputValue, messages, setMessages) => {
  const url = "http://localhost:8080/api/retrieval";
  let currentAnswer = "";
  const timestamp = getTimeStamp();

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_input: inputValue,
        conversation: messages,
      }),
    });

    if (!response.body) {
      setMessages([
        ...messages,
        { role: "user", content: inputValue, timestamp: timestamp },
        {
          role: "assistant",
          content: "No response received. Please try again.",
          timestamp: timestamp,
        },
      ]);
      return;
    }

    let decoder = new TextDecoderStream();
    const reader = response.body.pipeThrough(decoder).getReader();

    while (true) {
      let { value, done } = await reader.read();

      if (done) {
        break;
      } else {
        currentAnswer += value;
        setMessages([
          ...messages,
          { role: "user", content: inputValue, timestamp: timestamp },
          { role: "assistant", content: currentAnswer, timestamp: timestamp },
        ]);
      }
    }
  } catch (error) {
    console.log(error);
    setMessages([
      ...messages,
      { role: "user", content: inputValue, timestamp: timestamp },
      {
        role: "assistant",
        content: "An error occurred. Please try again.",
        timestamp: timestamp,
      },
    ]);
  }
};

export const getLangchainAnswer = async (inputValue, messages, setMessages) => {
  const url = "http://localhost:8080/api/langchain";
  let answer = "";
  const timestamp = getTimeStamp();

  try {
    const response = await axios.post(url, {
      user_input: inputValue,
    });

    answer = response.data;
  } catch (error) {
    console.log(error);
    answer = "An error occurred. Please try again.";
  } finally {
    setMessages([
      ...messages,
      { role: "user", content: inputValue, timestamp: timestamp },
      { role: "assistant", content: answer, timestamp: timestamp },
    ]);
  }
};
