import { BsPlus, BsGearFill } from 'react-icons/bs';
import { FaFire, FaHandsHelping } from 'react-icons/fa';
import React from "react";

const SideBar = () => {
    // No need for state management or effect hooks for responsiveness
    return (
        <div className="top-0 left-0 h-screen w-16 m-0 flex-col bg-[#9d2a92] text-white shadow-lg md:block hidden">
            <a href='/'>
                <SideBarIcon icon={<BsPlus size="32"/>} text="Nueva solicitud"/>
            </a>
            {/* <SideBarIcon icon={<FaHandsHelping size="24"/>} text="Citas médicas"/>
            <SideBarIcon icon={<BsGearFill size="20"/>} text="Configuracion"/> */}
        </div>
    );
};

const SideBarIcon = ({ icon, text = 'tooltip'}) => (
    <div className="sidebar-icon group">
        {icon}
        <span className="sidebar-tooltip group-hover:scale-100">
            {text}
        </span>
    </div>
);

export default SideBar;
