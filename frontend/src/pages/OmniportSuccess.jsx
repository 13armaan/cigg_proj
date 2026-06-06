import { useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";


export default function OmniportSuccess() {
  const {login} = useAuth();
  const navigate = useNavigate();
  

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const access = params.get("access");
    const refresh = params.get("refresh");

    if (!access || !refresh) {
      navigate("/login");
      return;
    }

    
    login(access,refresh)

    setTimeout(() => navigate("/gallery"), 0);
  }, []);

  return <p>Logging you in...</p>;
}
