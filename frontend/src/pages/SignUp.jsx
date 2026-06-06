import { useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";
import "./SignUp.css";

export default function Signup() {
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [username, setUserName] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSignup = async () => {
        if (!email || !password || !username) {
            alert("All fields required");
            return;
        }

        try {
            setLoading(true);

            await api.post("/accounts/register/", {
                username,
                email,
                password,
            });

            // store email for OTP step
            localStorage.setItem("signup_email", email);
            localStorage.setItem("pass",password);

            navigate("/verify-otp");
        } catch (err) {
            const data = err.response?.data;

            const message = data
                ? Object.values(data).flat()[0]
                : "Signup failed";

            alert(message);
        }
        finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-box">
                <h2>Create Account</h2>
                <p className="auth-subtitle">Join SnapSync</p>

                <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <input
                        id="username"
                        type="text"
                        placeholder="Enter your username"
                        value={username}
                        onChange={(e) => setUserName(e.target.value)}
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="email">Email</label>
                    <input
                        id="email"
                        type="email"
                        placeholder="Enter your email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <input
                        id="password"
                        type="password"
                        placeholder="Enter your password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>

                <button 
                    className="auth-button"
                    onClick={handleSignup} 
                    disabled={loading}
                >
                    {loading ? "Creating account..." : "Sign Up"}
                </button>

                <p className="auth-link">
                    Already have an account? <a href="/login">Login</a>
                </p>
            </div>
        </div>
    );
}