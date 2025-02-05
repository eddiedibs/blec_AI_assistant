import { BsPlus, BsGearFill } from 'react-icons/bs';
import { FaHome } from "react-icons/fa";
import KidsaludIcon from './shared/KidsaludIcon';
import { Link } from 'react-router-dom';

import React from "react";

const SideBar = () => {
    // No need for state management or effect hooks for responsiveness
    return (
        <div className="fixed top-0 left-0 w-screen h-[80px] p-1 m-0 flex flex-row gap-8 justify-end items-center bg-[#3fae48] text-white shadow-lg overflow-hidden z-10">
            <KidsaludIcon width='278' height='73' style={{borderRadius: '50px', marginRight: 'auto'}}/>
            <Link to="/chat">
                <SideBarIcon icon={<BsPlus size="32"/>} text="Nueva solicitud"/>
            </Link>
            <Link to="/" style={{marginRight: '2%'}}>
                <SideBarIcon icon={<FaHome size="28"/>} text="Inicio"/>
            </Link>
            
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
