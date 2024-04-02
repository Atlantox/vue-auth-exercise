import { defineStore } from 'pinia'

const useSessionStore = defineStore('session', {
  state: () => {
    return {
      token: ''
    }
  },
  persist: true
})

export default useSessionStore