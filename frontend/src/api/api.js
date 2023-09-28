import axios from "axios";

export async function* getMessages(inputValue, messages) {
  const url = "http://localhost:8080/api/chat";
  let answer = "";

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
      yield "No response received. Please try again.";
    }

    let decoder = new TextDecoderStream();
    const reader = response.body.pipeThrough(decoder).getReader();

    while (true) {
      let { value, done } = await reader.read();
      if (done) {
        break;
      } else {
        answer += value;
        yield answer;
      }
    }
  } catch (error) {
    console.log(error);
    yield "An error occurred. Please try again.";
  }
}

export const getLangchainAnswer = async (inputValue) => {
  const url = "http://localhost:8080/api/langchain";
  let answer = "";

  try {
    const response = await axios.post(url, {
      user_input: inputValue,
    });
    answer = response.data;
  } catch (error) {
    console.log(error);
    answer = "An error occurred. Please try again.";
  } finally {
    return answer;
  }
};
