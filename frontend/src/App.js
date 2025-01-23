import React, { Component } from "react";
import SideBar from './components/SideBar';
import ChatUI from './components/AiChat';
import { ToastContainer, Bounce } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function App() {
  return (
    <>
    <div className="flex flex-row overflow-x-hidden">
      <SideBar/>
      <ChatUI/>
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
    </>
  );
}

export default App;
