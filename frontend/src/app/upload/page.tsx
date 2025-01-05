"use client";
import React, { useState } from "react";
import ChatBox from "../components/ChatBox";
import { IoIosArrowBack } from "react-icons/io";
import { useRouter } from "next/navigation";

const UploadPage: React.FC = () => {
  const router = useRouter();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [messages, setMessages] = useState<
    { sender: string; text: string }[]
  >([]);
  const [fetching, setFetching] = useState(false);
  const [modelSelection, setModelSelection] = useState("default-model");
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
      setError(null);
    }
  };

  const handleFileUpload = async () => {
    if (selectedFile) {
      try {
        setSubmitted(true);
        const formData = new FormData();
        formData.append("file", selectedFile);

        const response = await fetch(
          `${process.env.NEXT_PUBLIC_BACKEND_URL}/upload`,
          {
            method: "POST",
            body: formData,
          }
        );

        if (!response.ok) {
          throw new Error("File upload failed");
        }

        const result = await response.json();
        alert("File uploaded successfully!");
        console.log("File uploaded successfully:", result);
      } catch (error) {
        console.error("Error uploading file:", error);
        setError("File upload failed.");
      } finally {
        setSubmitted(false);
      }
    } else {
      setError("Please select a file to upload.");
    }
  };

  const handleSendMessage = async (message: string) => {
    setFetching(true);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/chat`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message, model: modelSelection }),
        }
      );

      if (!response.ok) {
        throw new Error("Error fetching response from the server");
      }

      const data = await response.json();
      setMessages((prev) => [
        ...prev,
        { sender: "user", text: message },
        { sender: "bot", text: data.response },
      ]);
    } catch (error) {
      console.error("Error sending message:", error);
    } finally {
      setFetching(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white">
      <div className="flex items-center mt-3 ml-2">
        <IoIosArrowBack
          className="text-white text-3xl cursor-pointer"
          onClick={() => router.push("/")}
        />
        <div className="ml-3">
          <h1 className="text-5xl bg-gradient-to-r from-violet-500 to-pink-500 inline-block text-transparent bg-clip-text">
            AURA
          </h1>
          <p className="text-sm mt-2 italic text-gray-300">
            <span className="text-pink-500 text-lg">A</span>nalytics and{" "}
            <span className="text-pink-500 text-lg">U</span>nderstanding for{" "}
            <span className="text-pink-500 text-lg">R</span>esponsible{" "}
            <span className="text-pink-500 text-lg">A</span>I
          </p>
        </div>
      </div>

      <div className="w-full max-w-4xl mx-auto py-8 px-6">
        <p className="mt-6 text-gray-300">
          Welcome to the Upload Page! Here, you can upload your documents to get started with our chat feature. 
          Please upload a file in one of the following formats: PDF, TXT, or CSV. Once uploaded, our platform 
          will process the document and enable you to interact with the content through our chat interface. 
          This feature allows you to ask questions and receive information based on the uploaded document.
        </p>

        <form
          className="mt-10 space-y-6"
          onSubmit={(e) => e.preventDefault()}
        >
          <div className="relative">
            <label className="block text-lg font-semibold mb-2">
              Upload File
            </label>
            <input
              type="file"
              accept=".pdf,.txt,.csv"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-500 file:text-white hover:file:bg-violet-600 focus:outline-none"
              required
            />
            {error && (
              <p className="text-red-400 mt-2 text-sm">{error}</p>
            )}
          </div>

          <div className="flex justify-center">
            <button
              type="button"
              onClick={handleFileUpload}
              className={`py-3 px-6 text-lg font-bold rounded-lg shadow-md ${
                submitted
                  ? "bg-gray-500 cursor-not-allowed"
                  : "bg-gradient-to-r from-violet-500 to-pink-500 hover:from-violet-600 hover:to-pink-600"
              } text-white`}
              disabled={submitted}
            >
              {submitted ? "Uploading..." : "Upload File"}
            </button>
          </div>
        </form>

        <div className="mt-10">
          <h2 className="text-xl font-semibold mb-4">Chat Feature</h2>
          <ChatBox
            messages={messages}
            onSend={handleSendMessage}
            model="default-model"
            otherModels={["default-model", "alternative-model"]}
            historyId={null}
            user={{
              id: "user-id",
              avatar: "/avatar.png",
              name: "User Name",
              email: "user@example.com",
            }}
            fetching={fetching}
            modelSelection={modelSelection}
            setModelSelection={setModelSelection}
          />
        </div>
      </div>
    </div>
  );
};

export default UploadPage;