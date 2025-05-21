import React, { useState } from "react";

const PdfUploads = ({ onFileSelect }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadSuccess, setUploadSuccess] = useState(null); // null, true or false

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setSelectedFile(file);
    setUploadSuccess(null); // reset status

    // Inform parent component
    if (onFileSelect) {
      onFileSelect(file);
    }

    // Simulate uploading file to backend
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      setUploadSuccess(true);
    } catch (error) {
      setUploadSuccess(false);
    }
  };

  return (
    <div className="mb-6">
      <label className="block mb-2 font-semibold text-gray-700">Upload Your PDF</label>
      <input
        type="file"
        accept="application/pdf"
        onChange={handleFileChange}
        className="block mb-2"
      />
      {selectedFile && (
        <div className="mb-2">
          <strong>Selected:</strong> {selectedFile.name}
        </div>
      )}
      {uploadSuccess === true && (
        <div className="text-green-600 font-medium">
          ✅ PDF "{selectedFile?.name}" uploaded! You can now ask questions.
        </div>
      )}
      {uploadSuccess === false && (
        <div className="text-red-600 font-medium">
          ❌ Failed to upload PDF to backend.
        </div>
      )}
    </div>
  );
};

export default PdfUploads;
