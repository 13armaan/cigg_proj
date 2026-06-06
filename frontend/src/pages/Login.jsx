import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

import "./Login.css";
import api from "../services/api";

function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await api.post("/accounts/login/", {
        email: email,
        password: password,
      });

      // SAVE TOKENS
      // localStorage.setItem("access", res.data.access);
      // localStorage.setItem("refresh", res.data.refresh);
      login(res.data.access, res.data.refresh)
      setTimeout(() => navigate("/gallery"), 0);

      console.log("Login successful!");

    } catch (err) {
      if (err.response) {
        alert(err.response.data?.non_field_errors || "Login failed");
      } else {
        alert("Server error");
      }
    }


  };
  const handleOmniportLogin = () => {
    window.location.href = "http://127.0.0.1:8000/api/accounts/auth/omniport/login/";
  };
  const handleSignup =()=>{
    navigate("/signup")
  }



  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Login</h2>

        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button type="submit">Login</button>
          
          <div className="divider">OR</div>

          <button
            className="omniport-btn"
            onClick={handleOmniportLogin}
          >
          
            Login with Omniport
          </button>
        </form>
        <div className="divider">OR</div>

          <button
            className="omniport-btn"
            onClick={handleSignup}
          >
          
            Sign-Up
          </button>
      </div>
    </div>
  );
}

export default Login;
