interface Document {
  id: string;
  filename: string;
  file_path: string;
  rag_path: string;
}

const DocumentCell: React.FC<Document> = (doc: Document) => {
  const { id, filename, file_path, rag_path } = doc;

  const handleDownload = () => {
    // Trigger the file download
    const link = document.createElement("a");
    link.href = file_path; // Use the file_path to download the file
    link.download = filename; // Set the file name to be used for download
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div
      className="flex items-center m-4 p-1 bg-slate-800 border-2 border-slate-800 rounded-lg cursor-pointer transition duration-300"
      onClick={handleDownload}
    >
      {/* File Icon */}
      <div className="w-8 h-8 flex items-center justify-center rounded-full mr-1">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-file"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/></svg>
      </div>

      {/* File Name */}
      <span className="flex-1 text-slate-50 text-xs font-xs truncate">
        {filename}
      </span>
    </div>
  );
};

export default DocumentCell;
