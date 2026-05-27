import React, { useEffect, useRef, useState } from "react";

const ChatBot = ({ messages }) => {
  const chatEndRef = useRef(null);
  const [typingIndex, setTypingIndex] = useState(null);

  // Auto scroll
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, typingIndex]);

  // Simulate "AI typing effect"
  useEffect(() => {
    if (messages.length > 0 && messages[messages.length - 1].sender === "bot") {
      setTypingIndex(messages.length - 1);
      const timer = setTimeout(() => setTypingIndex(null), 800);
      return () => clearTimeout(timer);
    }
  }, [messages]);

  return (
    <div className="flex flex-col h-96 bg-gradient-to-b from-white to-gray-50 rounded-xl shadow-lg overflow-y-auto p-4 space-y-3">
      
      {/* Header */}
      <div className="text-center text-sm text-gray-500 mb-2">
        💬 AI RAG Chat Assistant
      </div>

      {/* Messages */}
      {messages.length === 0 && (
        <div className="flex justify-center items-center h-full text-gray-400">
          Start chatting with your document...
        </div>
      )}

      {messages.map((msg, idx) => {
        const isUser = msg.sender === "user";
        const isTyping = idx === typingIndex;

        return (
          <div
            key={idx}
            className={`flex ${isUser ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`relative max-w-[75%] px-4 py-2 rounded-2xl shadow-sm text-sm transition-all duration-300 ${
                isUser
                  ? "bg-purple-600 text-white rounded-br-sm"
                  : "bg-gray-200 text-gray-800 rounded-bl-sm"
              }`}
            >
              <p>
                {msg.text}
                {isTyping && (
                  <span className="ml-2 animate-pulse">...</span>
                )}
              </p>

              {/* Timestamp */}
              <div className="text-[10px] mt-1 opacity-60 text-right">
                {msg.time || ""}
              </div>
            </div>
          </div>
        );
      })}

      {/* Typing indicator */}
      {typingIndex !== null && (
        <div className="text-xs text-gray-400 animate-pulse">
          AI is thinking...
        </div>
      )}

      <div ref={chatEndRef} />
    </div>
  );
};

export default ChatBot;