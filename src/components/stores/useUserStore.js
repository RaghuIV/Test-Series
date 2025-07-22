// userStore.js
import { create } from 'zustand';

const useUserStore = create((set) => ({
  email: '',
  password: '',
  phone: '',
  firstName: '',
  lastName: '',

  // Set individual field
  setField: (key, value) => set((state) => ({ ...state, [key]: value })),

  // Reset all fields
  resetUser: () =>
    set({
      email: '',
      password: '',
      phone: '',
      firstName: '',
      lastName: '',
    }),
}));

export default useUserStore;
