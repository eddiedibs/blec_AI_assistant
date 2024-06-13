// import React from 'react';
// import ReactDOM from 'react-dom/client';
import React, { Component } from "react";
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App';

const root = createRoot(document.getElementById('app'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

