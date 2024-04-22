import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import api from "api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import { useState, useEffect } from "react";

function ProtectedRoute({ children }) {
  const [isAuth, setisAuth] = useState(null);
  // We check if the user is authenticated every time the component is rendered
  useEffect(() => {
    auth().catch(() => setisAuth(false));
  }, []);

  const refreshToken = async () => {
    //We get the refresh token from localStorage
    const refreshToken = localStorage.getItem(REFRESH_TOKEN);
    try {
      //We send the refresh token to the server to get a new access token
      const res = await api.post("/api/token/refresh/", {
        refresh: refreshToken,
      });
      // If the request is successful, we update the access token in localStorage and setisAuth to true
      if (res === 200) {
        localStorage.setItem(ACCESS_TOKEN, res.data.access);
        setisAuth(true);
      } else {
        setisAuth(false);
      }
    } catch (error) {
      console.log(error);
      setisAuth(false);
    }
  };

  // We call the auth function to check if the user is authenticated
  const auth = async () => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    // If the token is not found, we setisAuth to false and return
    if (!token) {
      setisAuth(false);
      return;
    }
    // If the token is found, we decode it to get the expiration time
    const decoded = jwtDecode(token);
    const tokenExpiration = decoded.exp;
    const now = Date.now() / 1000;
    if (tokenExpiration < now) {
      await refreshToken();
    } else {
      setisAuth(true);
    }
  };
  return isAuth ? children : <Navigate to="/login" />;
}

export default ProtectedRoute;
