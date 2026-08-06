import { Outlet } from "react-router-dom";

import Sidebar from "../components/layout/Sidebar";
import Navbar from "../components/layout/Navbar";

export default function MainLayout() {
    return (
        <div className="app-layout">

            <Sidebar />

            <div className="main-wrapper">

                <Navbar />

                <main className="page-content fade-in">

                    <Outlet />

                </main>

            </div>

        </div>
    );
}