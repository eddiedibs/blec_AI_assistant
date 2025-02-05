"use client";

import React, { useState, useEffect } from "react";
import { Carousel } from "flowbite-react";
import { motion } from "framer-motion";
import { Link } from 'react-router-dom';

const HomeBanner = () => {
    const formVariants = {
        hidden: { opacity: 0, y: 50 },
        visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
      };

    return (
      <div className="w-full h-screen flex flex-row justify-center content-center items-center bg-[#0290cc]">
        <motion.div
          variants={formVariants}
          initial="hidden"
          animate="visible"
        >
            <div className="flex flex-col justify-center content-center items-center gap-8 z-10 px-52">
                <span className="text-white font-montserrat text-2xl">¡Cuidamos la salud de los más pequeños de la casa!</span>
                <h1 className="text-white font-bold font-montserrat text-4xl">¡Más vida ✨ + salud 🏥!</h1>
                <span className="text-white font-montserrat text-2xl">En Kidsalud, nuestra prioridad es la salud 🩺 y felicidad 😊 de cada niño 👶, ofreciendo un entorno seguro 🏡, cálido ❤️ y lleno de confianza 🤝 para ellos y sus familias 👨‍👩‍👧‍👦.</span>
                <Link to="/chat" className="text-white bg-[#39a142] transition-colors duration-500 ease-in-out hover:bg-white hover:text-[#39a142] focus:ring-4 focus:outline-none focus:ring-[#39a142] font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center">
                    ¡Agenda tu cita!
                </Link>

            </div>


        </motion.div>

        <Carousel slideInterval={3000} pauseOnHover className="w-full h-full">
          <img className="h-screen object-cover" src="/media/kidsalud_banner_img1.jpg" alt="..." />
          <img className="h-screen object-cover" src="/media/kidsalud_banner_img2.jpg" alt="..." />
          <img className="h-screen object-cover" src="/media/kidsalud_banner_img3.jpg" alt="..." />
        </Carousel>


      </div>
    );
  };

export default HomeBanner