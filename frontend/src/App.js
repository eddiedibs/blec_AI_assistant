import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SideBar from './components/SideBar';
import ChatUI from './components/AiChat';
import HomePage from './components/HomePage'; // New HomePage component
import { ToastContainer, Bounce } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function App() {
  return (
    <Router>
      <div className="flex flex-col overflow-x-hidden">
        <SideBar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/chat" element={<ChatUI />} />
        </Routes>
      </div>
      <ToastContainer
        position="bottom-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick={false}
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="colored"
        transition={Bounce}
      />
    </Router>
  );
}

export default App;
