<script setup>
import { ref } from 'vue'
import LoginService from '@/services/LoginService.js'
import useSessionStore from '@/stores/session.js'

const sessionStore = useSessionStore()

</script>

<template>
    <div class="container">
        <h1 class="w-100">Perfil</h1>
        <ul class="w-100">
            <li>Correo: {{ sessionStore.userData.email }} </li>
            <li>Usuario: {{ sessionStore.userData.username }} </li>
        </ul>
    </div>
</template>

<style scoped>

</style>