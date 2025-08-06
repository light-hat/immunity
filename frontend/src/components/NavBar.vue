<script>
import {computed} from 'vue';
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'NavBar',
  computed: {
    ...mapGetters(['user', 'loading']),
  },
  methods: {
    ...mapActions([
      'logout'
    ]),
    async handleLogout() {
      try {
        await this.logout();
        // Redirect to login page after successful logout
        this.$router.push('/login');
      } catch (error) {
        console.error('Logout error:', error);
        // Even if logout fails, clear local state and redirect
        this.$store.commit('removeToken');
        this.$router.push('/login');
      }
    }

  }
}
</script>

<template>
    <div class="uk-background-secondary"> 
        <nav class="uk-navbar-container uk-navbar-transparent uk-light">
            <div style="margin-left: 3em; margin-right: 3em;">
                <div uk-navbar>

                    <div class="uk-navbar-left">

                        <img src="../assets/favicon_white.png"
                        alt=""
                        width="40"
                        height="40">

                        <p style="letter-spacing: 8px;">IMMUNITY</p>

                    </div>

                    <div class="uk-navbar-right">

                        <ul class="uk-navbar-nav" >
                            <li>
                                <router-link to="/" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right" uk-icon="icon: home"></span>
                                    <span>Dashboard</span>
                                </router-link>
                            </li>
                            
                        </ul>
                        
                    </div>

                    <div class="uk-navbar-right">

                        <ul class="uk-navbar-nav">
                            <li v-if="user" class="uk-parent">
                                <a href="#" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right" uk-icon="icon: user"></span>
                                    <span>{{ user.username.toUpperCase() }}</span>
                                    <span uk-icon="icon: chevron-down"></span>
                                </a>
                                <div v-if="showUserDropdown" class="uk-dropdown uk-dropdown-bottom-right">
                                    <ul class="uk-nav uk-dropdown-nav">
                                        <li>
                                            <router-link to="/account">
                                                <span class="uk-icon uk-margin-small-right" uk-icon="icon: cog"></span>
                                                <span>Account Settings</span>
                                            </router-link>
                                        </li>
                                        <li class="uk-nav-divider"></li>
                                        <li>
                                            <a href="#" @click.prevent="handleLogout">
                                                <span class="uk-icon uk-margin-small-right" uk-icon="icon: sign-out"></span>
                                                <span>Logout</span>
                                            </a>
                                        </li>
                                    </ul>
                                </div>
                            </li>
                        </ul>

                    </div>

                </div>
            </div>
        </nav>
    </div>
</template>

<style scoped>
nav {
    margin-bottom: 2em;
}

.img {
    margin-top: 1em;
}
</style>
