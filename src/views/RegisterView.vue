<script setup>
import { ref } from 'vue'
import LoginService from '@/services/LoginService.js'

const username = ref('')
const password = ref('')
const email = ref('')

const registerError = ref('')
const loginService = new LoginService()

const TryRegister = async () => {
  const registerResult = loginService.GetRegisterResult()
  await loginService.TryRegister(username.value, password.value, email.value)
  if (registerResult.value.success){
    alert(registerResult.value.message)
    window.location.href = '/'
  }
  else{
    registerError.value = registerResult.value.message
  }
}
</script>

<template>
  <div class="container flex-column">
    <h1>Registro</h1>
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
        <label for="email">Correo</label>
        <input type="email" id="email" v-model="email">
      </div>

      <div class="form-item">
        <button @click="TryRegister">Acceder</button>
      </div>

      <div v-if="registerError !==''" class="form-item">
        <h2 class="red">{{ registerError }}</h2>
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