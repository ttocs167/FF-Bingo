<template>
  <v-app>
    <v-layout column>
      <v-container>
        <v-flex xs6 offset-xs3>
            <v-card flat dark>
              <v-toolbar flat dense>
                <v-toolbar-title>Register</v-toolbar-title>
              </v-toolbar>

              <div class="pl-4 pr-4 pt-2 pb-2">
                <v-container dark>
                  <v-text-field dark
                    dense
                    label="Email"
                    required
                    v-model="email"
                    color="white"
                  ></v-text-field>
                  <br>
                  <v-text-field dark
                    dense
                    label="Password"
                    required
                    v-model="password"
                    color="white"
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
            </v-card>
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
