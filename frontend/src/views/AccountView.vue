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
    <nav class="uk-navbar-container advanced-navbar" uk-navbar>
      <div class="uk-navbar-left">
        <div class="nav-brand">
          <span uk-icon="icon: shield; ratio: 1.5" class="brand-icon"></span>
          <!-- <span class="brand-text">IMMUNITY</span>  -->
        </div>
        <ul class="uk-navbar-nav advanced-nav">
          <li>
            <router-link to="/" class="nav-link">
              <span uk-icon="icon: home; ratio: 1.2" class="nav-icon"></span>
              <span class="nav-text">DASHBOARD</span>
            </router-link>
          </li>
          <li class="uk-active">
            <a href="#" class="nav-link nav-link-active">
              <span uk-icon="icon: user; ratio: 1.2" class="nav-icon"></span>
              <span class="nav-text">ACCOUNT SETTINGS</span>
            </a>
          </li>
        </ul>
      </div>
      
      <div class="uk-navbar-right">
        <ul class="uk-navbar-nav">
          <li v-if="user" class="user-menu">
            <div class="user-link" @click="toggleDropdown">
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
              <div class="uk-card uk-card-default uk-card-body uk-card-hover info-card">
                <div class="uk-card-header">
                  <div class="card-header-content">
                    <div class="card-icon-wrapper">
                      <span uk-icon="user" class="card-icon"></span>
                    </div>
                    <div class="card-title-section">
                      <h3 class="uk-card-title">Account Information</h3>
                      <span class="card-subtitle">Personal details and account status</span>
                    </div>
                    <div class="card-actions">
                      <button @click="refreshUserData" class="uk-button uk-button-small uk-button-primary refresh-btn">
                        <span uk-icon="refresh"></span>
                      </button>
                    </div>
                  </div>
                </div>
                <div class="uk-card-body">
                  <div v-if="user" class="uk-grid-small" uk-grid>
                    <div class="uk-width-1-1">
                      <div class="uk-flex uk-flex-middle uk-margin-small">
                        <span uk-icon="user" class="uk-margin-small-right"></span>
                        <div>
                          <strong>Username:</strong> {{ user.username }}
                        </div>
                      </div>
                    </div>
                    <div class="uk-width-1-1">
                      <div class="uk-flex uk-flex-middle uk-margin-small">
                        <span uk-icon="mail" class="uk-margin-small-right"></span>
                        <div>
                          <strong>Email:</strong> {{ user.email }}
                        </div>
                      </div>
                    </div>
                    <div class="uk-width-1-1">
                      <div class="uk-flex uk-flex-middle uk-margin-small">
                        <span uk-icon="calendar" class="uk-margin-small-right"></span>
                        <div>
                          <strong>Date Joined:</strong> {{ formattedDateJoined }}
                        </div>
                      </div>
                    </div>
                    <div class="uk-width-1-1">
                      <div class="uk-flex uk-flex-middle uk-margin-small">
                        <span uk-icon="clock" class="uk-margin-small-right"></span>
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
                    <span uk-icon="refresh"></span> Refresh
                  </button>
                </div>
              </div>
            </div>

            <!-- Quick Stats -->
            <div>
              <div class="uk-card uk-card-default uk-card-body uk-card-hover">
                <div class="uk-card-header">
                  <h3 class="uk-card-title">
                    <span uk-icon="chart-line"></span> Account Statistics
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
              <div class="uk-card uk-card-default uk-card-body uk-card-hover">
                <div class="uk-card-header">
                  <h3 class="uk-card-title">
                    <span uk-icon="lock"></span> Change Password
                  </h3>
                </div>
                <div class="uk-card-body">
                  <form @submit.prevent="handlePasswordChange">
                    <div class="uk-margin">
                      <label class="uk-form-label form-label">
                        <span class="label-icon" uk-icon="lock"></span>
                        Current Password
                        <span class="required-indicator">*</span>
                      </label>
                      <div class="uk-form-controls">
                        <div class="uk-inline uk-width-1-1 form-field-wrapper">
                          <span class="uk-form-icon form-icon" uk-icon="lock"></span>
                          <input 
                            v-model="passwordForm.currentPassword"
                            type="password" 
                            class="uk-input form-input" 
                            placeholder="Enter current password"
                            required
                          />
                          <div class="field-status">
                            <span class="status-icon" uk-icon="check" v-if="passwordForm.currentPassword"></span>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div class="uk-margin">
                      <label class="uk-form-label">New Password</label>
                      <div class="uk-form-controls">
                        <div class="uk-inline uk-width-1-1">
                          <span class="uk-form-icon" uk-icon="lock"></span>
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
                          <span class="uk-form-icon" uk-icon="lock"></span>
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
                    
                    <button 
                      type="submit" 
                      class="uk-button uk-button-primary uk-width-1-1"
                      :disabled="loading"
                      style="display: block !important; visibility: visible !important;"
                    >
                      <span uk-icon="check" v-if="!loading"></span>
                      <span uk-spinner v-else></span>
                      {{ loading ? 'Changing Password...' : 'Change Password' }}
                    </button>
                  </form>
                  
                  <div v-if="passwordError" class="uk-alert-danger" uk-alert>
                    <p>{{ passwordError }}</p>
                  </div>
                  
                  <div v-if="passwordSuccess" class="uk-alert-success" uk-alert>
                    <p>{{ passwordSuccess }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Change Username -->
            <div>
              <div class="uk-card uk-card-default uk-card-body uk-card-hover">
                <div class="uk-card-header">
                  <h3 class="uk-card-title">
                    <span uk-icon="user"></span> Change Username
                  </h3>
                </div>
                <div class="uk-card-body">
                  <form @submit.prevent="handleUsernameChange">
                    <div class="uk-margin">
                      <label class="uk-form-label">Current Username</label>
                      <div class="uk-form-controls">
                        <div class="uk-inline uk-width-1-1">
                          <span class="uk-form-icon" uk-icon="user"></span>
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
                          <span class="uk-form-icon" uk-icon="user"></span>
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
                          <span class="uk-form-icon" uk-icon="lock"></span>
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
                    
                    <button 
                      type="submit" 
                      class="uk-button uk-button-primary uk-width-1-1"
                      :disabled="loading"
                      style="display: block !important; visibility: visible !important;"
                    >
                      <span uk-icon="check" v-if="!loading"></span>
                      <span uk-spinner v-else></span>
                      {{ loading ? 'Changing Username...' : 'Change Username' }}
                    </button>
                  </form>
                  
                  <div v-if="usernameError" class="uk-alert-danger" uk-alert>
                    <p>{{ usernameError }}</p>
                  </div>
                  
                  <div v-if="usernameSuccess" class="uk-alert-success" uk-alert>
                    <p>{{ usernameSuccess }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Change Email -->
            <div class="uk-width-1-1">
              <div class="uk-card uk-card-default uk-card-body uk-card-hover">
                <div class="uk-card-header">
                  <h3 class="uk-card-title">
                    <span uk-icon="mail"></span> Change Email
                  </h3>
                </div>
                <div class="uk-card-body">
                  <form @submit.prevent="handleEmailChange">
                    <div class="uk-grid uk-child-width-1-3@m" uk-grid>
                      <div>
                        <label class="uk-form-label">Current Email</label>
                        <div class="uk-form-controls">
                          <div class="uk-inline uk-width-1-1">
                            <span class="uk-form-icon" uk-icon="mail"></span>
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
                            <span class="uk-form-icon" uk-icon="mail"></span>
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
                            <span class="uk-form-icon" uk-icon="lock"></span>
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
                        style="display: block !important; visibility: visible !important;"
                      >
                        <span uk-icon="check" v-if="!loading"></span>
                        <span uk-spinner v-else></span>
                        {{ loading ? 'Changing Email...' : 'Change Email' }}
                      </button>
                    </div>
                  </form>
                  
                  <div v-if="emailError" class="uk-alert-danger" uk-alert>
                    <p>{{ emailError }}</p>
                  </div>
                  
                  <div v-if="emailSuccess" class="uk-alert-success" uk-alert>
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
              <div class="uk-card uk-card-default uk-card-body uk-card-hover">
                <div class="uk-card-header">
                  <h3 class="uk-card-title">
                    <span uk-icon="paint-bucket"></span> Theme Settings
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
              <div class="uk-card uk-card-default uk-card-body uk-card-hover">
                <div class="uk-card-header">
                  <h3 class="uk-card-title">
                    <span uk-icon="bell"></span> Notification Settings
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
              <div class="uk-card uk-card-default uk-card-body uk-card-hover">
                <div class="uk-card-header">
                  <h3 class="uk-card-title">
                    <span uk-icon="shield"></span> Privacy Settings
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
              <div class="uk-card uk-card-default uk-card-body uk-card-hover">
                <div class="uk-card-header">
                  <h3 class="uk-card-title">
                    <span uk-icon="download"></span> Data Management
                  </h3>
                </div>
                <div class="uk-card-body">
                  <div class="uk-margin">
                    <button @click="exportSettings" class="uk-button uk-button-primary uk-width-1-1">
                      <span uk-icon="download"></span> Export Settings
                    </button>
                  </div>
                  
                  <div class="uk-margin">
                    <button @click="importSettings" class="uk-button uk-button-secondary uk-width-1-1">
                      <span uk-icon="upload"></span> Import Settings
                    </button>
                  </div>
                  
                  <div class="uk-margin">
                    <button @click="resetSettings" class="uk-button uk-button-danger uk-width-1-1">
                      <span uk-icon="refresh"></span> Reset to Defaults
                    </button>
                  </div>
                  
                  <div class="uk-margin">
                    <button @click="savePreferences" class="uk-button uk-button-success uk-width-1-1">
                      <span uk-icon="check"></span> Save All Preferences
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
/* Advanced Navigation Styling (Same as Dashboard) */
.advanced-navbar {
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  border-bottom: 3px solid #1e87f0;
  position: relative;
  overflow: visible !important;
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

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
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
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
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
}

/* Force dropdown to be visible when open */
.uk-dropdown.uk-open {
  display: block !important;
  visibility: visible !important;
  opacity: 1 !important;
}

.uk-dropdown-nav {
  margin: 0;
  padding: 0;
  list-style: none;
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
  background: #eee;
  margin: 5px 0;
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
}

/* Add hover functionality back */
.user-menu:hover .uk-dropdown {
  display: block !important;
}

.user-link:hover + .uk-dropdown {
  display: block !important;
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

.account-settings {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding-bottom: 2rem;
}

.uk-card {
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.uk-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.uk-card-header {
  border-bottom: 1px solid #e5e5e5;
  padding: 1.5rem 1.5rem 1rem;
}

.uk-card-title {
  margin: 0;
  font-weight: 600;
}

.uk-card-body {
  padding: 1.5rem;
}

.uk-subnav-pill > * > * {
  border-radius: 20px;
  padding: 0.5rem 1.5rem;
  transition: all 0.3s ease;
}

.uk-subnav-pill > .uk-active > * {
  background-color: #1e87f0;
  color: white;
}

.uk-button {
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.uk-button:hover {
  transform: translateY(-1px);
}

.uk-input {
  border-radius: 8px;
  border: 2px solid #e5e5e5;
  transition: all 0.3s ease;
}

.uk-input:focus {
  border-color: #1e87f0;
  box-shadow: 0 0 0 3px rgba(30, 135, 240, 0.1);
}

.uk-alert {
  border-radius: 8px;
  border: none;
}

.uk-alert-success {
  background-color: #d4edda;
  color: #155724;
}

.uk-alert-danger {
  background-color: #f8d7da;
  color: #721c24;
}

/* Theme styles */
.theme-light {
  --bg-primary: #ffffff;
  --bg-secondary: #f8f9fa;
  --text-primary: #333333;
  --text-secondary: #666666;
  --border-color: #e5e5e5;
  --accent-color: #1e87f0;
}

.theme-dark {
  --bg-primary: #1a1a1a;
  --bg-secondary: #2d2d2d;
  --text-primary: #ffffff;
  --text-secondary: #cccccc;
  --border-color: #404040;
  --accent-color: #4a9eff;
}

/* Color scheme styles */
.color-blue {
  --primary-color: #1e87f0;
  --primary-hover: #0f7ae5;
  --primary-light: #e3f2fd;
}

/* Default color scheme - ensure blue is applied by default */
:root {
  --primary-color: #1e87f0 !important;
  --primary-hover: #0f7ae5 !important;
  --primary-light: #e3f2fd !important;
}

/* Force blue color scheme on all elements */
.account-settings,
.account-settings * {
  --primary-color: #1e87f0 !important;
  --primary-hover: #0f7ae5 !important;
  --primary-light: #e3f2fd !important;
}

/* Ensure all buttons are visible */
.uk-button {
  display: block !important;
  visibility: visible !important;
  opacity: 1 !important;
}

.uk-button:disabled {
  opacity: 0.7 !important;
  cursor: not-allowed !important;
}

/* Icon spacing */
.uk-form-icon {
  color: #666;
}

.uk-text-large {
  font-size: 2rem;
  font-weight: bold;
}

.uk-text-meta {
  color: #666;
  font-size: 0.9rem;
}

/* Preferences tab improvements */
.uk-radio, .uk-checkbox {
  margin-right: 8px;
}

.uk-radio:checked, .uk-checkbox:checked {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.uk-select {
  border-radius: 8px;
  border: 2px solid #e5e5e5;
  transition: all 0.3s ease;
}

.uk-select:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(30, 135, 240, 0.1);
}

/* Button improvements for preferences */
.uk-button-secondary {
  background-color: #6c757d;
  color: white;
  border: 1px solid #6c757d;
}

.uk-button-secondary:hover {
  background-color: #5a6268;
  border-color: #545b62;
}

.uk-button-success {
  background-color: #28a745;
  color: white;
  border: 1px solid #28a745;
}

.uk-button-success:hover {
  background-color: #218838;
  border-color: #1e7e34;
}

.uk-button-danger {
  background-color: #dc3545;
  color: white;
  border: 1px solid #dc3545;
}

.uk-button-danger:hover {
  background-color: #c82333;
  border-color: #bd2130;
}

/* Form label improvements */
.uk-form-label {
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

/* Checkbox and radio improvements */
.uk-grid-small > * {
  margin-bottom: 0.5rem;
}

.uk-grid-small > * > label {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  transition: background-color 0.2s ease;
}

.uk-grid-small > * > label:hover {
  background-color: #f8f9fa;
}

/* Card improvements for preferences */
.uk-card-hover:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
}

/* Responsive improvements for preferences */
@media (max-width: 959px) {
  .uk-grid-large > * {
    margin-bottom: 1rem;
  }
}

@media (max-width: 639px) {
  .uk-grid-small > * > label {
    font-size: 0.9rem;
    padding: 0.4rem;
  }
  
  .uk-button {
    font-size: 0.9rem;
    padding: 0.5rem 1rem;
  }
}

/* Professional breadcrumb styling */
.uk-breadcrumb {
  background: rgba(255, 255, 255, 0.8);
  padding: 0.75rem 1rem;
  border-radius: 8px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.uk-breadcrumb > * > * {
  color: #666;
  font-size: 0.9rem;
  text-decoration: none;
  transition: color 0.3s ease;
}

.uk-breadcrumb > * > *:hover {
  color: #1e87f0;
  text-decoration: none;
}

.uk-breadcrumb > * > .uk-text-primary {
  color: #1e87f0 !important;
  font-weight: 500;
}

.uk-breadcrumb > * > .uk-text-muted {
  color: #999 !important;
}

/* Professional header styling */
.uk-button-text {
  background: transparent;
  border: none;
  color: #1e87f0;
  font-weight: 500;
  transition: all 0.3s ease;
}

.uk-button-text:hover {
  background: rgba(30, 135, 240, 0.1);
  color: #0f7ae5;
  transform: none;
}

/* Professional tab navigation styling */
.uk-subnav-pill {
  background: rgba(255, 255, 255, 0.8);
  padding: 0.5rem;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.uk-subnav-pill > * > * {
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  transition: all 0.3s ease;
  font-weight: 500;
  color: #666;
  text-decoration: none;
}

.uk-subnav-pill > * > *:hover {
  background: rgba(30, 135, 240, 0.1);
  color: #1e87f0;
  transform: translateY(-1px);
}

.uk-subnav-pill > .uk-active > * {
  background: linear-gradient(135deg, #1e87f0 0%, #0f7ae5 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(30, 135, 240, 0.3);
  transform: translateY(-1px);
}

/* Glassmorphism breadcrumb */
.uk-breadcrumb {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Professional tab navigation */
.uk-subnav-pill {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Subtle text button */
.uk-button-text {
  background: transparent;
  color: #1e87f0;
  transition: all 0.3s ease;
}

/* Enhanced Professional Styling */

/* Header Enhancements */
.header-icon-wrapper {
  position: relative;
  display: inline-block;
}

.status-indicator {
  position: absolute;
  bottom: -2px;
  right: -2px;
  width: 12px;
  height: 12px;
  background: #28a745;
  border: 2px solid white;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.7; }
  100% { transform: scale(1); opacity: 1; }
}

.page-title {
  font-size: 2.2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #1e87f0 0%, #0f7ae5 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  font-size: 1rem;
  color: #666;
  margin-bottom: 1rem;
}

.page-status {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 0.5rem;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge.status-active {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
  border: 1px solid rgba(40, 167, 69, 0.2);
}

.last-updated {
  font-size: 0.8rem;
  color: #999;
}

.header-actions {
  display: flex;
  align-items: center;
}

.back-button {
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.back-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(30, 135, 240, 0.1), transparent);
  transition: left 0.5s ease;
}

.back-button:hover::before {
  left: 100%;
}

/* Enhanced Card Design */
.info-card {
  position: relative;
  overflow: hidden;
  border: none;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.info-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #1e87f0, #0f7ae5, #1e87f0);
  background-size: 200% 100%;
  animation: shimmer 3s ease-in-out infinite;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.card-header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.card-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #1e87f0, #0f7ae5);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(30, 135, 240, 0.3);
}

.card-icon {
  color: white;
  font-size: 1.2rem;
}

.card-title-section {
  flex: 1;
}

.card-subtitle {
  font-size: 0.85rem;
  color: #666;
  margin-top: 0.25rem;
  display: block;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.refresh-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.refresh-btn:hover {
  transform: rotate(180deg);
}

/* Enhanced Form Styling */
.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
}

.label-icon {
  color: #1e87f0;
  font-size: 0.9rem;
}

.required-indicator {
  color: #dc3545;
  font-weight: bold;
  margin-left: 0.25rem;
}

.form-field-wrapper {
  position: relative;
  transition: all 0.3s ease;
}

.form-field-wrapper:focus-within {
  transform: translateY(-2px);
}

.form-icon {
  color: #666;
  transition: color 0.3s ease;
}

.form-field-wrapper:focus-within .form-icon {
  color: #1e87f0;
}

.form-input {
  border: 2px solid #e5e5e5;
  border-radius: 12px;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.8);
}

.form-input:focus {
  border-color: #1e87f0;
  box-shadow: 0 0 0 4px rgba(30, 135, 240, 0.1);
  background: white;
  transform: translateY(-1px);
}

.field-status {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
}

.status-icon {
  color: #28a745;
  font-size: 0.9rem;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.8); }
  to { opacity: 1; transform: scale(1); }
}

/* Enhanced Button Styling */
.uk-button-primary {
  background: linear-gradient(135deg, #1e87f0 0%, #0f7ae5 100%);
  border: none;
  border-radius: 12px;
  padding: 0.875rem 1.5rem;
  font-weight: 600;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 12px rgba(30, 135, 240, 0.3);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.uk-button-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.uk-button-primary:hover::before {
  left: 100%;
}

.uk-button-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(30, 135, 240, 0.4);
}

/* Enhanced Alert Styling */
.uk-alert {
  border-radius: 12px;
  border: none;
  padding: 1rem 1.5rem;
  margin: 1rem 0;
  position: relative;
  overflow: hidden;
}

.uk-alert::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
}

.uk-alert-success {
  background: rgba(40, 167, 69, 0.1);
  color: #155724;
  border: 1px solid rgba(40, 167, 69, 0.2);
}

.uk-alert-success::before {
  background: #28a745;
}

.uk-alert-danger {
  background: rgba(220, 53, 69, 0.1);
  color: #721c24;
  border: 1px solid rgba(220, 53, 69, 0.2);
}

.uk-alert-danger::before {
  background: #dc3545;
}

/* Responsive Enhancements */
@media (max-width: 959px) {
  .page-title {
    font-size: 1.8rem;
  }
  
  .card-header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .page-status {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}

@media (max-width: 639px) {
  .page-title {
    font-size: 1.5rem;
  }
  
  .form-input {
    font-size: 16px; /* Prevents zoom on iOS */
  }
}

/* Ensure dropdown appears outside navbar */
.uk-navbar-container {
  position: relative;
  z-index: 1000;
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

/* Simple dropdown styling */
.simple-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 200px;
  z-index: 9999;
  margin-top: 5px;
}

.dropdown-item {
  padding: 16px 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.dropdown-item:last-child {
  border-bottom: none;
}

.dropdown-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(30, 135, 240, 0.08), transparent);
  transition: left 0.4s ease;
}

.dropdown-item:hover::before {
  left: 100%;
}

.dropdown-item:hover {
  background: rgba(30, 135, 240, 0.04);
  transform: translateX(3px);
}

.dropdown-divider {
  height: 1px;
  background: #eee;
  margin: 5px 0;
}

.dropdown-link {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #333;
  text-decoration: none;
  font-size: 14px;
}

.dropdown-link:hover {
  color: #1e87f0;
  text-decoration: none;
}

.logout-link {
  color: #dc3545;
}

.logout-link:hover {
  color: #dc3545;
}

/* Advanced dropdown styling */
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
  padding: 12px 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.dropdown-item:last-child {
  border-bottom: none;
}

.dropdown-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(30, 135, 240, 0.1), transparent);
  transition: left 0.3s ease;
}

.dropdown-item:hover::before {
  left: 100%;
}

.dropdown-item:hover {
  background: rgba(30, 135, 240, 0.05);
  transform: translateX(5px);
}

.dropdown-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0, 0, 0, 0.1), transparent);
  margin: 8px 16px;
}

.dropdown-link {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #333;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  position: relative;
  z-index: 1;
}

.dropdown-link:hover {
  color: #1e87f0;
  text-decoration: none;
}

.dropdown-link .dropdown-icon {
  width: 16px;
  height: 16px;
  transition: transform 0.2s ease;
}

.dropdown-link:hover .dropdown-icon {
  transform: scale(1.1);
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