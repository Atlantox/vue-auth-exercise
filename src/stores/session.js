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
    }
  },

  persist: true
})

export default useSessionStore