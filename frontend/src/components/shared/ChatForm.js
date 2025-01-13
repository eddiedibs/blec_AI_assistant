import React, { useState, useEffect } from 'react';
import axios from "axios";

const ChatForm = ({ onSubmit }) => {
    const [options, setOptions] = useState([]);
    const [selectedOption, setSelectedOption] = useState("");
  
    // Fetch options from Django API on component mount
    useEffect(() => {
      axios
        .get("api/doctors") // Replace with your Django endpoint
        .then((response) => {
            console.log(response.data);
          setOptions(response.data); // Assume response contains an array of prefixes
        })
        .catch((error) => {
          console.error("Error fetching options:", error);
        });
    }, []);
  
    // Handle selection change
    const handleChange = (event) => {
      setSelectedOption(event.target.value);
      console.log("Selected:", event.target.value); // Use this value as needed
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(); // Notify parent component
    };

return (
  <div className="w-full h-full flex flex-col justify-end bg-white p-6 rounded-lg">
    <form onSubmit={handleSubmit}>
        <div class="grid gap-6 mb-2 md:grid-cols-2">
            <div>
                <label for="first_name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Nombre</label>
                <input type="text" id="first_name" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Coloca tu nombre" required />
            </div>
            <div>
                <label for="last_name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Apellido</label>
                <input type="text" id="last_name" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Coloca tu apellido" required />
            </div>
        </div>
        <div class="grid gap-6 mb-2 md:grid-cols-2">
            <div class="mb-2">
                <label for="id_number" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Cédula de identidad</label>
                <input type="id_number" id="id_number" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="eg. 11254879" required />
            </div> 
            <div class="mb-2">
                <label for="phone_number" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Número telefónico</label>
                <input type="phone_number" id="phone_number" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="eg. 042412345678" required />
            </div> 
        </div>
        
        <div class="mb-2">
            <label for="doctor" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Doctor a agendar</label>
            <select class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" value={selectedOption} onChange={handleChange}>
                <option value="" disabled>
                    Selecciona un doctor
                </option>
                {options.map((option) => (
                    <option key={option.value} value={option.value}>
                    {option.name}
                    </option>
                ))}
            </select>
            {/* <input type="doctor" id="doctor" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="eg. 042412345678" required /> */}
        </div>
        
        <div class="mb-2">
            <label for="appointment_reason" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Razón de la cita</label>
            <input type="appointment_reason" id="appointment_reason" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="eg. Malestar general" required />
        </div> 
        {/* <div class="flex items-start mb-2">
            <div class="flex items-center h-5">
            <input id="remember" type="checkbox" value="" class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800" required />
            </div>
            <label for="remember" class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">I agree with the <a href="#" class="text-blue-600 hover:underline dark:text-blue-500">terms and conditions</a>.</label>
        </div> */}
        <button type="submit" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Submit</button>
    </form>
  </div>
);
};

export default ChatForm;
