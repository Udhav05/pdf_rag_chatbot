import React, { useState, useEffect } from "react";
import Header from "../components/Header";
import PdfUploads from "../components/PdfUploads";
import ChatBot from "../components/ChatBot";
import QueryInput from "../components/QueryInput";

const Home = () => {
  const [messages, setMessages] = useState([]);
  const [pdfFile, setPdfFile] = useState(null);

  // 🧾 Handle file upload
  const handleFileSelect = (file) => {
    setPdfFile(file);
    setMessages((prev) => [
      ...prev,
      { sender: "bot", text: `✅ PDF "${file.name}" uploaded! You can now ask questions.` }
    ]);
  };

  // 💬 Handle user query input
  const handleQuerySubmit = async (query) => {
    if (!pdfFile) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "❗ Please upload a PDF first." }
      ]);
      return;
    }

    setMessages((prev) => [...prev, { sender: "user", text: query }]);

    try {
      // Example: Call backend API (replace with your actual API)
      const response = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          question: query,
          filename: pdfFile.name
        })
      });

      const data = await response.json();
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: data.answer || "No answer received from backend." }
      ]);
    } catch (error) {
      console.error("Error querying backend:", error);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "❌ Failed to get a response from the backend." }
      ]);
    }
  };

  // 📤 Send the PDF to the backend when selected
  useEffect(() => {
    if (pdfFile) {
      const uploadPDF = async () => {
        const formData = new FormData();
        formData.append("file", pdfFile);

        try {
          const response = await fetch("http://localhost:8000/upload", {
            method: "POST",
            body: formData
          });

          const result = await response.json();
          console.log("PDF uploaded:", result);
        } catch (err) {
          console.error("PDF upload failed:", err);
          setMessages((prev) => [
            ...prev,
            { sender: "bot", text: "❌ Failed to upload PDF to backend." }
          ]);
        }
      };

      uploadPDF();
    }
  }, [pdfFile]);

  return (
    <div className="max-w-3xl mx-auto p-6 min-h-screen bg-gradient-to-b from-purple-100 to-purple-50">
      <Header />
      <PdfUploads onFileSelect={handleFileSelect} />
      <ChatBot messages={messages} />
      <QueryInput onSubmit={handleQuerySubmit} />
    </div>
  );
};

export default Home;
