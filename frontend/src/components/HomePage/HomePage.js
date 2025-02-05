"use client";

import React, { useState, useEffect } from "react";
import HomeBanner from '../HomeBanner'
import Footer from '../Footer'
const HomePage = () => {
    const [isChatFormSubmitted, setIsChatFormSubmitted] = useState(false);

  
    return (
      <div>
        <div className="w-full h-screen flex flex-col">
            <HomeBanner/>
        </div>
        <div className="w-full h-full flex flex-col">
          <Footer/>
        </div>
      </div>

    );
  };

export default HomePage