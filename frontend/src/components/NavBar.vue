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
    <div class="uk-background-primary"> 
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

                        <ul class="uk-navbar-nav" v-if="user">


                            <li class="uk-active" v-if="$route.path === '/'">
                                <router-link to="/" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right" uk-icon="icon: home"></span>
                                    <span>Dashboard</span>
                                </router-link>
                            </li>
                            <li v-else>
                                <router-link to="/" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right" uk-icon="icon: home"></span>
                                    <span>Dashboard</span>
                                </router-link>
                            </li>
                            

                            <li class="uk-active" v-if="$route.path === '/projects'">
                                <router-link to="/projects" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: album">
                                    </span>
                                    Projects
                                    <span class="uk-badge">0</span>
                                </router-link>
                            </li>
                            <li v-else>
                                <router-link to="/projects" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: album">
                                    </span>
                                    Projects
                                    <span class="uk-badge">0</span>
                                </router-link>
                            </li>
                            

                            <!--<li class="uk-active" v-if="$route.path === '/agents'">
                                <router-link to="/agents" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: server">
                                    </span>
                                    Agents
                                    <span class="uk-badge">0</span>
                                </router-link>
                            </li>
                            <li v-else>
                                <router-link to="/agents" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: server">
                                    </span>
                                    Agents
                                    <span class="uk-badge">0</span>
                                </router-link>
                            </li>
                            
                            <li class="uk-active" v-if="$route.path === '/tests'">
                                <router-link to="/tests" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: play-circle">
                                    </span>
                                    Test cases
                                    <span class="uk-badge">0</span>
                                </router-link>
                            </li>
                            <li v-else>
                                <router-link to="/tests" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: play-circle">
                                    </span>
                                    Test cases
                                    <span class="uk-badge">0</span>
                                </router-link>
                            </li>
                            
                            <li class="uk-active" v-if="$route.path === '/vulns'">
                                <router-link to="/vulns" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: warning">
                                    </span>
                                    Vulnerabilities
                                    <span class="uk-badge">0</span>
                                </router-link>
                            </li>
                            <li v-else>
                                <router-link to="/vulns" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: warning">
                                    </span>
                                    Vulnerabilities
                                    <span class="uk-badge">0</span>
                                </router-link>
                            </li>
                            
                            <li class="uk-active" v-if="$route.path === '/reports'">
                                <router-link to="/reports" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: file-pdf">
                                    </span>
                                    Reports
                                    <span class="uk-badge">0</span>
                                </router-link>
                            </li>
                            <li v-else>
                                <router-link to="/reports" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: file-pdf">
                                    </span>
                                    Reports
                                    <span class="uk-badge">0</span>
                                </router-link>
                            </li>
                            
                            <li class="uk-active" v-if="$route.path === '/policy'">
                                <router-link to="/policy" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: settings">
                                    </span>
                                    Policy
                                </router-link>
                            </li>
                            <li v-else>
                                <router-link to="/policy" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: settings">
                                    </span>
                                    Policy
                                </router-link>
                            </li>
                            
                            <li class="uk-active" v-if="$route.path === '/sbom'">
                                <router-link to="/sbom" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: cloud-download">
                                    </span>
                                    SBOM
                                </router-link>
                            </li>
                            <li v-else>
                                <router-link to="/sbom" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: cloud-download">
                                    </span>
                                    SBOM
                                </router-link>
                            </li>
                            
                            <li class="uk-active" v-if="$route.path === '/tm'">
                                <router-link to="/tm" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: bolt">
                                    </span>
                                    Threat Modeling
                                </router-link>
                            </li>
                            <li v-else>
                                <router-link to="/tm" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: bolt">
                                    </span>
                                    Threat Modeling
                                </router-link>
                            </li>
                            
                            <li class="uk-active" v-if="$route.path === '/copilot'">
                                <router-link to="/copilot" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: commenting">
                                    </span>
                                    CoPilot
                                </router-link>
                            </li>
                            <li v-else>
                                <router-link to="/copilot" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: commenting">
                                    </span>
                                    CoPilot
                                </router-link>
                            </li>-->

                        </ul>
                        
                    </div>

                    <div class="uk-navbar-right">

                        <div class="uk-navbar-item" v-if="user">
                            <form class="uk-search uk-search-navbar">
                                <span uk-search-icon></span>
                                <input class="uk-search-input" type="search" placeholder="Search...">
                            </form>
                        </div>

                        <ul class="uk-navbar-nav" v-if="user">

                            <li class="uk-active uk-parent" v-if="$route.path === '/account'">
                                <a href="#" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right" uk-icon="icon: user"></span>
                                    <span>{{ user.username.toUpperCase() }}</span>
                                    <span uk-icon="icon: chevron-down"></span>
                                </a>
                                <div class="uk-dropdown uk-dropdown-bottom-right" uk-dropdown>
                                    <ul class="uk-nav uk-dropdown-nav">
                                        <li class="uk-active">
                                            <router-link to="/account">
                                                <span class="uk-icon uk-margin-small-right" uk-icon="icon: cog"></span>
                                                <span>Account Settings</span>
                                            </router-link>
                                        </li>
                                        <li>
                                            <a href="https://light-hat.github.io/immunity/">
                                                <span class="uk-icon uk-margin-small-right" uk-icon="icon: file-text"></span>
                                                <span>Docs</span>
                                            </a>
                                        </li>
                                        <li>
                                            <a href="https://github.com/light-hat/immunity">
                                                <span class="uk-icon uk-margin-small-right" uk-icon="icon: github"></span>
                                                <span>GitHub</span>
                                            </a>
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
                            <li class="uk-parent" v-else>
                                <a href="#" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right" uk-icon="icon: user"></span>
                                    <span>{{ user.username.toUpperCase() }}</span>
                                    <span uk-icon="icon: chevron-down"></span>
                                </a>
                                <div class="uk-dropdown uk-dropdown-bottom-right" uk-dropdown>
                                    <ul class="uk-nav uk-dropdown-nav">
                                        <li>
                                            <router-link to="/account">
                                                <span class="uk-icon uk-margin-small-right" uk-icon="icon: cog"></span>
                                                <span>Account Settings</span>
                                            </router-link>
                                        </li>
                                        <li>
                                            <a href="https://light-hat.github.io/immunity/">
                                                <span class="uk-icon uk-margin-small-right" uk-icon="icon: file-text"></span>
                                                <span>Docs</span>
                                            </a>
                                        </li>
                                        <li>
                                            <a href="https://github.com/light-hat/immunity">
                                                <span class="uk-icon uk-margin-small-right" uk-icon="icon: github"></span>
                                                <span>GitHub</span>
                                            </a>
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
                        <ul class="uk-navbar-nav" v-else>
                            <li>
                                <a href="https://light-hat.github.io/immunity/" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right" uk-icon="icon: file-text"></span>
                                    <span>Docs</span>
                                </a>
                            </li>
                            <li>
                                <a href="https://github.com/light-hat/immunity" class="uk-navbar-item">
                                    <span class="uk-icon uk-margin-small-right" uk-icon="icon: github"></span>
                                    <span>Github</span>
                                </a>
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
