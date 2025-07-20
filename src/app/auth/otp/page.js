"use client";
import React, { useState, useRef, useEffect } from "react";
import { Shield, ArrowLeft, RefreshCw } from "lucide-react";
import Link from "next/link";
import useThemeStore from '@/components/stores/useThemeStore';
import { useRouter } from "next/navigation"; 

export default function OTPVerification() {
  const router = useRouter();
  const { darkMode } = useThemeStore();
  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const [isLoading, setIsLoading] = useState(false);
  const [isResending, setIsResending] = useState(false);
  const [timer, setTimer] = useState(60);
  const [canResend, setCanResend] = useState(false);
  const inputRefs = useRef([]);

  // Timer effect
  useEffect(() => {
    if (timer > 0) {
      const interval = setInterval(() => {
        setTimer(prev => prev - 1);
      }, 1000);
      return () => clearInterval(interval);
    } else {
      setCanResend(true);
    }
  }, [timer]);

  const handleOtpChange = (index, value) => {
    if (value.length > 1) return; 
    
    const newOtp = [...otp];
    newOtp[index] = value;
    setOtp(newOtp);

    // Auto-focus next input
    if (value && index < 5) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (index, e) => {
    // Handle backspace
    if (e.key === 'Backspace' && !otp[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
    // Handle paste
    if (e.key === 'v' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      navigator.clipboard.readText().then(text => {
        const pastedOtp = text.replace(/\D/g, '').slice(0, 6).split('');
        const newOtp = [...otp];
        pastedOtp.forEach((digit, idx) => {
          if (idx < 6) newOtp[idx] = digit;
        });
        setOtp(newOtp);
        
        // Focus the next empty input or the last input
        const nextIndex = Math.min(pastedOtp.length, 5);
        inputRefs.current[nextIndex]?.focus();
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const otpString = otp.join('');
    if (otpString.length !== 6) {
      alert("Please enter all 6 digits");
      return;
    }
    const storedEmail = localStorage.getItem('email')
    setIsLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/verify-otp/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: storedEmail,
          otp: otpString,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.message || "OTP verification failed");
      }

      alert("Verification successful!");
      router.push("/auth/login/");
    } catch (error) {
      alert(error.message);
      // Clear OTP on error
      setOtp(['', '', '', '', '', '']);
      inputRefs.current[0]?.focus();
    } finally {
      setIsLoading(false);
    }
  };

  const handleResendOTP = async () => {
    if (!canResend) return;
    
    setIsResending(true);
    setCanResend(false);
    setTimer(60);

    try {
      const res = await fetch("/api/resend-otp", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          // Add email or phone from previous step
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.message || "Failed to resend OTP");
      }

      alert("OTP sent successfully!");
    } catch (error) {
      alert(error.message);
      setCanResend(true);
      setTimer(0);
    } finally {
      setIsResending(false);
    }
  };

  return (
    <div className="max-h-screen overflow-y-auto">
      <form className="p-6 space-y-4" onSubmit={handleSubmit}>
        {/* Back Button */}
        <div className="mb-2">
          <Link 
            href="/auth/register"
            className={`inline-flex items-center text-sm font-medium transition-colors duration-200 ${
              darkMode
                ? "text-gray-400 hover:text-gray-300"
                : "text-gray-600 hover:text-gray-700"
            }`}
          >
            <ArrowLeft className="w-4 h-4 mr-1" />
            Back to Registration
          </Link>
        </div>

        {/* Header */}
        <div className="text-center mb-6">
          <div
            className={`inline-flex items-center justify-center w-14 h-14 rounded-full mb-3 ${
              darkMode
                ? "bg-gradient-to-r from-blue-500 to-purple-600"
                : "bg-gradient-to-r from-blue-600 to-purple-700"
            }`}
          >
            <Shield className="w-7 h-7 text-white" />
          </div>
          <h1
            className={`text-2xl font-bold mb-1 ${
              darkMode ? "text-white" : "text-gray-900"
            }`}
          >
            Verify Your Account
          </h1>
          <p
            className={`text-sm ${
              darkMode ? "text-gray-400" : "text-gray-600"
            }`}
          >
            Enter the 6-digit code sent to your email address
          </p>
          <p
            className={`text-xs mt-1 font-medium ${
              darkMode ? "text-blue-400" : "text-blue-600"
            }`}
          >
            example@email.com
          </p>
        </div>

        {/* OTP Input Fields */}
        <div className="space-y-4">
          <label
            className={`block text-sm font-medium text-center ${
              darkMode ? "text-gray-300" : "text-gray-700"
            }`}
          >
            Verification Code
          </label>
          
          <div className="flex justify-center gap-3">
            {otp.map((digit, index) => (
              <input
                key={index}
                ref={el => inputRefs.current[index] = el}
                type="text"
                inputMode="numeric"
                maxLength="1"
                value={digit}
                onChange={(e) => handleOtpChange(index, e.target.value.replace(/\D/g, ''))}
                onKeyDown={(e) => handleKeyDown(index, e)}
                className={`w-12 h-12 text-center text-xl font-bold rounded-xl border-2 transition-all duration-200 ${
                  darkMode
                    ? `bg-gray-700/50 border-gray-600 text-white focus:border-blue-500 focus:bg-gray-700 ${digit ? 'border-blue-500 bg-gray-700' : ''}`
                    : `bg-white border-gray-300 text-gray-900 focus:border-blue-500 focus:bg-blue-50/50 ${digit ? 'border-blue-500 bg-blue-50/30' : ''}`
                } focus:outline-none focus:ring-2 focus:ring-blue-500/20`}
                autoComplete="off"
              />
            ))}
          </div>
        </div>

        {/* Timer and Resend */}
        <div className="text-center space-y-2">
          {!canResend ? (
            <p
              className={`text-sm ${
                darkMode ? "text-gray-400" : "text-gray-600"
              }`}
            >
              Didn't receive the code? Resend in{" "}
              <span className={`font-medium ${darkMode ? "text-blue-400" : "text-blue-600"}`}>
                {timer}s
              </span>
            </p>
          ) : (
            <button
              type="button"
              onClick={handleResendOTP}
              disabled={isResending}
              className={`inline-flex items-center text-sm font-medium transition-colors duration-200 ${
                darkMode
                  ? "text-blue-400 hover:text-blue-300"
                  : "text-blue-600 hover:text-blue-700"
              } disabled:opacity-50 hover:underline`}
            >
              {isResending ? (
                <>
                  <RefreshCw className="w-4 h-4 mr-1 animate-spin" />
                  Sending...
                </>
              ) : (
                <>
                  <RefreshCw className="w-4 h-4 mr-1" />
                  Resend Code
                </>
              )}
            </button>
          )}
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading || otp.join('').length !== 6}
          className={`w-full py-2.5 px-4 rounded-xl font-semibold text-white transition-all duration-200 ${
            isLoading || otp.join('').length !== 6
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-gradient-to-r from-blue-600 to-purple-700 hover:from-blue-700 hover:to-purple-800 transform hover:scale-[1.02] active:scale-[0.98]"
          } shadow-lg hover:shadow-xl focus:outline-none focus:ring-2 focus:ring-blue-500/50`}
        >
          {isLoading ? (
            <div className="flex items-center justify-center">
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
              Verifying...
            </div>
          ) : (
            "Verify Account"
          )}
        </button>

        {/* Footer Links */}
        <div className="mt-4 space-y-2">
          <div
            className={`text-center text-sm ${
              darkMode ? "text-gray-400" : "text-gray-600"
            }`}
          >
            <span>Having trouble? </span>
            <Link
              href="/auth/contact"
              className={`font-medium transition-colors duration-200 ${
                darkMode
                  ? "text-blue-400 hover:text-blue-300"
                  : "text-blue-600 hover:text-blue-700"
              } hover:underline`}
            >
              Contact Support
            </Link>
          </div>
        </div>

        {/* Decorative Bubbles */}
        <div className="absolute -top-4 -left-4 w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full opacity-20 blur-sm"></div>
        <div className="absolute -bottom-4 -right-4 w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-600 rounded-full opacity-20 blur-sm"></div>
      </form>
    </div>
  );
}