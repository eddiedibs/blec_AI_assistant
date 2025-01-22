
"use client"
import React, { useState, useEffect } from 'react';
import axios from "axios";
import { Datepicker, Spinner  } from "flowbite-react";
import { CustomFlowbiteTheme } from "flowbite-react";

const ChatForm = ({ onSubmit }) => {
    const [options, setOptions] = useState([]);
    const today = new Date(); // Example: "2025-01-18"
    // Initialize state with today's date
    const [selectedBirthDate, setSelectedBirthDate] = useState(today);    
    const [selectedAppointmentDate, setSelectedAppointmentDate] = useState(today);    
    const [selectedTime, setSelectedTime] = useState("");
    const [selectedOption, setSelectedOption] = useState("");
    const [formData, setFormData] = useState({
        first_name: "",
        last_name: "",
        id_number: "",
        email: "",
        birth_date: new Date(),
        appointment_date: new Date(),
        // appointment_time: "",
        doctor: "",
        appointment_reason: "",
      });
      const [loading, setLoading] = useState(false);
    // Fetch options from Django API on component mount
    useEffect(() => {
      axios
        // .get("api/doctors") // Replace with your Django endpoint
        .get("http://localhost:8082/api/doctors") // Replace with your Django endpoint
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
        const { id, value } = event.target;
        // setSelectedOption(value);
        setFormData((prev) => ({ ...prev, [id]: value }));
    };
    const handleSelectChange = (event) => {
        const { id, value } = event.target;
        setSelectedOption(value);
        setFormData((prev) => ({ ...prev, [id]: value }));
    };
    const handleBirthDateChange = (event) => {
        setSelectedBirthDate(event)
        setFormData((prev) => ({ ...prev, ["birth_date"]: event }));
    };
    const handleAppointmentDateChange = (date) => {
        // Update only the date part
        setSelectedAppointmentDate(date);
        updateFormData(date, selectedTime);
      };

    const handleTimeChange = (event) => {
        // Update only the time part
        const time = event.target.value;
        setSelectedTime(time);
        updateFormData(selectedAppointmentDate, time);
      };
    
      const updateFormData = (date, time) => {
        if (!date || !time) return;
    
        // Combine date and time into a single Date object
        const combinedDateTime = new Date(date);
        const [hours, minutes] = time.split(":");
        combinedDateTime.setHours(hours);
        combinedDateTime.setMinutes(minutes);
    
        // Save the combined date and time into the form data
        setFormData((prev) => ({
          ...prev,
          appointment_date: combinedDateTime, // Save in ISO format
        }));
      };


    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
          // Replace with your actual API endpoint
          console.log("formData:", formData);
          const response = await axios.post("http://localhost:8082/api/appointments", formData);
          console.log("Response:", response.data);
    
          // Notify parent component
          if (onSubmit) {
            onSubmit(response.data);
          }
    
          alert("Appointment successfully created!");
        } catch (error) {
          console.error("Error submitting form:", error);
          alert("There was an error creating the appointment.");
        } finally {
          setLoading(false);
        }
      };

    const customTheme = {
        "root": {
            "base": "relative"
        },
        "popup": {
            "root": {
                "base": "absolute bottom-10 z-50 block pt-2",
                "inline": "relative top-0 z-auto",
                "inner": "inline-block rounded-lg bg-secondary bg-white p-4 shadow-lg dark:bg-gray-700",
            },
            "header": {
            "base": "",
            "title": "px-2 py-3 text-center font-semibold text-gray-900 dark:text-white",
            "selectors": {
                "base": "mb-2 flex justify-between",
                "button": {
                "base": "rounded-lg bg-white px-5 py-2.5 text-sm font-semibold text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600",
                "prev": "",
                "next": "",
                "view": ""
                }
            }
            },
            "view": {
            "base": "p-1"
            },
            "footer": {
            "base": "mt-2 flex space-x-2",
            "button": {
                "base": "w-full rounded-lg px-5 py-2 text-center text-sm font-medium focus:ring-4 focus:ring-cyan-300",
                "today": "bg-cyan-700 text-white hover:bg-cyan-800 dark:bg-cyan-600 dark:hover:bg-cyan-700",
                "clear": "border border-gray-300 bg-white text-gray-900 hover:bg-gray-100 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600"
            }
            }
        },
        "views": {
            "days": {
            "header": {
                "base": "mb-1 grid grid-cols-7",
                "title": "h-6 text-center text-sm font-medium leading-6 text-gray-500 dark:text-gray-400"
            },
            "items": {
                "base": "grid w-64 grid-cols-7",
                "item": {
                "base": "block flex-1 cursor-pointer rounded-lg border-0 text-center text-sm font-semibold leading-9 text-gray-900 hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600",
                "selected": "bg-cyan-700 text-white hover:bg-cyan-600",
                "disabled": "text-gray-500"
                }
            }
            },
            "months": {
            "items": {
                "base": "grid w-64 grid-cols-4",
                "item": {
                "base": "block flex-1 cursor-pointer rounded-lg border-0 text-center text-sm font-semibold leading-9 text-gray-900 hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600",
                "selected": "bg-cyan-700 text-white hover:bg-cyan-600",
                "disabled": "text-gray-500"
                }
            }
            },
            "years": {
            "items": {
                "base": "grid w-64 grid-cols-4",
                "item": {
                "base": "block flex-1 cursor-pointer rounded-lg border-0 text-center text-sm font-semibold leading-9 text-gray-900 hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600",
                "selected": "bg-cyan-700 text-white hover:bg-cyan-600",
                "disabled": "text-gray-500"
                }
            }
            },
            "decades": {
            "items": {
                "base": "grid w-64 grid-cols-4",
                "item": {
                "base": "block flex-1 cursor-pointer rounded-lg border-0 text-center text-sm font-semibold leading-9 text-gray-900 hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600",
                "selected": "bg-cyan-700 text-white hover:bg-cyan-600",
                "disabled": "text-gray-500"
                }
            }
            }
        }
    };

