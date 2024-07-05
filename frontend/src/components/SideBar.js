import { BsPlus, BsGearFill } from 'react-icons/bs'
import { FaFire, FaHandsHelping } from 'react-icons/fa'
import React, { Component } from "react";



const SideBar = () => {
    return (
        <div className="fixed top-0 left-0 h-screen w-16 m-0
        flex flex-col
        bg-purple-900 text-white shadow-lg">
        
        <SideBarIcon icon={<BsPlus size="32"/>} text="Nuevo chat"/>
        <SideBarIcon icon={<FaHandsHelping size="24"/>} text="Ayuda"/>
        <SideBarIcon icon={<BsGearFill size="20"/>} text="Configuracion"/>
        </div>
    );
};

const SideBarIcon = ({ icon, text = 'tooltip'}) => (
    <div className="sidebar-icon group">
        {icon}
        <span class="sidebar-tooltip group-hover:scale-100">
            {text}
        </span>
    </div>

);

export default SideBar