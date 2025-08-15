<script>
import {ref, onMounted} from 'vue';
import {mapActions, mapGetters} from 'vuex';

export default {
  name: 'ProjectsView',
  data() {
    return {
      showUserDropdown: false,
    };
  },
  computed: {
    ...mapGetters(['user', 'isAuthenticated']),
  },
  methods: {
    ...mapActions(['getCurrentUser', 'logout']),
    async handleLogout() {
      await this.logout();
      this.$router.push('/login');
    },
    
    toggleDropdown() {
      this.showUserDropdown = !this.showUserDropdown;
    },
    
    // Handle dropdown visibility
    showDropdown() {
      const dropdown = document.querySelector('.advanced-dropdown');
      if (dropdown) {
        dropdown.classList.add('uk-open');
      }
    },
    
    hideDropdown() {
      const dropdown = document.querySelector('.advanced-dropdown');
      if (dropdown) {
        dropdown.classList.remove('uk-open');
      }
    },
    
    handleClickOutside(event) {
      const dropdown = document.querySelector('.simple-dropdown');
      const userLink = document.querySelector('.user-link');
      
      if (dropdown && userLink && !dropdown.contains(event.target) && !userLink.contains(event.target)) {
        this.showUserDropdown = false;
      }
    }
  },
  async mounted() {
    if (this.isAuthenticated && !this.user) {
      await this.getCurrentUser();
    }
    
    // Add click outside handler to close dropdown
    document.addEventListener('click', this.handleClickOutside);
  },
  
  beforeUnmount() {
    // Remove click outside handler
    document.removeEventListener('click', this.handleClickOutside);
  },
};
</script>
<template>
    <div id="create_project_modal" uk-modal>
        <div class="uk-modal-dialog">
            <button class="uk-modal-close-full uk-close-large" type="button" uk-close></button>

            <div class="uk-modal-header">
                <h2>Добавить проект</h2>
            </div>

            <form @submit.prevent="handleCreateProject">

                <div class="uk-modal-body">
                    <div class="uk-margin">
                        <input v-model="name"
                              type="text"
                              placeholder="Название проекта"
                              class="uk-input "
                              required />
                    </div>

                    <div class="uk-margin">
                        <textarea v-model="description"
                              placeholder="Описание"
                              type="text"
                              class="uk-textarea"
                              required />
                    </div>

                    <div class="uk-margin">
                        <select v-model="language" type="text" class="uk-select" placeholder="Язык программирования">
                            <option value="python">Python</option>
                        </select>
                    </div>

                </div>

                <div class="uk-modal-footer uk-text-right">
                    <div class="uk-navbar">
                        <div class="uk-navbar-left">
                            <button class="uk-button uk-button-default uk-modal-close" type="button">Cancel</button>
                        </div>
                        <div class="uk-navbar-right">
                            <button class="uk-button uk-button-secondary" type="submit" :disabled="loading">Создать</button>
                        </div>
                    </div>
                </div>

            </form>

        </div>
    </div>
    <div class="uk-container uk-container-xlarge">
        <div class="uk-navbar">
            <div class="uk-navbar-left">
                <h2 v-if="projects.length > 0">
                    <span class="uk-icon uk-margin-small-right"
                        uk-icon="icon: server; ratio: 2">
                    </span>
                    Проекты ({{ projects.length }})
                </h2>
                <h2 v-else>
                    <span class="uk-icon uk-margin-small-right"
                        uk-icon="icon: server; ratio: 2">
                    </span>
                    Проекты (0)
                </h2>
            </div>
            <div class="uk-navbar-right">
                <a href="#create_project_modal" class="uk-button uk-button-secondary" uk-toggle>
                    <span class="uk-icon uk-margin-small-right"
                        uk-icon="icon: plus">
                    </span>
                    Добавить проект
                </a>
            </div>
        </div>

        <table class="uk-table uk-table-middle uk-table-divider">
            <thead>
                <tr>
                    <th>Название проекта</th>
                    <th class="uk-center">Язык программирования</th>
                    <th class="uk-center">Статус</th>
                    <th class="uk-center">Последнее взаимодействие</th>
                    <th class="uk-center">Дата подключения</th>
                </tr>
            </thead>
            <tbody>

                <tr v-for="project in projects" :key="project.id">
                    <td>
                        <router-link :to="{ name: 'application_detail', params: { id: project.id } }" class="uk-button uk-button-text">{{ project.name }}</router-link>
                    </td>
                    <td class="uk-center">
                        <span class="uk-label uk-label-default">
                            {{ project.language }}
                        </span>
                    </td>
                    <td class="uk-center">
                        <span v-if="project.online" class="uk-label uk-label-success">
                            Online
                        </span>
                        <p v-else>
                            Offline
                        </p>
                    </td>
                    <td class="uk-center">{{ project.created_at }}</td>
                    <td class="uk-center">{{ project.last_online }}</td>
                </tr>

            </tbody>
        </table>

    </div>
</template>

<style scoped>
    .uk-center {
        text-align: center;
    }
</style>