return (
  <div className="w-full h-full flex flex-col justify-end bg-white p-6 rounded-lg">
    <form onSubmit={handleSubmit}>
        <div class="grid gap-6 mb-2 md:grid-cols-2">
            <div>
                <label for="first_name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Nombre</label>
                <input onChange={handleChange}  type="text" id="first_name" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Coloca tu nombre" required />
            </div>
            <div>
                <label for="last_name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Apellido</label>
                <input onChange={handleChange}  type="text" id="last_name" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Coloca tu apellido" required />
            </div>
        </div>
        <div class="grid gap-6 mb-2 md:grid-cols-2">
            <div class="mb-2">
                <label for="id_number" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Cédula de identidad</label>
                <input onChange={handleChange}  type="id_number" id="id_number" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="eg. 11254879" required />
            </div> 
            <div class="mb-2">
                <label for="email" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Correo electrónico</label>
                <input onChange={handleChange}  type="email" id="email" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="eg. ejemplo@gmail.com" required />
            </div> 
            <div>
                <label for="birth_date" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Fecha de nacimiento</label>
                <Datepicker theme={customTheme} id="birth_date" value={selectedBirthDate} onChange={handleBirthDateChange}/>
            </div>
            <div>
                <label for="appointment_date" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Fecha deseada para cita</label>
                <div class="flex flex-row">
                    <Datepicker theme={customTheme} id="appointment_date" value={selectedAppointmentDate} onChange={handleAppointmentDateChange}/>
                    <div class="relative">
                        <div class="absolute inset-y-0 end-0 top-0 flex items-center pe-3.5 pointer-events-none">
                            <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                                <path fill-rule="evenodd" d="M2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10S2 17.523 2 12Zm11-4a1 1 0 1 0-2 0v4a1 1 0 0 0 .293.707l3 3a1 1 0 0 0 1.414-1.414L13 11.586V8Z" clip-rule="evenodd"/>
                            </svg>
                        </div>
                        <input type="time" id="time" value={selectedTime} onChange={handleTimeChange} class="bg-gray-50 border leading-none border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" min="09:00" max="18:00" required />
                    </div>
                </div>
            </div>
                
        </div>
        
        <div class="mb-2">
            <label for="doctor" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Doctor a agendar</label>
            <select value={selectedOption} onChange={handleSelectChange} id='doctor' class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                <option value="" disabled>
                    Selecciona un doctor
                </option>
                {options.map((option) => (
                    <option key={option.value} value={option.value}>
                    {option.name}
                    </option>
                ))}
            </select>
            {/* <input onChange={handleChange}  type="doctor" id="doctor" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="eg. 042412345678" required /> */}
        </div>
        
        <div class="mb-2">
            <label for="appointment_reason" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Razón de la cita</label>
            <input onChange={handleChange}  type="appointment_reason" id="appointment_reason" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="eg. Malestar general" required />
        </div> 
        {/* <div class="flex items-start mb-2">
            <div class="flex items-center h-5">
            <input onChange={handleChange} id="remember" type="checkbox" value="" class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800" required />
            </div>
            <label for="remember" class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">I agree with the <a href="#" class="text-blue-600 hover:underline dark:text-blue-500">terms and conditions</a>.</label>
        </div> */}
        <button type="submit" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
        {loading ? (
            <div className="flex justify-center items-center">
              <Spinner aria-label="Loading spinner" />
              <span className="ml-2">Submitting...</span>
            </div>
          ) : (
            "Submit"
          )}
        </button>
    </form>
  </div>
);
};

export default ChatForm;
