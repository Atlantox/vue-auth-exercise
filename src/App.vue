<script setup>
  import useSessionStore from '@/stores/session.js'
  const sessionStore = useSessionStore()
</script>

<template>
    <section class="container">
      <div class="route-container">
        <router-link :to="{name: 'home'}">Inicio</router-link>
      </div>
      <div v-if="sessionStore.token === ''" class="route-container">
        <router-link :to="{name: 'login'}">Login</router-link>
      </div>
      <div v-if="sessionStore.token === ''" class="route-container">
        <router-link :to="{name: 'register'}">Registro</router-link>
      </div>
      <div v-if="sessionStore.token !== ''" class="route-container">
        <router-link :to="{name: 'notes'}">Notas</router-link>
      </div>
      <div v-if="sessionStore.token !== ''" class="route-container">
        <router-link :to="{name: 'profile'}">Perfil</router-link>
      </div>
      <div v-if="sessionStore.token !== ''" class="route-container">
        <button @click="sessionStore.DestroySession()">Cerrar sesión</button>
      </div>
    </section>

    <main class="container">
      <router-view></router-view>
    </main>
</template>

<style scoped>
.route-container{
  margin: 0 15px;
}
</style>