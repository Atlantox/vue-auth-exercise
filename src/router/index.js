import { createRouter, createWebHistory } from 'vue-router'
import useSessionStore  from '@/stores/session.js'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import NotesView from '../views/NotesView.vue'
import ProfileView from '../views/ProfileView.vue'
import NoteForm from '../views/NoteForm.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {requireAuth: false, denyIfAuth: false}
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: {requireAuth: false, denyIfAuth: true}
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: {requireAuth: false, denyIfAuth: true}
    },
    {
      path: '/notes',
      name: 'notes',
      component: NotesView,
      meta: {requireAuth: true, denyIfAuth: false}
    },
    {
      path: '/noteForm/:id?',
      name: 'noteForm',
      component: NoteForm,
      meta: {requireAuth: true, denyIfAuth: false}
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: {requireAuth: true, denyIfAuth: false}
    },
  ]
})

router.beforeEach((to, from, next) => {
  const sessionStore = useSessionStore()
  var userLogged = true
  if(sessionStore.token === '') userLogged = false
  var requiredAuth = to.meta.requireAuth
  var denyIfAuth = to.meta.denyIfAuth

  if(requiredAuth && !userLogged)
    next({name: 'login'})
  else if(userLogged && denyIfAuth)
    next({name: 'home'})
  else{
    next()  
  }
}) 

export default router
