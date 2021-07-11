<template>
  <v-app id="app">
    <v-app-bar
      app
      prominent
    >
      <v-img :src="require('@/assets/Sophia_Happy.png')"
      max-width="123px"
      max-height="123px"
      contain
      />
      <v-toolbar-title>BingoBot</v-toolbar-title>

    </v-app-bar>

    <v-main>
      <v-container fluid>
          <v-row
          v-for="k in 5"
          :key="k"
          cols=1
          no-gutters
          align="center"
          justify="center">
            <v-col
              v-for="n in 5"
              :key="n"
              cols="1"
              no-gutters
            >
              <v-card
              aspect-ratio="1/1"
              width="100%"
              outlined>
                <v-responsive :aspect-ratio="1/1">
                  <v-card-actions>
                    <v-btn block tile>
                      CARD
                    </v-btn>
                  </v-card-actions>
                </v-responsive>
              </v-card>
            </v-col>
          </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
}
</script>

<style scoped>

</style>
