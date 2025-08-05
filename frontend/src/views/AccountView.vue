<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'AccountView',
  data() {
    return {
      passwordForm: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: '',
      },
      usernameForm: {
        currentUsername: '',
        newUsername: '',
        currentPassword: '',
      },
      emailForm: {
        currentEmail: '',
        newEmail: '',
        currentPassword: '',
      },
      passwordError: '',
      usernameError: '',
      emailError: '',
      passwordSuccess: '',
      usernameSuccess: '',
      emailSuccess: '',
      activeTab: 'profile', // profile, security, preferences
      preferences: {
        theme: 'auto', // 'light', 'dark', 'auto'
        colorScheme: 'blue', // 'blue', 'green', 'purple', 'orange', 'red'
        fontSize: 'medium', // 'small', 'medium', 'large'
        emailNotifications: true,
        browserNotifications: true,
        notifyScans: true,
        notifyVulnerabilities: true,
        notifyReports: true,
        analytics: true,
        sessionTimeout: '15', // '15', '30', '60', '120', '0'
        twoFactor: false,
      },
      timestampInterval: null, // To hold the interval ID for timestamp refresh
      mediaQuery: null, // To hold the media query listener for system theme changes
      showUserDropdown: false,
    };
  },
  computed: {
    ...mapGetters(['user', 'loading']),
    formattedDateJoined() {
      if (this.user && this.user.date_joined) {
        console.log('Raw date_joined:', this.user.date_joined);
        const date = new Date(this.user.date_joined);
        console.log('Parsed date:', date);
        console.log('Date validity:', !isNaN(date.getTime()));
        
        if (isNaN(date.getTime())) {
          return 'Invalid Date';
        }
        
        return date.toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
      }
      return 'N/A';
    },
    formattedLastLogin() {
      if (this.user && this.user.last_login) {
        console.log('Raw last_login:', this.user.last_login);
        const date = new Date(this.user.last_login);
        console.log('Parsed last_login date:', date);
        console.log('Last login date validity:', !isNaN(date.getTime()));
        
        if (isNaN(date.getTime())) {
          return 'Invalid Date';
        }
        
        return date.toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
      }
      return 'N/A';
    }
  },
  methods: {
    ...mapActions([
      'changePassword', 
      'changeUsername', 
      'changeEmail',
      'getCurrentUser',
      'getPreferences',
      'savePreferences',
      'resetPreferences',
      'exportPreferences',
      'importPreferences',
      'getUserStats',
      'logout'
    ]),
    
    async handlePasswordChange() {
      console.log('Password change button clicked');
      console.log('Current password length:', this.passwordForm.currentPassword?.length);
      console.log('New password length:', this.passwordForm.newPassword?.length);
      console.log('New password value:', this.passwordForm.newPassword);
      this.passwordError = '';
      this.passwordSuccess = '';
      
      if (!this.passwordForm.currentPassword || !this.passwordForm.newPassword) {
        this.passwordError = 'Please fill in all fields';
        return;
      }
      
      if (this.passwordForm.newPassword !== this.passwordForm.confirmPassword) {
        this.passwordError = 'New passwords do not match';
        return;
      }
      
      if (this.passwordForm.newPassword.length < 8) { // Changed back to 8 for production
        this.passwordError = 'New password must be at least 8 characters long';
        return;
      }
      
      const result = await this.changePassword({
        currentPassword: this.passwordForm.currentPassword,
        newPassword: this.passwordForm.newPassword,
      });
      
      if (result.success) {
        this.passwordSuccess = 'Password changed successfully! Redirecting to dashboard...';
        this.passwordForm = {
          currentPassword: '',
          newPassword: '',
          confirmPassword: '',
        };
        setTimeout(() => {
          this.$router.push('/');
        }, 1500);
      } else {
        this.passwordError = result.error;
      }
    },
    
    async handleUsernameChange() {
      console.log('Username change button clicked');
      this.usernameError = '';
      this.usernameSuccess = '';
      
      if (!this.usernameForm.currentUsername || !this.usernameForm.newUsername || !this.usernameForm.currentPassword) {
        this.usernameError = 'Please fill in all fields';
        return;
      }
      
      if (this.usernameForm.newUsername.length < 3) {
        this.usernameError = 'New username must be at least 3 characters long';
        return;
      }
      
      const result = await this.changeUsername({
        currentUsername: this.usernameForm.currentUsername,
        newUsername: this.usernameForm.newUsername,
        currentPassword: this.usernameForm.currentPassword,
      });
      
      if (result.success) {
        this.usernameSuccess = 'Username changed successfully! Redirecting to dashboard...';
        this.usernameForm = {
          currentUsername: '',
          newUsername: '',
          currentPassword: '',
        };
        setTimeout(() => {
          this.$router.push('/');
        }, 1500);
      } else {
        this.usernameError = result.error;
      }
    },

    async handleEmailChange() {
      console.log('Email change button clicked');
      this.emailError = '';
      this.emailSuccess = '';
      
      if (!this.emailForm.currentEmail || !this.emailForm.newEmail || !this.emailForm.currentPassword) {
        this.emailError = 'Please fill in all fields';
        return;
      }
      
      // Basic email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.emailForm.newEmail)) {
        this.emailError = 'Please enter a valid email address';
        return;
      }
      
      const result = await this.changeEmail({
        currentEmail: this.emailForm.currentEmail,
        newEmail: this.emailForm.newEmail,
        currentPassword: this.emailForm.currentPassword,
      });
      
      if (result.success) {
        this.emailSuccess = 'Email changed successfully! Your profile has been updated.';
        this.emailForm = {
          currentEmail: '',
          newEmail: '',
          currentPassword: '',
        };
        // Refresh user data to show updated email
        await this.refreshUserData();
      } else {
        this.emailError = result.error;
      }
    },

    setActiveTab(tab) {
      this.activeTab = tab;
      // Update URL hash for better navigation
      if (typeof window !== 'undefined') {
        window.location.hash = tab.toUpperCase();
      }
      // Force a re-render
      this.$forceUpdate();
    },

    async refreshUserData() {
      await this.getCurrentUser();
      // Log user data structure for debugging
      if (this.user) {
        console.log('User data structure:', this.user);
        console.log('Available fields:', Object.keys(this.user));
      }
    },

    // Handle URL hash changes
    handleHashChange() {
      try {
        let hash = '';
        if (typeof window !== 'undefined' && window.location && window.location.hash) {
          hash = window.location.hash.replace('#', '').toLowerCase();
        }
        
        // Handle different hash formats
        if (hash === 'security' || hash === 'set') {
          this.activeTab = 'security';
        } else if (hash === 'preferences' || hash === 'pref') {
          this.activeTab = 'preferences';
        } else if (hash === 'profile' || hash === 'prof') {
          this.activeTab = 'profile';
        } else if (!hash) {
          // Default to profile if no hash
          this.activeTab = 'profile';
        } else {
          // Try to match partial hash
          if (hash.includes('sec')) {
            this.activeTab = 'security';
          } else if (hash.includes('pref')) {
            this.activeTab = 'preferences';
          } else if (hash.includes('prof')) {
            this.activeTab = 'profile';
          } else {
            this.activeTab = 'profile';
          }
        }
      } catch (error) {
        this.activeTab = 'profile'; // Fallback to profile
      }
    },

    async updateTheme() {
      try {
        // Apply theme to document
        this.applyTheme();
        // Save preferences
        await this.savePreferences();
      } catch (error) {
        console.error('Error updating theme:', error);
      }
    },

    async updateColorScheme() {
      try {
        // Apply color scheme to document
        this.applyColorScheme();
        // Save preferences
        await this.savePreferences();
      } catch (error) {
        console.error('Error updating color scheme:', error);
      }
    },

    async updateFontSize() {
      try {
        // Apply font size to document
        this.applyFontSize();
        // Save preferences
        await this.savePreferences();
      } catch (error) {
        console.error('Error updating font size:', error);
      }
    },

    // Apply theme to document
    applyTheme() {
      const root = document.documentElement;
      const theme = this.preferences.theme;
      
      // Remove existing theme classes
      root.classList.remove('theme-light', 'theme-dark', 'theme-auto');
      
      // Add new theme class
      root.classList.add(`theme-${theme}`);
      
      // For auto theme, check system preference
      if (theme === 'auto') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        root.classList.add(prefersDark ? 'theme-dark' : 'theme-light');
      }
      
      console.log(`Theme applied: ${theme}`);
    },

    // Apply color scheme to document
    applyColorScheme() {
      const root = document.documentElement;
      const colorScheme = this.preferences.colorScheme || 'blue'; // Ensure blue is default
      
      // Remove existing color scheme classes
      root.classList.remove('color-blue', 'color-green', 'color-purple', 'color-orange', 'color-red');
      
      // Add new color scheme class
      root.classList.add(`color-${colorScheme}`);
      
      // Also apply to body for better coverage
      document.body.classList.remove('color-blue', 'color-green', 'color-purple', 'color-orange', 'color-red');
      document.body.classList.add(`color-${colorScheme}`);
      
      console.log(`Color scheme applied: ${colorScheme}`);
      console.log('Root classes:', root.className);
      console.log('Body classes:', document.body.className);
    },

    // Apply font size to document
    applyFontSize() {
      const root = document.documentElement;
      const fontSize = this.preferences.fontSize;
      
      // Remove existing font size classes
      root.classList.remove('font-small', 'font-medium', 'font-large');
      
      // Add new font size class
      root.classList.add(`font-${fontSize}`);
      
      console.log(`Font size applied: ${fontSize}`);
    },

    async updateEmailNotifications() {
      await this.savePreferences();
    },

    async updateBrowserNotifications() {
      await this.savePreferences();
    },

    async updateNotificationTypes() {
      await this.savePreferences();
    },

    async updateAnalytics() {
      await this.savePreferences();
    },

    async updateSessionTimeout() {
      await this.savePreferences();
    },

    async updateTwoFactor() {
      await this.savePreferences();
    },

    async savePreferences() {
      try {
        const result = await this.$store.dispatch('savePreferences', this.preferences);
        if (result.success) {
          // Show success notification
          this.$notify({
            type: 'success',
            title: 'Success',
            text: 'Preferences saved successfully!'
          });
        } else {
          this.$notify({
            type: 'error',
            title: 'Error',
            text: result.error || 'Failed to save preferences'
          });
        }
      } catch (error) {
        this.$notify({
          type: 'error',
          title: 'Error',
          text: 'Failed to save preferences'
        });
      }
    },

    async exportSettings() {
      try {
        const result = await this.exportPreferences();
        if (result.success) {
          this.$notify({
            type: 'success',
            title: 'Success',
            text: 'Preferences exported successfully!'
          });
        } else {
          this.$notify({
            type: 'error',
            title: 'Error',
            text: result.error || 'Failed to export preferences'
          });
        }
      } catch (error) {
        this.$notify({
          type: 'error',
          title: 'Error',
          text: 'Failed to export preferences'
        });
      }
    },

    async importSettings() {
      const fileInput = document.createElement('input');
      fileInput.type = 'file';
      fileInput.accept = 'application/json';
      fileInput.onchange = async (event) => {
        const file = event.target.files[0];
        if (file) {
          try {
            const result = await this.importPreferences(file);
            if (result.success) {
              this.preferences = result.preferences;
              
              // Apply imported preferences to the document
              this.applyTheme();
              this.applyColorScheme();
              this.applyFontSize();
              
              this.$notify({
                type: 'success',
                title: 'Success',
                text: 'Preferences imported successfully!'
              });
            } else {
              this.$notify({
                type: 'error',
                title: 'Error',
                text: result.error || 'Failed to import preferences'
              });
            }
          } catch (error) {
            this.$notify({
              type: 'error',
              title: 'Error',
              text: 'Failed to import preferences'
            });
          } finally {
            fileInput.remove();
          }
        }
      };
      fileInput.click();
    },

    async resetSettings() {
      if (confirm('Are you sure you want to reset all preferences to their default values?')) {
        try {
          const result = await this.resetPreferences();
          if (result.success) {
            this.preferences = result.preferences;
            
            // Apply reset preferences to the document
            this.applyTheme();
            this.applyColorScheme();
            this.applyFontSize();
            
            this.$notify({
              type: 'success',
              title: 'Success',
              text: 'Preferences reset to defaults successfully!'
            });
          } else {
            this.$notify({
              type: 'error',
              title: 'Error',
              text: result.error || 'Failed to reset preferences'
            });
          }
        } catch (error) {
          this.$notify({
            type: 'error',
            title: 'Error',
            text: 'Failed to reset preferences'
          });
        }
      }
    },

    // Auto-refresh timestamps every minute
    startTimestampRefresh() {
      this.timestampInterval = setInterval(() => {
        this.$forceUpdate(); // Force re-computation of formatted timestamps
      }, 60000); // Update every minute
    },

    stopTimestampRefresh() {
      if (this.timestampInterval) {
        clearInterval(this.timestampInterval);
        this.timestampInterval = null;
      }
    },

    // Handle system theme changes
    handleSystemThemeChange() {
      if (this.preferences.theme === 'auto') {
        this.applyTheme();
      }
    },

    goToDashboard() {
      this.$router.push('/');
    },

    // Reset loading state to ensure buttons are visible
    resetLoadingState() {
      this.$store.commit('setLoading', false);
    },

    // Force apply blue color scheme
    forceApplyBlue() {
      console.log('Force applying blue color scheme');
      this.preferences.colorScheme = 'blue';
      
      // Apply to document root
      const root = document.documentElement;
      root.classList.remove('color-blue', 'color-green', 'color-purple', 'color-orange', 'color-red');
      root.classList.add('color-blue');
      
      // Apply to body
      document.body.classList.remove('color-blue', 'color-green', 'color-purple', 'color-orange', 'color-red');
      document.body.classList.add('color-blue');
      
      // Apply to component
      const component = this.$el;
      if (component) {
        component.classList.remove('color-blue', 'color-green', 'color-purple', 'color-orange', 'color-red');
        component.classList.add('color-blue');
      }
      
      console.log('Blue color scheme force applied');
    },

    // Ensure all buttons are visible
    ensureButtonsVisible() {
      console.log('Ensuring all buttons are visible');
      
      // Force all buttons to be visible
      const buttons = document.querySelectorAll('.uk-button');
      buttons.forEach(button => {
        button.style.display = 'block';
        button.style.visibility = 'visible';
        button.style.opacity = '1';
        button.style.pointerEvents = 'auto';
      });
      
      // Force primary buttons to use blue
      const primaryButtons = document.querySelectorAll('.uk-button-primary');
      primaryButtons.forEach(button => {
        button.style.backgroundColor = '#1e87f0';
        button.style.borderColor = '#1e87f0';
      });
      
      console.log(`Made ${buttons.length} buttons visible`);
    },

    toggleDropdown() {
      this.showUserDropdown = !this.showUserDropdown;
    },
    
    handleClickOutside(event) {
      const dropdown = document.querySelector('.advanced-dropdown');
      const userLink = document.querySelector('.user-link');
      
      if (dropdown && userLink && !dropdown.contains(event.target) && !userLink.contains(event.target)) {
        this.showUserDropdown = false;
      }
    },

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
  },
  
  created() {
    // Apply default blue color scheme immediately
    console.log('Component created - applying blue color scheme');
    this.$nextTick(() => {
      // Force blue as default
      this.preferences.colorScheme = 'blue';
      this.applyColorScheme();
      console.log('Blue color scheme applied in created hook');
    });
  },
  
  async mounted() {
    // Reset loading state to ensure buttons are visible
    this.resetLoadingState();
    
    // Force apply blue color scheme
    this.forceApplyBlue();
    
    // Ensure all buttons are visible
    this.ensureButtonsVisible();
    
    await this.refreshUserData();
    // Pre-fill current values
    if (this.user) {
      this.usernameForm.currentUsername = this.user.username;
      this.emailForm.currentEmail = this.user.email;
    }
    
    // Load user preferences
    try {
      const result = await this.getPreferences();
      if (result.success && result.preferences) {
        this.preferences = { ...this.preferences, ...result.preferences };
        
        // Apply saved preferences to the document
        this.applyTheme();
        this.applyColorScheme();
        this.applyFontSize();
      } else {
        // Apply default preferences if none loaded
        this.applyTheme();
        this.applyColorScheme();
        this.applyFontSize();
      }
    } catch (error) {
      console.error('Failed to load preferences:', error);
      // Apply default preferences on error
      this.applyTheme();
      this.applyColorScheme();
      this.applyFontSize();
    }
    
    // Handle initial hash change - do this after data is loaded
    this.$nextTick(() => {
      this.handleHashChange();
    });
    
    // Add event listener for hash changes
    window.addEventListener('hashchange', this.handleHashChange);
    
    // Add event listener for system theme changes
    this.mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    this.mediaQuery.addEventListener('change', this.handleSystemThemeChange);
    
    // Start timestamp refresh
    this.startTimestampRefresh();
    
    // Ensure buttons are visible after a short delay
    setTimeout(() => {
      this.forceApplyBlue();
      this.ensureButtonsVisible();
    }, 100);
    
    // Add click outside handler to close dropdown
    document.addEventListener('click', this.handleClickOutside);
  },

  beforeDestroy() {
    // Clean up event listener
    window.removeEventListener('hashchange', this.handleHashChange);
    // Clean up media query listener
    if (this.mediaQuery) {
      this.mediaQuery.removeEventListener('change', this.handleSystemThemeChange);
    }
    // Stop timestamp refresh
    this.stopTimestampRefresh();
    // Remove click outside handler
    document.removeEventListener('click', this.handleClickOutside);
  },
};
</script>

