'use client';

import { Sun, Moon } from 'lucide-react';
import useThemeStore from '@/components/stores/useThemeStore';

export default function AuthLayout({ children }) {
  const { darkMode, toggleDarkMode } = useThemeStore();

  return (
    <div
      className={`h-screen w-full flex items-center justify-center p-4 transition-colors duration-300 ${
        darkMode
          ? 'bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900'
          : 'bg-gradient-to-br from-blue-50 via-white to-purple-50'
      }`}
    >
      <div
        className={`relative w-full max-w-md backdrop-blur-xl rounded-2xl shadow-2xl border transition-all duration-300 ${
          darkMode
            ? 'bg-gray-800/80 border-gray-700/50 shadow-black/20'
            : 'bg-white/80 border-white/20 shadow-black/10'
        }`}
      >
        <button
          onClick={toggleDarkMode}
          className={`absolute top-4 right-4 p-2 rounded-full transition-all duration-300 ${
            darkMode
              ? 'bg-gray-700 hover:bg-gray-600 text-yellow-400'
              : 'bg-gray-100 hover:bg-gray-200 text-gray-600'
          }`}
        >
          {darkMode ? <Sun size={20} /> : <Moon size={20} />}
        </button>

        {children}
      </div>
    </div>
  );
}
