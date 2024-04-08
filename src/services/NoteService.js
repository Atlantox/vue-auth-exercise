import { ref } from 'vue'
import useSessionStore  from '@/stores/session.js'
import ApiConfig from './config.js'
const apiConfig = new ApiConfig()

class NoteService{
    constructor(){
        this.notes = ref('')
        this.singleNote = ref('')
        this.handleNote = ref('')
    }

    GetNotes(){
        return this.notes
    }

    GetSingleNote(){
        return this.singleNote
    }

    GetHandleNoteResult(){
        return this.handleNote
    }

    async FetchSingleNote(id){
        const store = useSessionStore()
        try{
            let url = apiConfig.base_url + '/notes/' + id
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
                this.singleNote.value = {'note': result.note, 'success': true }
            else
                this.singleNote.value =  {'message': result.message, 'success': false } 
        }
        catch(error){
            this.singleNote.value = 'Error: ' + error
        }
    }

    async HandleNote(data){
        const store = useSessionStore()
        try{
            let url = apiConfig.base_url + '/notes'
            var fetchHeaders = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }

            if (store.token !== '')
                fetchHeaders['Authorization'] = 'Bearer ' + store.token
            
            let jsonBody = {
                titulo: data['title'],
                contenido: data['content']
            }
            let fetchConfig = {
                method: 'POST',
                headers: fetchHeaders,
                body: JSON.stringify(jsonBody)
            }

            if(data['id'] !== undefined){
                url += '/' + data['id']    
                fetchConfig.method = 'PUT'
            }

            let response = await fetch(url, fetchConfig)
            let json = await response.json()
            let result = await json
            if(result.success)
                this.handleNote.value = true
            else
                this.handleNote.value =  result.message
        }
        catch(error){
            this.handleNote.value = 'Error: ' + error
        }
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
}

export default NoteService