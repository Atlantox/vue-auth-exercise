import { defineStore } from 'pinia'

const useSessionStore = defineStore('session', {
  state: () => {
    return {
      token: '',
      userData: ''
    }
  },
  actions:{
    DestroySession(){
      this.token = ''
      window.location.href = '/'
    }
  },

  persist: true
})

export default useSessionStore