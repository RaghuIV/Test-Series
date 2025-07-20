"use client";
import React, { useState } from "react";
import { Eye, EyeOff, Mail, Lock, User, Phone } from "lucide-react";
import Link from "next/link";
import useThemeStore from '@/components/stores/useThemeStore';
import { useRouter } from "next/navigation"; 

export default function Register() {
  const router = useRouter();
  const { darkMode } = useThemeStore();
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [inputEmail, setInputEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
  e.preventDefault();

  if (password !== confirmPassword) {
    alert("Passwords do not match");
    return;
  }

  setIsLoading(true);
  localStorage.setItem('email',inputEmail)

  try {
    const res = await fetch("http://127.0.0.1:8000/api/register/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        first_name: firstName,
        last_name: lastName,
        email: inputEmail,
        phone,
        password,
      }),
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.message || "Registration failed");
    }

    router.push("/auth/otp");
  } catch (error) {
    alert(error.message);
  } finally {
    setIsLoading(false);
  }
};

  return (
      <div className="max-h-screen overflow-y-auto">
        <form className="p-6 space-y-4" onSubmit={handleSubmit}>
        {/* Header */}
        <div className="text-center mb-3">
          <div
            className={`inline-flex items-center justify-center w-14 h-14 rounded-full mb-3 ${
              darkMode
                ? "bg-gradient-to-r from-blue-500 to-purple-600"
                : "bg-gradient-to-r from-blue-600 to-purple-700"
            }`}
          >
            <User className="w-7 h-7 text-white" />
          </div>
          <h1
            className={`text-2xl font-bold mb-1 ${
              darkMode ? "text-white" : "text-gray-900"
            }`}
          >
            Create Account
          </h1>
          <p
            className={`text-sm ${
              darkMode ? "text-gray-400" : "text-gray-600"
            }`}
          >
            Join our Test Series platform and start your journey
          </p>
        </div>

        {/* Full Name Field */}
        <div className="space-y-1 flex gap-x-1">
          <div>
          <label
            className={`block text-sm font-medium ${
              darkMode ? "text-gray-300" : "text-gray-700"
            }`}
          >
            First Name
          </label>
          <div className="relative">
            <User
              className={`absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 ${
                darkMode ? "text-gray-400" : "text-gray-500"
              }`}
            />
            <input
              type="text"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              placeholder="First name"
              className={`w-full pl-10 pr-4 py-2.5 rounded-xl border transition-all duration-200 ${
                darkMode
                  ? "bg-gray-700/50 border-gray-600 text-white placeholder-gray-400 focus:border-blue-500 focus:bg-gray-700"
                  : "bg-white border-gray-300 text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:bg-blue-50/50"
              } focus:outline-none focus:ring-2 focus:ring-blue-500/20`}
              required
            />
          </div>
          </div>
          <div>
          <label
            className={`block text-sm font-medium ${
              darkMode ? "text-gray-300" : "text-gray-700"
            }`}
          >
            Last Name
          </label>
          <div className="relative">
            <User
              className={`absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 ${
                darkMode ? "text-gray-400" : "text-gray-500"
              }`}
            />
            <input
              type="text"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              placeholder="Last name"
              className={`w-full pl-10 pr-4 py-2.5 rounded-xl border transition-all duration-200 ${
                darkMode
                  ? "bg-gray-700/50 border-gray-600 text-white placeholder-gray-400 focus:border-blue-500 focus:bg-gray-700"
                  : "bg-white border-gray-300 text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:bg-blue-50/50"
              } focus:outline-none focus:ring-2 focus:ring-blue-500/20`}
              required
            />
          </div>
          </div>
        </div>

        {/* Email Field */}
        <div className="space-y-1">
          <label
            className={`block text-sm font-medium ${
              darkMode ? "text-gray-300" : "text-gray-700"
            }`}
          >
            Email Address
          </label>
          <div className="relative">
            <Mail
              className={`absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 ${
                darkMode ? "text-gray-400" : "text-gray-500"
              }`}
            />
            <input
              type="email"
              value={inputEmail}
              onChange={(e) => setInputEmail(e.target.value)}
              placeholder="Enter your email"
              className={`w-full pl-10 pr-4 py-2.5 rounded-xl border transition-all duration-200 ${
                darkMode
                  ? "bg-gray-700/50 border-gray-600 text-white placeholder-gray-400 focus:border-blue-500 focus:bg-gray-700"
                  : "bg-white border-gray-300 text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:bg-blue-50/50"
              } focus:outline-none focus:ring-2 focus:ring-blue-500/20`}
              required
            />
          </div>
        </div>

        {/* Phone Number Field */}
        <div className="space-y-1">
          <label
            className={`block text-sm font-medium ${
              darkMode ? "text-gray-300" : "text-gray-700"
            }`}
          >
            Phone Number
          </label>
          <div className="relative">
            <Phone
              className={`absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 ${
                darkMode ? "text-gray-400" : "text-gray-500"
              }`}
            />
            <input
              type="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="Enter your phone number"
              className={`w-full pl-10 pr-4 py-2.5 rounded-xl border transition-all duration-200 ${
                darkMode
                  ? "bg-gray-700/50 border-gray-600 text-white placeholder-gray-400 focus:border-blue-500 focus:bg-gray-700"
                  : "bg-white border-gray-300 text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:bg-blue-50/50"
              } focus:outline-none focus:ring-2 focus:ring-blue-500/20`}
              required
            />
          </div>
        </div>

        {/* Password Field */}
        <div className="space-y-1">
          <label
            className={`block text-sm font-medium ${
              darkMode ? "text-gray-300" : "text-gray-700"
            }`}
          >
            Password
          </label>
          <div className="relative">
            <Lock
              className={`absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 ${
                darkMode ? "text-gray-400" : "text-gray-500"
              }`}
            />
            <input
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Create a strong password"
              className={`w-full pl-10 pr-12 py-2.5 rounded-xl border transition-all duration-200 ${
                darkMode
                  ? "bg-gray-700/50 border-gray-600 text-white placeholder-gray-400 focus:border-blue-500 focus:bg-gray-700"
                  : "bg-white border-gray-300 text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:bg-blue-50/50"
              } focus:outline-none focus:ring-2 focus:ring-blue-500/20`}
              required
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className={`absolute right-3 top-1/2 transform -translate-y-1/2 ${
                darkMode
                  ? "text-gray-400 hover:text-gray-300"
                  : "text-gray-500 hover:text-gray-600"
              }`}
            >
              {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
            </button>
          </div>
        </div>

        {/* Confirm Password Field */}
        <div className="space-y-1">
          <label
            className={`block text-sm font-medium ${
              darkMode ? "text-gray-300" : "text-gray-700"
            }`}
          >
            Confirm Password
          </label>
          <div className="relative">
            <Lock
              className={`absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 ${
                darkMode ? "text-gray-400" : "text-gray-500"
              }`}
            />
            <input
              type={showConfirmPassword ? "text" : "password"}
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm your password"
              className={`w-full pl-10 pr-12 py-2.5 rounded-xl border transition-all duration-200 ${
                darkMode
                  ? "bg-gray-700/50 border-gray-600 text-white placeholder-gray-400 focus:border-blue-500 focus:bg-gray-700"
                  : "bg-white border-gray-300 text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:bg-blue-50/50"
              } focus:outline-none focus:ring-2 focus:ring-blue-500/20`}
              required
            />
            <button
              type="button"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              className={`absolute right-3 top-1/2 transform -translate-y-1/2 ${
                darkMode
                  ? "text-gray-400 hover:text-gray-300"
                  : "text-gray-500 hover:text-gray-600"
              }`}
            >
              {showConfirmPassword ? <EyeOff size={20} /> : <Eye size={20} />}
            </button>
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading}
          className={`w-full py-2.5 px-4 rounded-xl font-semibold text-white transition-all duration-200 ${
            isLoading
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-gradient-to-r from-blue-600 to-purple-700 hover:from-blue-700 hover:to-purple-800 transform hover:scale-[1.02] active:scale-[0.98]"
          } shadow-lg hover:shadow-xl focus:outline-none focus:ring-2 focus:ring-blue-500/50`}
        >
          {isLoading ? (
            <div className="flex items-center justify-center">
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
              Creating Account...
            </div>
          ) : (
            "Create Account"
          )}
        </button>

        {/* Footer Links */}
        <div className="mt-4 space-y-2">
          <div
            className={`text-center text-sm ${
              darkMode ? "text-gray-400" : "text-gray-600"
            }`}
          >
            <span>Already have an account? </span>
            <Link
              href="/auth/login"
              className={`font-medium transition-colors duration-200 ${
                darkMode
                  ? "text-blue-400 hover:text-blue-300"
                  : "text-blue-600 hover:text-blue-700"
              } hover:underline`}
            >
              Sign in here
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