import { Routes, Route, useLocation } from "react-router-dom";
import ChatComp from "./components/ChatComp";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/SignIn";
import SignUp from "./pages/SignUp";

const AppRoutes = [
  {
    path: "/login",
    element: <Login />,
    isPrivate: false,
  },
  {
    path: "/signup",
    element: <SignUp />,
    isPrivate: false,
  },
  {
    path: "/dashboard",
    element: <Dashboard />,
    isPrivate: true,
  },
  {
    path: "/chat/:chat_id",
    element: <ChatComp />,
    isPrivate: false,
  },
];

function App() {
  const location = useLocation();

  return (
    <>
      <Routes>
        {AppRoutes.map((route) => (
          <Route
            path={route.path}
            element={
              route?.isPrivate ? (
                <div className="flex">
                  <Sidebar />
                  {route.element}
                </div>
              ) : (
                route.element
              )
            }
          />
        ))}
      </Routes>
    </>
  );
}

export default App;
