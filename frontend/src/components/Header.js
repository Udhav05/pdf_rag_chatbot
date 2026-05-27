import React from "react";

const Header = () => {
  return (
    <header className="bg-gradient-to-r from-purple-700 to-pink-600 text-white shadow-md py-4 px-6">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <h1 className="text-2xl font-bold">📄 RAG PDF Chatbot</h1>
        <nav>
          <ul className="flex space-x-4">
            <li>
              <a href="/" className="hover:underline">
                Home
              </a>
            </li>
            <li>
              <a href="#upload" className="hover:underline">
                Upload
              </a>
            </li>
            <li>
              <a href="#chat" className="hover:underline">
                Chat
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
