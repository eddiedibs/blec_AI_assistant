import { create } from "zustand";
import { toast, Bounce } from "react-toastify";

const UseNotificationStore = create((set) => ({
  notifySuccess: (message) => {
    toast.success(message, {
      position: "bottom-right",
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: false,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "colored",
      transition: Bounce,
    });
  },
  notifyError: (message) => {
    toast.error(message, {
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: false,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "colored",
      transition: Bounce,
    });
  },
  notifyInfo: (message) => {
    toast.info(message, {
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: false,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "colored",
      transition: Bounce,
    });
  },
  notifyWarning: (message) => {
    toast.warn(message, {
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: false,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "colored",
      transition: Bounce,
    });
  },
  customNotification: (message, options) => {
    toast(message, options);
  },
}));
export default UseNotificationStore;
