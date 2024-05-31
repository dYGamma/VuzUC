import { Dashboard } from "./routes/dashboard";
import {
  Navigate,
  RouterProvider,
  createBrowserRouter,
} from "react-router-dom";
import { ThemeProvider } from "./components/theme-provider";
import { Authentification } from "./routes/authentication";

import "@/core/styles/globals.css";
import ProductsPage from "./routes/products";
import NavBar from "./components/nav-bar";

const router = createBrowserRouter([
  {
    path: "/dashboard",
    element: <NavBar />,
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      {
        path: "/dashboard/products",
        element: <ProductsPage />,
      },
    ],
  },
  {
    path: "/",
    element: <Authentification />,
  },
  {
    path: "*",
    element: <Navigate to="/dashboard" />,
  },
]);

function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <RouterProvider router={router} />
    </ThemeProvider>
  );
}

export default App;
