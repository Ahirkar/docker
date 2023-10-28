import { isEmpty } from "ramda";
import "./chatBot.css";
import { useEffect, useState, useRef } from "react";
import { IoMdSend } from "react-icons/io";

function Basic() {
  const [chat, setChat] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [botTyping, setbotTyping] = useState(false);
  const videoRef = useRef();
  const mediaRecorderRef = useRef(null);
  const [isRecording, setIsRecording] = useState(false);

  const startRecording = () => {
    const stream = videoRef.current.srcObject;
    mediaRecorderRef.current = new MediaRecorder(stream);
    mediaRecorderRef.current.start();
    setIsRecording(true);
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    setIsRecording(false);
  };

  const handleDataAvailable = (event) => {
    const videoBlob = new Blob([event.data], { type: "video/mp4" });
    const audioBlob = new Blob([event.data], { type: "audio/mpeg" });
    const videoUrl = URL.createObjectURL(videoBlob);
    // Do something with the recorded video URL, such as save it to state
    console.log("video url", videoUrl, videoBlob, event.data, audioBlob);
  };

  const handleStartClick = () => {
    if (videoRef.current) {
      startRecording();
      mediaRecorderRef.current.addEventListener(
        "dataavailable",
        handleDataAvailable
      );
    }
  };

  const handleStopClick = () => {
    if (mediaRecorderRef.current && isRecording) {
      stopRecording();
      mediaRecorderRef.current.removeEventListener(
        "dataavailable",
        handleDataAvailable
      );
    }
  };

  useEffect(() => {
    const constraints = { audio: false, video: true };
    navigator.mediaDevices
      .getUserMedia(constraints)
      .then((stream) => {
        videoRef.current.srcObject = stream;
      })
      .catch();
  }, []); //"Hi Welcome to our vKYC platform, How may I assist you."

  useEffect(() => {
    const objDiv = document.getElementById("messageArea");
    objDiv.scrollTop = objDiv.scrollHeight;
    console.log("chat", chat);
    if (isEmpty(chat)) {
      const name = "no name";
      const request_temp = {
        sender: "bot",
        sender_id: name,
        msg: "Hi Welcome to our vKYC platform, How may I assist you.",
      };
      setChat([request_temp]);
    }
  }, [chat]);

  const handleSubmit = (evt) => {
    evt.preventDefault();
    const name = "no name";
    const request_temp = { sender: "user", sender_id: name, msg: inputMessage };

    if (inputMessage !== "") {
      setChat((chat) => [...chat, request_temp]);
      setbotTyping(true);
      setInputMessage("");
      rasaAPI(name, inputMessage);
    } else {
      window.alert("Please enter valid message");
    }
  };

  const rasaAPI = async function handleClick(name, msg) {
    await fetch("http://172.27.22.51:5005/webhooks/rest/webhook", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        charset: "UTF-8",
      },
      credentials: "same-origin",
      body: JSON.stringify({ sender: name, message: msg }),
    })
      .then((response) => response.json())
      .then((response) => {
        if (response) {
          console.log('response',response)
          const response_temp = response.map((temp) => {
            const recipient_id = temp["recipient_id"];
            const recipient_msg = temp["text"];

            return {
              sender: "bot",
              recipient_id: recipient_id,
              msg: recipient_msg,
            };
          });

          setbotTyping(false);
          setChat((chat) => [...chat, ...response_temp]);
        }
      });
  };

  return (
    <div className="page">
      <div className="video-section" >
        <video style={{height:'900px'}} ref={videoRef} autoPlay muted />
      </div>
      <div>
        {!isRecording ? (
          <button onClick={handleStartClick}>Start Recording</button>
        ) : (
          <button onClick={handleStopClick}>Stop Recording</button>
        )}
      </div>
      <div className="box">
        <div className="card">
          <div className="cardHeader">
            <div className="cardHeaderTitle">Chatbot</div>
            {botTyping ? <h6>Bot Typing....</h6> : null}
          </div>
          <div className="cardBody" id="messageArea">
            <div className="row msgarea">
              {chat
                .map((user, key) => (
                  <div key={key}>
                    {user.sender === "user" ? (
                      <div className="msgalignstart">
                        <h5 className="usermsg">{user.msg}</h5>
                        <img
                          className="userIcon"
                          src={require("./userAvatar.jpg")}
                          alt="User avatar"
                        />
                      </div>
                    ) : (
                      <div className="msgalignend">
                        <img
                          className="botIcon"
                          src={require("./images.png")}
                          alt="Bot avatar"
                          style={{ width: "50px", height: "50px" }}
                        />
                        <h5 className="botmsg">{user.msg}</h5>
                      </div>
                    )}
                  </div>
                ))
                .reverse()}
            </div>
          </div>
          <div className="cardFooter text-white footer-style">
            <div className="footerRow">
              <form className="form-style" onSubmit={handleSubmit}>
                <input
                  onChange={(e) => setInputMessage(e.target.value)}
                  value={inputMessage}
                  type="text"
                  className="msginp"
                ></input>
                <button type="submit" className="circleBtn">
                  <IoMdSend className="sendBtn" />
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Basic;
