import { ref } from 'vue'
import useSessionStore  from '@/stores/session.js'

class LoginService{
    constructor(){
        this.loginResult = ref('')
    }

    getLoginResult(){
        return this.loginResult
    }

    async TryLogin(username, password){
        const store = useSessionStore()
        try{
            const url = 'http://localhost:5000/login'
            let fetchHeaders = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }

            if (store.token !== '')
                fetchHeaders['Authorization'] = 'Bearer ' + store.token
            
            const fetchConfig = {
                method: 'POST',
                headers: fetchHeaders,
                body: JSON.stringify({
                    'username': username,
                    'password': password
                })
            }
            const response = await fetch(url, fetchConfig)
            const json = await response.json()
            this.loginResult.value = await json
        }
        catch(error){
            this.loginResult.value = 'Error: ' + error
        }
    }
}

export default LoginService