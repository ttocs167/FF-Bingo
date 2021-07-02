<template>
  <v-app>
    <v-layout column>
      <v-container>
        <v-flex xs6 offset-xs3>
            <div class="white elevation-2">
              <v-toolbar flat dense dark>
                <v-toolbar-title>Register</v-toolbar-title>
              </v-toolbar>

              <div class="pl-4 pr-4 pt-2 pb-2">
                <v-container>
                  <v-text-field
                    dense
                    label="Email"
                    required
                    v-model="email"
                  ></v-text-field>
                  <br>
                  <v-text-field
                    dense
                    label="Password"
                    required
                    v-model="password"
                  ></v-text-field>
                  <br>
                  <v-flex class="error" v-html="error" />
                  <br>
                  <v-btn dark
                    @click="register">
                    Register
                  </v-btn>
                </v-container>
              </div>
            </div>
        </v-flex>
      </v-container>
    </v-layout>
  </v-app>
</template>

<script>
import AuthenticationService from '@/services/AuthenticationService'
export default {
  data () {
    return {
      email: '',
      password: '',
      error: null
    }
  },
  methods: {
    async register () {
      try {
        await AuthenticationService.register({
          email: this.email,
          password: this.password
        })
      } catch (error) {
        this.error = error.response.data.error
      }
    }
  }
}
</script>

<style scoped>

</style>
