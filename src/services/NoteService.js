import { ref } from 'vue'
import useSessionStore  from '@/stores/session.js'
import ApiConfig from './config.js'
const apiConfig = new ApiConfig()

class NoteService{
    constructor(){
        this.notes = ref('')
        this.singleNote = ref('')
    }

    GetNotes(){
        return this.notes
    }

    async FetchNotes(){
        const store = useSessionStore()
        try{
            let url = apiConfig.base_url + '/notes'
            var fetchHeaders = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }

            if (store.token !== '')
                fetchHeaders['Authorization'] = 'Bearer ' + store.token
            
            const fetchConfig = {
                method: 'GET',
                headers: fetchHeaders
            }
            let response = await fetch(url, fetchConfig)
            let json = await response.json()
            let result = await json
            if(result.success)
                this.notes.value = result.notes
            else
                this.notes.value = result.message
        }
        catch(error){
            this.notes.value = 'Error: ' + error
        }
    }

    async GetNoteById(){

    }
}

export default NoteService