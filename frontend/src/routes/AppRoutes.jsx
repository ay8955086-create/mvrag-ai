import {
    Routes,
    Route,
} from "react-router-dom";

import MainLayout from "../layouts/MainLayout";

import Dashboard from "../pages/Dashboard";
import Upload from "../pages/Upload";
import Library from "../pages/Library";
import Chat from "../pages/Chat";
import Analytics from "../pages/Analytics";
import Settings from "../pages/Settings";
import NotFound from "../pages/NotFound";

export default function AppRoutes() {

    return (

        <Routes>

            <Route element={<MainLayout />}>

                <Route
                    path="/"
                    element={<Dashboard />}
                />

                <Route
                    path="/upload"
                    element={<Upload />}
                />

                <Route
                    path="/library"
                    element={<Library />}
                />

                <Route
                    path="/chat"
                    element={<Chat />}
                />

                <Route
                    path="/analytics"
                    element={<Analytics />}
                />

                <Route
                    path="/settings"
                    element={<Settings />}
                />

            </Route>

            <Route
                path="*"
                element={<NotFound />}
            />

        </Routes>

    );

}