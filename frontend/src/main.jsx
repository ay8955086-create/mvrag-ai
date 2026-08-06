import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "react-hot-toast";

import App from "./App";

import "./styles/globals.css";
import "./styles/variables.css";
import "./styles/animations.css";

import { ThemeProvider } from "./context/ThemeContext";

const queryClient = new QueryClient();

ReactDOM.createRoot(
document.getElementById("root")
).render(

<React.StrictMode>

<BrowserRouter>

<QueryClientProvider client={queryClient}>

<ThemeProvider>

<App/>

<Toaster position="top-right"/>

</ThemeProvider>

</QueryClientProvider>

</BrowserRouter>

</React.StrictMode>

);