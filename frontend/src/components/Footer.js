import React from "react";


const Footer = () => {
    return (
      <footer className="bg-[#39a142] text-white py-6">
        <div className="container mx-auto px-6 flex flex-col md:flex-row justify-between items-center">
          {/* Left Section */}
          <div className="text-center md:text-left">
            <h3 className="font-bold text-xl mb-2">Kidsalud</h3>
            <p className="text-sm">
              Cuidamos la salud de los más pequeños de la casa con amor y confianza.
            </p>
          </div>
  
          {/* Middle Section - Links */}
          <div className="mt-4 md:mt-0">
            <h4 className="font-semibold text-lg mb-2">Enlaces</h4>
            <ul className="text-sm space-y-2">
              <li><a href="/" className="hover:text-[#3fae48]">Inicio</a></li>
              {/* <li><a href="/#about" className="hover:text-[#3fae48]">Acerca de</a></li>
              <li><a href="/#services" className="hover:text-[#3fae48]">Servicios</a></li> */}
              <li><a href="/chat" className="hover:text-[#3fae48]">Agenda tu cita</a></li>
            </ul>
          </div>
  
          {/* Right Section - Social Media */}
          <div className="mt-4 md:mt-0">
            {/* <h4 className="font-semibold text-lg mb-2">Síguenos</h4> */}
            <div className="flex space-x-4">
              <a href="https://www.facebook.com" target="_blank" rel="noopener noreferrer" className="hover:text-[#3fae48]">
                <i className="fab fa-facebook-f"></i>
              </a>
              <a href="https://www.twitter.com" target="_blank" rel="noopener noreferrer" className="hover:text-[#3fae48]">
                <i className="fab fa-twitter"></i>
              </a>
              <a href="https://www.instagram.com" target="_blank" rel="noopener noreferrer" className="hover:text-[#3fae48]">
                <i className="fab fa-instagram"></i>
              </a>
            </div>
          </div>
        </div>
  
        {/* Bottom Section */}
        <div className="bg-[#2f8d3f] py-4 mt-6">
          <p className="text-center text-xs">
            &copy; {new Date().getFullYear()} Kidsalud. Todos los derechos reservados.
          </p>
        </div>
      </footer>
    );
  };
  
  export default Footer;
  