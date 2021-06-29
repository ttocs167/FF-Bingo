<template>
  <div>
  <h1>Register</h1>

  <input
    type="email"
    name="email"
    v-model="email"
    placeholder="email" />
  <br>
  <input
    type="password"
    name="password"
    v-model="password"
    placeholder="password" />
  <br>
  <button
    @click="register">
    Register
  </Button>
  </div>
</template>

<script>
import AuthenticationService from '@/services/AuthenticationService'
export default {
  data () {
    return {
    }
  },
  methods: {
    async register () {
      const response = await AuthenticationService.register({
        email: this.email,
        password: this.password
      })
      console.log(response.data)
    }
  }
}
</script>

<style scoped>

</style>
