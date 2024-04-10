<script setup>
import { onMounted, ref } from 'vue'
import NoteCard from '@/components/NoteCard.vue'
import NoteService from '@/services/NoteService.js'

const error = ref('')
const noteService = new NoteService()
const notes = noteService.GetNotes()

onMounted(async () => {
    await noteService.FetchNotes()
    if(notes.value.success === false){
        error.value = notes.value.message
    }
})


</script>

<template>
    <h1>Gestión de notas</h1>
    <div class="container">
        <router-link :to="{name:'noteForm'}">Nueva nota</router-link>
    </div>
    <div class="container"
    v-if="notes.length > 0">
        <article
        v-for="(note, index) in notes"
        :key="index">
            <NoteCard
            :id = "note.id"
            :title = "note.titulo"
            :content = "note.contenido"
            :created = "note.fecha_creacion"
            ></NoteCard>
        </article>
    </div>
    <div
    v-else>
    <template 
    v-if="error === ''">
        <h4>No hay notas registradas</h4>
    </template>
    <template 
    v-else>
        <h4>{{ error }}</h4>
    </template>
    </div>
</template>

<style scoped>

</style>