<template>
  <div class="account-settings">
    <!-- Enhanced Navigation Header (Same as Dashboard) -->
    <nav class="uk-navbar-container" uk-navbar>
      <div class="uk-navbar-left">
        <div class="uk-navbar-item">
          <span uk-icon="icon: shield; ratio: 1.5"></span>
        </div>
        <ul class="uk-navbar-nav">
          <li>
            <router-link to="/" class="uk-navbar-item">
              <span uk-icon="icon: home; ratio: 1.2"></span>
              <span>DASHBOARD</span>
            </router-link>
          </li>
          <li class="uk-active">
            <a href="#" class="uk-navbar-item">
              <span uk-icon="icon: user; ratio: 1.2"></span>
              <span>ACCOUNT SETTINGS</span>
            </a>
          </li>
        </ul>
      </div>
      
      <div class="uk-navbar-right">
        <ul class="uk-navbar-nav">
          <li v-if="user" class="uk-parent">
            <a href="#" class="uk-navbar-item" @click="toggleDropdown">
              <span uk-icon="icon: user"></span>
              <span>{{ user.username.toUpperCase() }}</span>
              <span uk-icon="icon: chevron-down"></span>
            </a>
            <div v-if="showUserDropdown" class="uk-dropdown uk-dropdown-bottom-right">
              <ul class="uk-nav uk-dropdown-nav">
                <li>
                  <router-link to="/account">
                    <span uk-icon="icon: cog"></span>
                    <span>Account Settings</span>
                  </router-link>
                </li>
                <li class="uk-nav-divider"></li>
                <li>
                  <a href="#" @click.prevent="handleLogout">
                    <span uk-icon="icon: sign-out"></span>
                    <span>Logout</span>
                  </a>
                </li>
              </ul>
            </div>
          </li>
        </ul>
      </div>
    </nav>

    <!-- Account Settings Content -->
    <div class="uk-container uk-margin-large-top">
      <!-- Tab Navigation -->
      <ul class="uk-subnav uk-subnav-pill" uk-switcher="animation: uk-animation-fade">
        <li :class="{ 'uk-active': activeTab === 'profile' }">
          <a href="#" @click.prevent="setActiveTab('profile')">
            <span uk-icon="user"></span> Profile
          </a>
        </li>
        <li :class="{ 'uk-active': activeTab === 'security' }">
          <a href="#" @click.prevent="setActiveTab('security')">
            <span uk-icon="lock"></span> Security
          </a>
        </li>
        <li :class="{ 'uk-active': activeTab === 'preferences' }">
          <a href="#" @click.prevent="setActiveTab('preferences')">
            <span uk-icon="cog"></span> Preferences
          </a>
        </li>
      </ul>

      <!-- Tab Content -->
      <div class="uk-switcher uk-margin">
        
        <!-- Profile Tab -->
        <div v-show="activeTab === 'profile'">
          <div class="uk-grid uk-child-width-1-2@m uk-grid-large" uk-grid>
            <!-- Account Information -->
            <div>
              <div class="uk-card uk-card-default uk-card-body">
                <div class="uk-card-header">
                  <h3 class="uk-card-title">
                    <span uk-icon="icon: user"></span> Account Information
                  </h3>
                </div>
                <div class="uk-card-body">
                  <div v-if="user" class="uk-grid-small" uk-grid>
                    <div class="uk-width-1-1">
                      <div class="uk-flex uk-flex-middle uk-margin-small">
                        <span uk-icon="icon: user" class="uk-margin-small-right"></span>
                        <div>
                          <strong>Username:</strong> {{ user.username }}
                        </div>
                      </div>
                    </div>
                    <div class="uk-width-1-1">
                      <div class="uk-flex uk-flex-middle uk-margin-small">
                        <span uk-icon="icon: mail" class="uk-margin-small-right"></span>
                        <div>
                          <strong>Email:</strong> {{ user.email }}
                        </div>
                      </div>
                    </div>
                    <div class="uk-width-1-1">
                      <div class="uk-flex uk-flex-middle uk-margin-small">
                        <span uk-icon="icon: calendar" class="uk-margin-small-right"></span>
                        <div>
                          <strong>Date Joined:</strong> {{ formattedDateJoined }}
                        </div>
                      </div>
                    </div>
                    <div class="uk-width-1-1">
                      <div class="uk-flex uk-flex-middle uk-margin-small">
                        <span uk-icon="icon: clock" class="uk-margin-small-right"></span>
                        <div>
                          <strong>Last Login:</strong> {{ formattedLastLogin }}
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-else class="uk-text-center">
                    <div uk-spinner></div>
                    <p>Loading user information...</p>
                  </div>
                </div>
                <div class="uk-card-footer">
                  <button @click="refreshUserData" class="uk-button uk-button-small uk-button-primary">
                    <span uk-icon="icon: refresh"></span> Refresh
                  </button>
                </div>
              </div>
            </div>

            <!-- Quick Stats -->
            <div>
              <div class="uk-card uk-card-default uk-card-body">
                <div class="uk-card-header">
                  <h3 class="uk-card-title">
                    <span uk-icon="icon: chart-line"></span> Account Statistics
                  </h3>
                </div>
                <div class="uk-card-body">
                  <div class="uk-grid-small" uk-grid>
                    <div class="uk-width-1-2">
                      <div class="uk-text-center">
                        <div class="uk-text-large uk-text-bold uk-text-primary">0</div>
                        <div class="uk-text-small">Projects</div>
                      </div>
                    </div>
                    <div class="uk-width-1-2">
                      <div class="uk-text-center">
                        <div class="uk-text-large uk-text-bold uk-text-success">0</div>
                        <div class="uk-text-small">Scans</div>
                      </div>
                    </div>
                    <div class="uk-width-1-2">
                      <div class="uk-text-center">
                        <div class="uk-text-large uk-text-bold uk-text-warning">0</div>
                        <div class="uk-text-small">Reports</div>
                      </div>
                    </div>
                    <div class="uk-width-1-2">
                      <div class="uk-text-center">
                        <div class="uk-text-large uk-text-bold uk-text-danger">0</div>
                        <div class="uk-text-small">Vulnerabilities</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Security Tab -->
        <div v-show="activeTab === 'security'">
          <div class="uk-grid uk-child-width-1-2@m uk-grid-large" uk-grid>
            <!-- Change Password -->
            <div>
              <div class="uk-card uk-card-default uk-card-body">
                <div class="uk-card-header">
                  <h3 class="uk-card-title">
                    <span uk-icon="icon: lock"></span> Change Password
                  </h3>
                </div>
                <div class="uk-card-body">
                  <form @submit.prevent="handlePasswordChange">
                    <div class="uk-margin">
                      <label class="uk-form-label">Current Password</label>
                      <div class="uk-form-controls">
                        <div class="uk-inline uk-width-1-1">
                          <span class="uk-form-icon" uk-icon="icon: lock"></span>
                          <input 
                            v-model="passwordForm.currentPassword"
                            type="password" 
                            class="uk-input" 
                            placeholder="Enter current password"
                            required
                          />
                        </div>
                      </div>
                    </div>
                    
                    <div class="uk-margin">
                      <label class="uk-form-label">New Password</label>
                      <div class="uk-form-controls">
                        <div class="uk-inline uk-width-1-1">
                          <span class="uk-form-icon" uk-icon="icon: lock"></span>
                          <input 
                            v-model="passwordForm.newPassword"
                            type="password" 
                            class="uk-input" 
                            placeholder="Enter new password"
                            required
                          />
                        </div>
                      </div>
                    </div>
                    
                    <div class="uk-margin">
                      <label class="uk-form-label">Confirm New Password</label>
                      <div class="uk-form-controls">
                        <div class="uk-inline uk-width-1-1">
                          <span class="uk-form-icon" uk-icon="icon: lock"></span>
                          <input 
                            v-model="passwordForm.confirmPassword"
                            type="password" 
                            class="uk-input" 
                            placeholder="Confirm new password"
                            required
                          />
                        </div>
                      </div>
                    </div>
                    
                    <div class="uk-margin">
                      <button 
                        type="submit" 
                        class="uk-button uk-button-primary uk-width-1-1"
                        :disabled="loading"
                      >
                        <span uk-spinner v-if="loading"></span>
                        <span v-else uk-icon="icon: check"></span>
                        {{ loading ? 'Changing Password...' : 'Change Password' }}
                      </button>
                    </div>
                  </form>
                  
                  <div v-if="passwordError" class="uk-alert-danger" uk-alert>
                    <a href="#" class="uk-alert-close" uk-close></a>
                    <p>{{ passwordError }}</p>
                  </div>
                  
                  <div v-if="passwordSuccess" class="uk-alert-success" uk-alert>
                    <a href="#" class="uk-alert-close" uk-close></a>
                    <p>{{ passwordSuccess }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Change Username -->
            <div>
              <div class="uk-card uk-card-default uk-card-body">
                <div class="uk-card-header">
                  <h3 class="uk-card-title">
                    <span uk-icon="icon: user"></span> Change Username
                  </h3>
                </div>
                <div class="uk-card-body">
                  <form @submit.prevent="handleUsernameChange">
                    <div class="uk-margin">
                      <label class="uk-form-label">Current Username</label>
                      <div class="uk-form-controls">
                        <div class="uk-inline uk-width-1-1">
                          <span class="uk-form-icon" uk-icon="icon: user"></span>
                          <input 
                            v-model="usernameForm.currentUsername"
                            type="text" 
                            class="uk-input" 
                            placeholder="Enter current username"
                            required
                          />
                        </div>
                      </div>
                    </div>
                    
                    <div class="uk-margin">
                      <label class="uk-form-label">New Username</label>
                      <div class="uk-form-controls">
                        <div class="uk-inline uk-width-1-1">
                          <span class="uk-form-icon" uk-icon="icon: user"></span>
                          <input 
                            v-model="usernameForm.newUsername"
                            type="text" 
                            class="uk-input" 
                            placeholder="Enter new username"
                            required
                          />
                        </div>
                      </div>
                    </div>
                    
                    <div class="uk-margin">
                      <label class="uk-form-label">Current Password</label>
                      <div class="uk-form-controls">
                        <div class="uk-inline uk-width-1-1">
                          <span class="uk-form-icon" uk-icon="icon: lock"></span>
                          <input 
                            v-model="usernameForm.currentPassword"
                            type="password" 
                            class="uk-input" 
                            placeholder="Enter current password"
                            required
                          />
                        </div>
                      </div>
                    </div>
                    
                    <div class="uk-margin">
                      <button 
                        type="submit" 
                        class="uk-button uk-button-primary uk-width-1-1"
                        :disabled="loading"
                      >
                        <span uk-spinner v-if="loading"></span>
                        <span v-else uk-icon="icon: check"></span>
                        {{ loading ? 'Changing Username...' : 'Change Username' }}
                      </button>
                    </div>
                  </form>
                  
                  <div v-if="usernameError" class="uk-alert-danger" uk-alert>
                    <a href="#" class="uk-alert-close" uk-close></a>
                    <p>{{ usernameError }}</p>
                  </div>
                  
                  <div v-if="usernameSuccess" class="uk-alert-success" uk-alert>
                    <a href="#" class="uk-alert-close" uk-close></a>
                    <p>{{ usernameSuccess }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Change Email -->
            <div class="uk-width-1-1">
              <div class="uk-card uk-card-default uk-card-body">
                <div class="uk-card-header">
                  <h3 class="uk-card-title">
                    <span uk-icon="icon: mail"></span> Change Email
                  </h3>
                </div>
                <div class="uk-card-body">
                  <form @submit.prevent="handleEmailChange">
                    <div class="uk-grid uk-child-width-1-3@m" uk-grid>
                      <div>
                        <label class="uk-form-label">Current Email</label>
                        <div class="uk-form-controls">
                          <div class="uk-inline uk-width-1-1">
                            <span class="uk-form-icon" uk-icon="icon: mail"></span>
                            <input 
                              v-model="emailForm.currentEmail"
                              type="email" 
                              class="uk-input" 
                              placeholder="Enter current email"
                              required
                            />
                          </div>
                        </div>
                      </div>
                      
                      <div>
                        <label class="uk-form-label">New Email</label>
                        <div class="uk-form-controls">
                          <div class="uk-inline uk-width-1-1">
                            <span class="uk-form-icon" uk-icon="icon: mail"></span>
                            <input 
                              v-model="emailForm.newEmail"
                              type="email" 
                              class="uk-input" 
                              placeholder="Enter new email"
                              required
                            />
                          </div>
                        </div>
                      </div>
                      
                      <div>
                        <label class="uk-form-label">Current Password</label>
                        <div class="uk-form-controls">
                          <div class="uk-inline uk-width-1-1">
                            <span class="uk-form-icon" uk-icon="icon: lock"></span>
                            <input 
                              v-model="emailForm.currentPassword"
                              type="password" 
                              class="uk-input" 
                              placeholder="Enter current password"
                              required
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div class="uk-margin-top">
                      <button 
                        type="submit" 
                        class="uk-button uk-button-primary"
                        :disabled="loading"
                      >
                        <span uk-spinner v-if="loading"></span>
                        <span v-else uk-icon="icon: check"></span>
                        {{ loading ? 'Changing Email...' : 'Change Email' }}
                      </button>
                    </div>
                  </form>
                  
                  <div v-if="emailError" class="uk-alert-danger" uk-alert>
                    <a href="#" class="uk-alert-close" uk-close></a>
                    <p>{{ emailError }}</p>
                  </div>
                  
                  <div v-if="emailSuccess" class="uk-alert-success" uk-alert>
                    <a href="#" class="uk-alert-close" uk-close></a>
                    <p>{{ emailSuccess }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Preferences Tab -->
        <div v-show="activeTab === 'preferences'">
          <div class="uk-grid uk-child-width-1-2@m uk-grid-large" uk-grid>
            <!-- Theme Settings -->
            <div>
              <div class="uk-card uk-card-default uk-card-body">
                <div class="uk-card-header">
                  <h3 class="uk-card-title">
                    <span uk-icon="icon: paint-bucket"></span> Theme Settings
                  </h3>
                </div>
                <div class="uk-card-body">
                  <div class="uk-margin">
                    <label class="uk-form-label">Theme Mode</label>
                    <div class="uk-form-controls">
                      <div class="uk-margin uk-grid-small uk-child-width-auto uk-grid">
                        <label>
                          <input 
                            class="uk-radio" 
                            type="radio" 
                            name="theme" 
                            value="light" 
                            v-model="preferences.theme"
                            @change="updateTheme"
                          > Light
                        </label>
                        <label>
                          <input 
                            class="uk-radio" 
                            type="radio" 
                            name="theme" 
                            value="dark" 
                            v-model="preferences.theme"
                            @change="updateTheme"
                          > Dark
                        </label>
                        <label>
                          <input 
                            class="uk-radio" 
                            type="radio" 
                            name="theme" 
                            value="auto" 
                            v-model="preferences.theme"
                            @change="updateTheme"
                          > Auto
                        </label>
                      </div>
                    </div>
                  </div>
                  
                  <div class="uk-margin">
                    <label class="uk-form-label">Color Scheme</label>
                    <div class="uk-form-controls">
                      <select v-model="preferences.colorScheme" @change="updateColorScheme" class="uk-select">
                        <option value="blue">Blue (Default)</option>
                        <option value="green">Green</option>
                        <option value="purple">Purple</option>
                        <option value="orange">Orange</option>
                        <option value="red">Red</option>
                      </select>
                    </div>
                  </div>
                  
                  <div class="uk-margin">
                    <label class="uk-form-label">Font Size</label>
                    <div class="uk-form-controls">
                      <select v-model="preferences.fontSize" @change="updateFontSize" class="uk-select">
                        <option value="small">Small</option>
                        <option value="medium">Medium</option>
                        <option value="large">Large</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Notification Settings -->
            <div>
              <div class="uk-card uk-card-default uk-card-body">
                <div class="uk-card-header">
                  <h3 class="uk-card-title">
                    <span uk-icon="icon: bell"></span> Notification Settings
                  </h3>
                </div>
                <div class="uk-card-body">
                  <div class="uk-margin">
                    <label class="uk-form-label">Email Notifications</label>
                    <div class="uk-form-controls">
                      <div class="uk-margin uk-grid-small uk-child-width-auto uk-grid">
                        <label>
                          <input 
                            class="uk-checkbox" 
                            type="checkbox" 
                            v-model="preferences.emailNotifications"
                            @change="updateEmailNotifications"
                          > Enable email notifications
                        </label>
                      </div>
                    </div>
                  </div>
                  
                  <div class="uk-margin">
                    <label class="uk-form-label">Browser Notifications</label>
                    <div class="uk-form-controls">
                      <div class="uk-margin uk-grid-small uk-child-width-auto uk-grid">
                        <label>
                          <input 
                            class="uk-checkbox" 
                            type="checkbox" 
                            v-model="preferences.browserNotifications"
                            @change="updateBrowserNotifications"
                          > Enable browser notifications
                        </label>
                      </div>
                    </div>
                  </div>
                  
                  <div class="uk-margin">
                    <label class="uk-form-label">Notification Types</label>
                    <div class="uk-form-controls">
                      <div class="uk-margin uk-grid-small uk-child-width-auto uk-grid">
                        <label>
                          <input 
                            class="uk-checkbox" 
                            type="checkbox" 
                            v-model="preferences.notifyScans"
                            @change="updateNotificationTypes"
                          > Scan completions
                        </label>
                        <label>
                          <input 
                            class="uk-checkbox" 
                            type="checkbox" 
                            v-model="preferences.notifyVulnerabilities"
                            @change="updateNotificationTypes"
                          > New vulnerabilities
                        </label>
                        <label>
                          <input 
                            class="uk-checkbox" 
                            type="checkbox" 
                            v-model="preferences.notifyReports"
                            @change="updateNotificationTypes"
                          > Report generation
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Privacy Settings -->
            <div>
              <div class="uk-card uk-card-default uk-card-body">
                <div class="uk-card-header">
                  <h3 class="uk-card-title">
                    <span uk-icon="icon: shield"></span> Privacy Settings
                  </h3>
                </div>
                <div class="uk-card-body">
                  <div class="uk-margin">
                    <label class="uk-form-label">Data Collection</label>
                    <div class="uk-form-controls">
                      <div class="uk-margin uk-grid-small uk-child-width-auto uk-grid">
                        <label>
                          <input 
                            class="uk-checkbox" 
                            type="checkbox" 
                            v-model="preferences.analytics"
                            @change="updateAnalytics"
                          > Allow analytics data collection
                        </label>
                      </div>
                    </div>
                  </div>
                  
                  <div class="uk-margin">
                    <label class="uk-form-label">Session Timeout</label>
                    <div class="uk-form-controls">
                      <select v-model="preferences.sessionTimeout" @change="updateSessionTimeout" class="uk-select">
                        <option value="15">15 minutes</option>
                        <option value="30">30 minutes</option>
                        <option value="60">1 hour</option>
                        <option value="120">2 hours</option>
                        <option value="0">Never (until logout)</option>
                      </select>
                    </div>
                  </div>
                  
                  <div class="uk-margin">
                    <label class="uk-form-label">Two-Factor Authentication</label>
                    <div class="uk-form-controls">
                      <div class="uk-margin uk-grid-small uk-child-width-auto uk-grid">
                        <label>
                          <input 
                            class="uk-checkbox" 
                            type="checkbox" 
                            v-model="preferences.twoFactor"
                            @change="updateTwoFactor"
                          > Enable 2FA
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Export/Import Settings -->
            <div>
              <div class="uk-card uk-card-default uk-card-body">
                <div class="uk-card-header">
                  <h3 class="uk-card-title">
                    <span uk-icon="icon: download"></span> Data Management
                  </h3>
                </div>
                <div class="uk-card-body">
                  <div class="uk-margin">
                    <button @click="exportSettings" class="uk-button uk-button-primary uk-width-1-1">
                      <span uk-icon="icon: download"></span> Export Settings
                    </button>
                  </div>
                  
                  <div class="uk-margin">
                    <button @click="importSettings" class="uk-button uk-button-secondary uk-width-1-1">
                      <span uk-icon="icon: upload"></span> Import Settings
                    </button>
                  </div>
                  
                  <div class="uk-margin">
                    <button @click="resetSettings" class="uk-button uk-button-danger uk-width-1-1">
                      <span uk-icon="icon: refresh"></span> Reset to Defaults
                    </button>
                  </div>
                  
                  <div class="uk-margin">
                    <button @click="savePreferences" class="uk-button uk-button-success uk-width-1-1">
                      <span uk-icon="icon: check"></span> Save All Preferences
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
  </div>
</template>

<style scoped>
/* Minimal UIKit-based styling only */
.account-settings {
  min-height: 100vh;
  background: #f8f9fa;
  padding-bottom: 2rem;
}

/* Ensure proper spacing for cards */
.uk-card {
  margin-bottom: 1rem;
}

/* Ensure proper button visibility */
.uk-button {
  display: block;
  visibility: visible;
}

/* Ensure proper form styling */
.uk-form-label {
  font-weight: 600;
}

/* Ensure proper alert styling */
.uk-alert {
  margin: 1rem 0;
}
</style> 