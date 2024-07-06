import React, { Component } from "react";
import SideBar from './components/SideBar';
import ChatUI from './components/AiChat';


function App() {
  return (
    <div className="flex flex-row overflow-x-hidden">
      <SideBar/>
      <ChatUI/>
    </div>
    
  );
}

export default App;
