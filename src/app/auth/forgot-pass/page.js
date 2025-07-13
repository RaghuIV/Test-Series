"use client"
import React, { useState } from "react";
import { Mail, ArrowLeft, CheckCircle } from "lucide-react";
import Link from "next/link";
import useThemeStore from '@/components/stores/useThemeStore';

export default function ForgotPassword() {
  const { darkMode } = useThemeStore();
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    await new Promise((resolve) => setTimeout(resolve, 1500));
    setIsLoading(false);
    setIsSuccess(true);
  };

  return (
      <div className="p-8 space-y-6">
        {/* Header */}
        <div className="text-center mb-4">
          <div
            className={`inline-flex items-center justify-center w-16 h-16 rounded-full mb-4 ${
              darkMode
                ? "bg-gradient-to-r from-blue-500 to-purple-600"
                : "bg-gradient-to-r from-blue-600 to-purple-700"
            }`}
          >
            <Mail className="w-8 h-8 text-white" />
          </div>
          <h1
            className={`text-3xl font-bold mb-2 ${
              darkMode ? "text-white" : "text-gray-900"
            }`}
          >
            {isSuccess ? "Check Your Email" : "Forgot Password?"}
          </h1>
          <p
            className={`text-sm ${
              darkMode ? "text-gray-400" : "text-gray-600"
            }`}
          >
            {isSuccess 
              ? "We've sent a password reset link to your email address"
              : "Enter your email address and we'll send you a link to reset your password"
            }
          </p>
        </div>

        {!isSuccess ? (
          <form onSubmit={handleSubmit}>
            {/* Email Field */}
            <div className="space-y-2 mb-6">
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
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email"
                  className={`w-full pl-10 pr-4 py-3 rounded-xl border transition-all duration-200 ${
                    darkMode
                      ? "bg-gray-700/50 border-gray-600 text-white placeholder-gray-400 focus:border-blue-500 focus:bg-gray-700"
                      : "bg-white border-gray-300 text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:bg-blue-50/50"
                  } focus:outline-none focus:ring-2 focus:ring-blue-500/20`}
                  required
                />
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className={`w-full py-3 px-4 rounded-xl font-semibold text-white transition-all duration-200 ${
                isLoading
                  ? "bg-gray-400 cursor-not-allowed"
                  : "bg-gradient-to-r from-blue-600 to-purple-700 hover:from-blue-700 hover:to-purple-800 transform hover:scale-[1.02] active:scale-[0.98]"
              } shadow-lg hover:shadow-xl focus:outline-none focus:ring-2 focus:ring-blue-500/50`}
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                  Sending Reset Link...
                </div>
              ) : (
                "Send Reset Link"
              )}
            </button>
          </form>
        ) : (
          <div className="text-center space-y-6">
            <div
              className={`inline-flex items-center justify-center w-20 h-20 rounded-full ${
                darkMode
                  ? "bg-green-900/30 text-green-400"
                  : "bg-green-100 text-green-600"
              }`}
            >
              <CheckCircle className="w-10 h-10" />
            </div>
            <div className="space-y-2">
              <p
                className={`text-sm ${
                  darkMode ? "text-gray-400" : "text-gray-600"
                }`}
              >
                If an account with that email exists, we've sent you a password reset link.
              </p>
              <p
                className={`text-xs ${
                  darkMode ? "text-gray-500" : "text-gray-500"
                }`}
              >
                Didn't receive the email? Check your spam folder or try again.
              </p>
            </div>
            <button
              onClick={() => setIsSuccess(false)}
              className={`text-sm font-medium transition-colors duration-200 ${
                darkMode
                  ? "text-blue-400 hover:text-blue-300"
                  : "text-blue-600 hover:text-blue-700"
              } hover:underline`}
            >
              Try with a different email
            </button>
          </div>
        )}

        {/* Footer Links */}
        <div className="mt-8 space-y-4">
          <div className="text-center">
            <Link
              href="/auth/login"
              className={`inline-flex items-center text-sm font-medium transition-colors duration-200 ${
                darkMode
                  ? "text-blue-400 hover:text-blue-300"
                  : "text-blue-600 hover:text-blue-700"
              } hover:underline`}
            >
              <ArrowLeft className="w-4 h-4 mr-1" />
              Back to Login
            </Link>
          </div>
          <div
            className={`text-center text-sm ${
              darkMode ? "text-gray-400" : "text-gray-600"
            }`}
          >
            <span>Don't have an account? </span>
            <Link
              href="/auth/register"
              className={`font-medium transition-colors duration-200 ${
                darkMode
                  ? "text-blue-400 hover:text-blue-300"
                  : "text-blue-600 hover:text-blue-700"
              } hover:underline`}
            >
              Create one now
            </Link>
          </div>
        </div>

        {/* Decorative Bubbles */}
        <div className="absolute -top-4 -left-4 w-8 h-8 bg-gradient-to-br from-orange-500 to-red-600 rounded-full opacity-20 blur-sm"></div>
        <div className="absolute -bottom-4 -right-4 w-12 h-12 bg-gradient-to-br from-red-500 to-pink-600 rounded-full opacity-20 blur-sm"></div>
      </div>
  );
}