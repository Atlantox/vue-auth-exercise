import { ref } from 'vue'
import useSessionStore  from '@/stores/session.js'
import ApiConfig from './config.js'
const apiConfig = new ApiConfig()

class LoginService{
    constructor(){
        this.loginResult = ref('')
    }

    GetLoginResult(){
        return this.loginResult
    }

    async TryLogin(username, password){
        const store = useSessionStore()
        try{
            let url = apiConfig.base_url + '/login'
            var fetchHeaders = {
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
            let response = await fetch(url, fetchConfig)
            let json = await response.json()
            this.loginResult.value = await json
        }
        catch(error){
            this.loginResult.value = 'Error: ' + error
        }
    }
}

export default LoginService