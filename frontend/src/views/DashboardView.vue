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
    <!-- Dashboard Content -->
    <div class="uk-container uk-container-expand uk-margin-top uk-position-center uk-center">
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

<style>
</style>