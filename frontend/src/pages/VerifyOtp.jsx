import { useState, useEffect } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./VerifyOtp.css";

export default function VerifyOtp() {
    const { login } = useAuth();
    const navigate = useNavigate();

    const [otp, setOtp] = useState("");
    const [email, setEmail] = useState("");
    const [pass, setPass] = useState("");
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const storedEmail = localStorage.getItem("signup_email");
        const password = localStorage.getItem("pass");

        if (!storedEmail || !password) {
            navigate("/signup");
        } else {
            setEmail(storedEmail);
            setPass(password);
        }
    }, []);

    const handleVerify = async () => {
        if (!otp) {
            alert("Enter OTP");
            return;
        }

        try {
            setLoading(true);

            await api.post("/accounts/verify-otp/", { email, otp });

            const res = await api.post("/accounts/login/", {
                email: email,
                password: pass,
            });
            console.log(res.data);

            login(res.data.access, res.data.refresh);
            setTimeout(() => navigate("/gallery"), 0);
            localStorage.removeItem("signup_email");
            localStorage.removeItem("pass");

            alert("Account verified!");
            

        } catch (err) {
            const data = err.response?.data;
            const message =
                data?.detail ||
                Object.values(data || {}).flat()[0] ||
                "Verification failed";

            alert(message);
        } finally {
            setLoading(false);
        }

    };

    return (
        <div className="auth-container">
            <div className="auth-box">
                <h2>Verify Email</h2>
                <p className="auth-subtitle">Enter the OTP sent to your email</p>

                <div className="email-display">
                    <p>Verification code sent to:</p>
                    <p className="email-text"><b>{email}</b></p>
                </div>

                <div className="form-group">
                    <label htmlFor="otp">One-Time Password</label>
                    <input
                        id="otp"
                        type="text"
                        placeholder="Enter 6-digit OTP"
                        value={otp}
                        onChange={(e) => setOtp(e.target.value)}
                        maxLength="6"
                    />
                </div>

                <button 
                    className="auth-button"
                    onClick={handleVerify} 
                    disabled={loading}
                >
                    {loading ? "Verifying..." : "Verify OTP"}
                </button>

                
            </div>
        </div>
    );
}