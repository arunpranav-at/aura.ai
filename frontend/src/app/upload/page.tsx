"use client";
import React, { useState, useEffect } from "react";
import ChatBox from "../components/ChatBox";
import DocumentCell from "../components/Document";
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
  const [loggedIn, setLoggedIn] = useState(false);
  const [user, setUser] = useState<any | null>(null);
  const [documentFetching, setDocumentFetching] = useState<boolean>(true);
  interface Document {
    id: string;
    filename: string;
    file_path: string;
    rag_path: string;
  }

  const [documents, setDocuments] = useState<Document[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Check if the user is authenticated by validating the JWT in the cookies
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_BACKEND_URL}/token/validate`,
          {
            method: "GET",
            credentials: "include", // Include cookies in the request
          }
        );

        if (response.ok) {
          const data = await response.json();
          setLoggedIn(true);
          setUser(data.user);
          const documents_response = await fetch(
            `${process.env.NEXT_PUBLIC_BACKEND_URL}/rag/documents`,
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              credentials: "include", // Include cookies in the request
              body: JSON.stringify({ username: data.user.name || "" }),
            }
          );
          if (documents_response.ok) {
            const documents_data = await documents_response.json();
            setDocuments(documents_data.documents);
            setDocumentFetching(false);
          } else {
            console.log("Error fetching documents:", documents_response);
          }
        } else {
          router.push("/")
          setLoggedIn(false);
        }
      } catch (error) {
        console.log("Error validating token:", error);
        setLoggedIn(false);
      }
    };

    fetchData();
  }, []);

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
        formData.append("username", localStorage.getItem("username") || "");

        const response = await fetch(
          `${process.env.NEXT_PUBLIC_BACKEND_URL}/rag/upload/document`,
          {
            method: "POST",
            body: formData
          }
        );

        if (!response.ok) {
          throw new Error("File upload failed");
        }

        const result = await response.json();
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
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/rag/response`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ username: localStorage.getItem("username") || "", query: message }),
        }
      );

      if (!response.ok) {
        throw new Error("Error fetching response from the server");
      }

      const data = await response.json();
      setMessages((prev) => [
        ...prev,
        { sender: "user", text: message },
        { sender: "bot", text: data.bot_response },
      ]);
    } catch (error) {
      console.error("Error sending message:", error);
    } finally {
      setFetching(false);
    }
  };

  return (
    <div className="grid grid-cols-6 bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white">
      <div className="flex flex-col min-h-screen bg-slate-900 text-white">
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
        <p className="text-lg mt-2 ml-4 text-gray-300">Your Documents</p>
        {!documentFetching && documents.map((doc) => <DocumentCell key={doc.id} id={doc.id} filename={doc.filename} file_path={doc.file_path} rag_path={doc.rag_path} />)}
      </div>
      <div className="flex col-start-2 col-span-5 flex-col min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white">
        <div className="w-full max-w-4xl mx-auto py-8 px-6">
          <p className="mt-6 text-gray-300">
            Welcome to the Upload Page! Here, you can upload your documents to get started with our chat feature. 
            Please upload a file in one of the following formats: PDF or text files. Once uploaded, our platform 
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
                accept=".pdf,.txt"
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
              user={user}
              fetching={fetching}
              modelSelection={modelSelection}
              setModelSelection={setModelSelection}
            />
          </div>
        </div>
      </div>

    </div>
  );
};

export default UploadPage;