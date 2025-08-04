<script>
import {ref, onMounted} from 'vue';
import {mapActions, mapGetters} from 'vuex';
import {AgCharts} from 'ag-charts-vue3';

export default {
  name: 'DashboardView',
  components: {
    'ag-charts': AgCharts,
  },
  data() {
    return {
      showUserDropdown: false,
    };
  },
  setup() {
    const options = ref({
      data: [
        {month: 'Jan', avgTemp: 2.3, iceCreamSales: 162000},
        {month: 'Mar', avgTemp: 6.3, iceCreamSales: 302000},
        {month: 'May', avgTemp: 16.2, iceCreamSales: 800000},
        {month: 'Jul', avgTemp: 22.8, iceCreamSales: 1254000},
        {month: 'Sep', avgTemp: 14.5, iceCreamSales: 950000},
        {month: 'Nov', avgTemp: 8.9, iceCreamSales: 200000},
      ],
      series: [{type: 'bar', xKey: 'month', yKey: 'iceCreamSales'}],
    });
    return {
      options,
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
  <div>
    <!-- Enhanced Navigation Header -->
    <nav class="uk-navbar-container advanced-navbar" uk-navbar>
      <div class="uk-navbar-left">
        <div class="nav-brand">
          <span uk-icon="icon: shield; ratio: 1.5" class="brand-icon"></span>
          <span class="brand-text">IMMUNITY</span>
        </div>
        <ul class="uk-navbar-nav advanced-nav">
          <li class="uk-active">
            <a href="#" class="nav-link nav-link-active">
              <span uk-icon="icon: home; ratio: 1.2" class="nav-icon"></span>
              <span class="nav-text">DASHBOARD</span>
            </a>
          </li>
          <li>
            <router-link to="/account" class="nav-link">
              <span uk-icon="icon: user; ratio: 1.2" class="nav-icon"></span>
              <span class="nav-text">ACCOUNT SETTINGS</span>
            </router-link>
          </li>
        </ul>
      </div>
      
      <div class="uk-navbar-right">
        <ul class="uk-navbar-nav">
          <li v-if="user" class="user-menu">
            <div class="user-link" @click="toggleDropdown" :style="{ backgroundColor: showUserDropdown ? 'rgba(255, 255, 255, 0.3)' : 'rgba(255, 255, 255, 0.1)' }">
              <div class="user-avatar">
                <span uk-icon="user" class="avatar-icon"></span>
              </div>
              <span class="username">{{ user.username.toUpperCase() }}</span>
              <span uk-icon="chevron-down" class="dropdown-icon"></span>
            </div>
            <div v-if="showUserDropdown" class="simple-dropdown">
              <div class="dropdown-item">
                <router-link to="/account" class="dropdown-link">
                  <span uk-icon="cog" class="dropdown-icon"></span>
                  <span>Account Settings</span>
                </router-link>
              </div>
              <div class="dropdown-divider"></div>
              <div class="dropdown-item">
                <a href="#" @click.prevent="handleLogout" class="dropdown-link logout-link">
                  <span uk-icon="sign-out" class="dropdown-icon"></span>
                  <span>Logout</span>
                </a>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </nav>

    <!-- Dashboard Content -->
    <div class="uk-container uk-container-expand uk-margin-top">
      <div class="uk-child-width-1-3@m uk-grid-small uk-grid-match" uk-grid>

        <div>
          <div class="uk-card uk-card-default uk-card-hover uk-card-body">
            <h3 class="uk-card-title">
              Vulnerability Types in Applications
            </h3>
            <ag-charts :options="options"/>
          </div>
        </div>

        <div>
          <div class="uk-card uk-card-default uk-card-hover uk-card-body">
            <h3 class="uk-card-title">Security Metrics</h3>
            <ag-charts :options="options"/>
          </div>
        </div>

        <div>
          <div class="uk-card uk-card-default uk-card-hover uk-card-body">
            <h3 class="uk-card-title">Risk Assessment</h3>
            <ag-charts :options="options"/>
          </div>
        </div>

        <div>
          <div class="uk-card uk-card-default uk-card-hover uk-card-body">
            <h3 class="uk-card-title">Scan Results</h3>
            <ag-charts :options="options"/>
          </div>
        </div>

        <div>
          <div class="uk-card uk-card-default uk-card-hover uk-card-body">
            <h3 class="uk-card-title">Performance Metrics</h3>
            <ag-charts :options="options"/>
          </div>
        </div>

        <div>
          <div class="uk-card uk-card-default uk-card-hover uk-card-body">
            <h3 class="uk-card-title">System Status</h3>
            <ag-charts :options="options"/>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
/* Advanced Navigation Styling */
.advanced-navbar {
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  border-bottom: 3px solid #1e87f0;
  position: relative;
  overflow: visible !important;
  z-index: 1000 !important;
}

.advanced-navbar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #1e87f0, #0f7ae5, #1e87f0);
  background-size: 200% 100%;
  animation: shimmer 3s ease-in-out infinite;
}

/* Force blue colors on all navigation elements */
.advanced-navbar * {
  color: #ffffff !important;
}

.advanced-nav > li > a,
.advanced-nav > li > .nav-link {
  color: #ffffff !important;
}

.nav-link {
  color: #ffffff !important;
}

.nav-icon {
  color: #ffffff !important;
}

.nav-text {
  color: #ffffff !important;
}

.username {
  color: #ffffff !important;
}

.dropdown-icon {
  color: #ffffff !important;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

/* Brand Styling */
.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 1rem;
  margin-right: 2rem;
}

.brand-icon {
  color: #ffffff;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

.brand-text {
  font-size: 1.5rem;
  font-weight: 800;
  color: #ffffff !important;
  letter-spacing: 2px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  /* Remove the gradient text effect that was making it transparent */
  /* background: linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text; */
}

/* Advanced Navigation Links */
.advanced-nav {
  display: flex;
  gap: 1rem;
}

.advanced-nav > li > a,
.advanced-nav > li > .nav-link {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 0.75rem 1.5rem;
  margin: 0.5rem 0.25rem;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.advanced-nav > li > a::before,
.advanced-nav > li > .nav-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.advanced-nav > li > a:hover::before,
.advanced-nav > li > .nav-link:hover::before {
  left: 100%;
}

.advanced-nav > li > a:hover,
.advanced-nav > li > .nav-link:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
}

/* Active Navigation Link */
.advanced-nav > li.uk-active > a,
.advanced-nav > li.uk-active > .nav-link-active {
  background: linear-gradient(135deg, #1e87f0 0%, #0f7ae5 100%);
  border-color: #ffffff;
  box-shadow: 0 8px 20px rgba(30, 135, 240, 0.4);
  transform: translateY(-2px);
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #ffffff;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.nav-icon {
  color: #ffffff;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.3));
}

.nav-text {
  font-weight: 700;
  letter-spacing: 1px;
}

/* User Menu Styling */
.user-menu {
  position: relative;
  z-index: 1001 !important;
}

.user-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  margin: 0.5rem 0.25rem;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  backdrop-filter: blur(10px);
  color: #ffffff;
  text-decoration: none;
}

.user-link:hover {
  background: rgba(255, 255, 255, 0.3) !important;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1e87f0 0%, #0f7ae5 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(30, 135, 240, 0.3);
}

.avatar-icon {
  color: #ffffff;
  font-size: 0.9rem;
}

.username {
  font-weight: 600;
  font-size: 0.9rem;
  letter-spacing: 0.5px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.dropdown-icon {
  color: #ffffff;
  transition: transform 0.3s ease;
}

.user-link:hover .dropdown-icon {
  transform: rotate(180deg);
}

/* Advanced Dropdown Styling */
.advanced-dropdown {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(15px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
  padding: 0.5rem 0;
  min-width: 200px;
  margin-top: 0.5rem;
  position: absolute;
  top: 100%;
  right: 0;
  z-index: 9999;
}

.uk-dropdown-nav {
  margin: 0;
  padding: 0;
  list-style: none;
}

.dropdown-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  color: #333;
  text-decoration: none;
  transition: all 0.3s ease;
  font-weight: 500;
  border-radius: 8px;
  margin: 0.25rem 0.5rem;
}

.dropdown-link:hover {
  background: rgba(30, 135, 240, 0.1);
  color: #1e87f0;
  transform: translateX(5px);
  text-decoration: none;
}

.dropdown-link .dropdown-icon {
  color: #666;
  transition: color 0.3s ease;
  width: 16px;
  height: 16px;
}

.dropdown-link:hover .dropdown-icon {
  color: #1e87f0;
}

.logout-link {
  color: #dc3545 !important;
  font-weight: 600;
  text-shadow: none;
  background: transparent;
}

.logout-link:hover {
  color: #dc3545 !important;
  background: rgba(220, 53, 69, 0.05);
}

.logout-link:hover .dropdown-icon {
  transform: scale(1.1);
  color: #dc3545 !important;
}

/* Ensure dropdown is visible */
.uk-dropdown {
  display: none;
  z-index: 9999;
  position: absolute;
  top: 100%;
  right: 0;
}

.uk-dropdown.uk-open {
  display: block;
}

/* User menu positioning */
.user-menu {
  position: relative;
}

.user-menu .uk-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  z-index: 9999;
}

/* Ensure dropdown appears outside navbar */
.uk-navbar-container {
  position: relative;
  z-index: 1000;
  overflow: visible !important;
}

/* Add hover functionality back - more specific rules */
.user-menu:hover .uk-dropdown,
.user-menu:hover .advanced-dropdown {
  display: block !important;
  visibility: visible !important;
  opacity: 1 !important;
}

.user-link:hover + .uk-dropdown,
.user-link:hover + .advanced-dropdown {
  display: block !important;
  visibility: visible !important;
  opacity: 1 !important;
}

/* Force dropdown visibility on hover */
.user-menu:hover .uk-dropdown.uk-dropdown-bottom-right {
  display: block !important;
  visibility: visible !important;
  opacity: 1 !important;
}

/* Additional hover rules */
.user-menu:hover .advanced-dropdown {
  display: block !important;
}

.user-link:hover ~ .advanced-dropdown {
  display: block !important;
}

/* Simple dropdown visibility */
.user-menu:hover .advanced-dropdown {
  display: block !important;
  visibility: visible !important;
  opacity: 1 !important;
}

/* Clean up test styles and ensure visibility */
.advanced-dropdown {
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(15px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
  padding: 0.5rem 0;
  min-width: 200px;
  margin-top: 0.5rem;
  position: absolute;
  top: 100%;
  right: 0;
  z-index: 99999 !important;
  display: none;
}

/* Ensure dropdown is visible when uk-open class is applied */
.advanced-dropdown.uk-open {
  display: block !important;
  visibility: visible !important;
  opacity: 1 !important;
  background: #ffffff !important; /* Temporary white background for visibility */
  border: 2px solid #1e87f0 !important; /* Blue border for visibility */
}

/* Force dropdown to be visible when open */
.uk-dropdown.uk-open {
  display: block !important;
  visibility: visible !important;
  opacity: 1 !important;
}

/* Responsive Design */
@media (max-width: 959px) {
  .nav-brand {
    margin-right: 1rem;
  }
  
  .brand-text {
    font-size: 1.2rem;
  }
  
  .advanced-nav {
    gap: 0.5rem;
  }
  
  .advanced-nav > li > a,
  .advanced-nav > li > .nav-link {
    padding: 0.5rem 1rem;
    font-size: 0.8rem;
  }
  
  .nav-text {
    display: none;
  }
  
  .nav-icon {
    font-size: 1.1rem;
  }
}

@media (max-width: 639px) {
  .nav-brand {
    margin-right: 0.5rem;
  }
  
  .brand-text {
    font-size: 1rem;
  }
  
  .user-link {
    padding: 0.5rem 1rem;
  }
  
  .username {
    display: none;
  }
}

/* Simple dropdown styling */
.simple-dropdown {
  position: absolute !important;
  top: calc(100% + 15px) !important;
  right: 0 !important;
  background: transparent;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  min-width: 240px;
  z-index: 99999 !important;
  animation: dropdownSlideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

@keyframes dropdownSlideIn {
  from {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.dropdown-item {
  padding: 16px 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  background: transparent;
}

.dropdown-item:last-child {
  border-bottom: none;
}

.dropdown-item::before {
  display: none;
}

.dropdown-item:hover::before {
  display: none;
}

.dropdown-item:hover {
  background: rgba(30, 135, 240, 0.04);
  transform: translateX(3px);
}

.dropdown-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0, 0, 0, 0.1), transparent);
  margin: 8px 16px;
}

.dropdown-link {
  display: flex;
  align-items: center;
  gap: 14px;
  color: #000000 !important;
  text-decoration: none;
  font-size: 16px;
  font-weight: 600;
  position: relative;
  z-index: 1;
  transition: all 0.2s ease;
  padding: 4px 0;
  letter-spacing: 0.3px;
  text-shadow: none;
  background: transparent;
}

.dropdown-link:hover {
  color: #1e87f0;
  text-decoration: none;
  transform: translateX(2px);
}

.dropdown-link .dropdown-icon {
  width: 20px;
  height: 20px;
  transition: all 0.2s ease;
  color: #1e87f0;
  flex-shrink: 0;
}

.dropdown-link:hover .dropdown-icon {
  transform: scale(1.1);
  color: #1e87f0;
}

.logout-link {
  color: #dc3545;
}

.logout-link:hover {
  color: #dc3545;
}

.logout-link:hover .dropdown-icon {
  transform: scale(1.1) rotate(5deg);
}

/* Enhanced user menu positioning */
.user-menu {
  position: relative;
}

.user-link {
  cursor: pointer;
  transition: all 0.3s ease;
}

.user-link:hover {
  transform: translateY(-1px);
}

/* Ensure dropdown appears above all other elements */
.uk-navbar-container {
  position: relative;
  z-index: 1000;
}

.simple-dropdown {
  z-index: 10000;
}
</style>

