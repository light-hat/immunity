import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// Import UIkit
import 'uikit/dist/css/uikit.min.css';
import UIkit from 'uikit';
import Icons from 'uikit/dist/js/uikit-icons';

UIkit.use(Icons);

// Simple notification system
const app = createApp(App)

// Add UIkit to global properties
app.config.globalProperties.$UIkit = UIkit;

// Add notification method to app
app.config.globalProperties.$notify = function(options) {
  const { type, title, text } = options;
  
  // Create notification element
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.innerHTML = `
    <div class="notification-content">
      <h4>${title}</h4>
      <p>${text}</p>
    </div>
    <button class="notification-close">&times;</button>
  `;
  
  // Add styles
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: ${type === 'success' ? '#d4edda' : '#f8d7da'};
    color: ${type === 'success' ? '#155724' : '#721c24'};
    border: 1px solid ${type === 'success' ? '#c3e6cb' : '#f5c6cb'};
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 10px;
    z-index: 9999;
    max-width: 300px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: flex-start;
    gap: 10px;
  `;
  
  // Add close button styles
  const closeBtn = notification.querySelector('.notification-close');
  closeBtn.style.cssText = `
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    color: inherit;
    padding: 0;
    margin: 0;
    line-height: 1;
  `;
  
  // Add to page
  document.body.appendChild(notification);
  
  // Auto remove after 5 seconds
  setTimeout(() => {
    if (notification.parentNode) {
      notification.parentNode.removeChild(notification);
    }
  }, 5000);
  
  // Close button functionality
  closeBtn.addEventListener('click', () => {
    if (notification.parentNode) {
      notification.parentNode.removeChild(notification);
    }
  });
};

app.use(store)
app.use(router)

// Initialize store
store.commit('initializeStore');

app.mount('#app')
