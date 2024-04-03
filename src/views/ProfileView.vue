<script setup>
import { ref } from 'vue'
import LoginService from '@/services/LoginService.js'
import useSessionStore from '@/stores/session.js'

const sessionStore = useSessionStore()
const username = ref('')
const password = ref('')
const loginError = ref('')
const loginService = new LoginService()

const TryLogin = async () => {
  const loginResult = loginService.getLoginResult()
  await loginService.TryLogin(username.value, password.value)
  if (loginResult.value.success){
    // Registra los datos de sesión
    sessionStore.token = loginResult.value['token']
    window.location.href = '/'
  }
  else{
    loginError.value = loginResult.value['message']
  }
}
</script>

<template>
  <div class="container flex-column">
    <h1>Login</h1>
    <div class="login-container">
      <div class="form-item">
        <label for="username">Usuario</label>
        <input type="text" id="username" v-model="username">
      </div>
      
      <div class="form-item">
        <label for="password">Contraseña</label>
        <input type="password" id="password" v-model="password">
      </div>

      <div class="form-item">
        <button @click="TryLogin">Acceder</button>
      </div>

      <div v-if="loginError !==''" class="form-item">
        <h2 class="red">{{ loginError }}</h2>
      </div>

    </div>
  </div>
</template>

<style scoped>
h1, h2{
  width:100%;
  text-align: center;
}

.login-container{
  display:flex;
  flex-direction: column;
}

.form-item{
  width:100%;
  text-align: center;
  margin: 10px 0;
}

.form-item label{
  margin-right: 5px;
}

.red{
  color:red;
}
</style>