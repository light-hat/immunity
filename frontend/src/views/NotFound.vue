<script>
import {ref, onMounted} from 'vue';
import {mapActions, mapGetters} from 'vuex';

export default {
  name: 'DashboardView',
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
    <div class="uk-container uk-container-expand uk-margin-top uk-position-center uk-center">
        <h3>404 - Not Found</h3>
        <p class="center">Incorrect Url.</p>
    </div>
</template>

<style>
.center {
    text-align: center;
}
</style>
