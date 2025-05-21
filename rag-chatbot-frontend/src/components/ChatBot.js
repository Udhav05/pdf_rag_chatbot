import React, { useEffect, useRef } from "react";

const ChatBot = ({ messages }) => {
  const chatEndRef = useRef(null);

  // Scroll to bottom when messages update
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div
      className="flex flex-col space-y-4 p-4 bg-white rounded-lg shadow-md h-96 overflow-y-auto"
      id="chatbox"
    >
      {messages.length === 0 && (
        <p className="text-gray-400 text-center">No messages yet. Start the chat!</p>
      )}
      {messages.map(({ sender, text }, idx) => (
        <div
          key={idx}
          className={`max-w-3/4 p-3 rounded-lg ${
            sender === "user" ? "bg-purple-600 text-white self-end" : "bg-gray-200 text-gray-900 self-start"
          }`}
        >
          <p>{text}</p>
        </div>
      ))}
      <div ref={chatEndRef} />
    </div>
  );
};

export default ChatBot;
