<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import NoteService from '@/services/NoteService.js'

const noteService = new NoteService()
const targetNote = noteService.GetSingleNote()

const error = ref('')
const title = ref('')
const content = ref('')
let id = ''
const route = useRoute()
let edit = route.params.id !== undefined
if(edit === true)
    id = route.params.id

onMounted(async () => {
    if(edit === true){
        await noteService.FetchSingleNote(route.params.id)
        if(targetNote.value.success === true){
            title.value = targetNote.value.note.titulo
            content.value = targetNote.value.note.contenido
        }
        else{
            window.location.href = '/'
        }
    }
})

const HandleNote = (async () => {
    const handleResult = noteService.GetHandleNoteResult()
    const data = {
        'title': title.value,
        'content': content.value
    }
    if(edit === true)
        data['id'] = id

    await noteService.HandleNote(data)
    if(handleResult.value === true){
        alert('Nota ' + (edit === true ? 'editada' : 'creada') + ' correctamente')
        if(edit === false){
            title.value = ''
            content.value = ''
        }
        else{
            noteService.FetchSingleNote(id)
        }
    }
    else{
        error.value = handleResult.value.message
    }
})

</script>

<template>
    <table>
        <tr>
            <td>Título:</td>
            <td><input type="text" v-model="title"></td>
        </tr>
        <tr>
            <td>Contenido:</td>
            <td><input type="text" v-model="content"></td>
        </tr>
        <tr v-if="edit === true && targetNote !== ''">
            <td>Creado:</td>
            <td>{{ targetNote.note.fecha_creacion }}</td>
        </tr>
        <tr>
            <td colspan="2">
                <button @click="HandleNote">
                    {{ edit === false  ? 'Crear nota' : 'Editar nota' }}
                </button>
            </td>
        </tr>
    </table>
    <h1 v-if="error !== ''">{{ error }}</h1>    
</template>

<style scoped>

</style>
