<script>
import UIkit from 'uikit';
import axios from 'axios';

export default {
  name: 'ApplicationDetailView',
  data() {
    return {
      item: null,
      context_list: null,
      vuln_list: null,
      project: null,
      label: '',
      file: '',
      line: null,
      intervalId: null,
      handleMarkup: null,
      selectedContext: null,
      isLoading: false,
    };
  },
  created() {
    this.fetchItem();
    this.startPolling();
  },
  beforeUnmount() {
    clearInterval(this.intervalId);
  },
  methods: {
    async fetchItem() {
      try {
        const response = await axios.get(`/api/users/project/${this.$route.params.id}/`);
        const context_list_response = await axios.get(`/api/users/context/?project=${this.$route.params.id}`);
        const vuln_list_response = await axios.get(`/api/users/vulnerability/?project=${this.$route.params.id}`);
        this.item = {...response.data.data};
        this.context_list = {...context_list_response.data.data.contexts};
        this.vuln_list = {...vuln_list_response.data.data};
        this.$forceUpdate();
      } catch (error) {
        console.error('Ошибка при получении данных:', error);
      }
    },
    startPolling() {
      this.intervalId = setInterval(() => {
        this.fetchItem();
      }, 3000);
    },
    async handleMarkup() {
        try {
            const datasetLabel = {
              ...this.item,
              project: this.item.id,
              label: this.label,
              file: this.file,
              line: this.line
            };

            const response = await axios.post(
              `/api/users/dataset/markup/`,
              datasetLabel
            );

            if (response.status === 200) {
              UIkit.notification({message: 'Данные размечены', status: 'success'});
            } else {
              UIkit.notification({message: 'Произошла ошибка', status: 'danger'});
            }
        } catch (error) {
            console.error('Ошибка при отправке данных:', error);
            UIkit.notification({message: 'Ошибка', status: 'danger'})
        }
    },
    async openModal(itemId) {
      this.isLoading = true;
      this.selectedContext = null;
      try {
        const context_request_data = await axios.get(`/api/users/context/${itemId}/`);
        this.selectedContext = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке данных элемента:", error);
      } finally {
        this.isLoading = false;
        UIkit.modal("#context-modal").show();
      }
    },
  },
};
</script>

<template>

    <div id="vuln_set_modal" uk-modal>
        <div class="uk-modal-dialog">
            <button class="uk-modal-close-full uk-close-large" type="button" uk-close></button>

            <div class="uk-modal-header">
                <h2>Уязвимый участок для датасета</h2>
            </div>

            <form @submit.prevent="handleMarkup">

                <div class="uk-modal-body">
                    <div class="uk-margin">
                        <input v-model="file"
                              type="text"
                              placeholder="Путь к файлу"
                              class="uk-input"
                              required />
                    </div>

                    <div class="uk-margin">
                        <input v-model="line"
                              type="number"
                              placeholder="Номер строки"
                              class="uk-input"
                              required />
                    </div>

                    <div class="uk-margin">
                        <select v-model="label" type="text" class="uk-select" placeholder="Метка">
                            <option value="Clean">Уязвимости нет</option>
                            <option value="CWE">Уязвимость</option>
                        </select>
                    </div>

                </div>

                <div class="uk-modal-footer uk-text-right">
                    <div class="uk-navbar">
                        <div class="uk-navbar-left">
                            <button class="uk-button uk-button-default uk-modal-close" type="button">Cancel</button>
                        </div>
                        <div class="uk-navbar-right">
                            <button class="uk-button uk-button-secondary" type="submit" :disabled="loading">Разметить</button>
                        </div>
                    </div>
                </div>

            </form>

        </div>
    </div>

    <div id="context-modal" uk-modal v-if="selectedContext">
        <div class="uk-modal-dialog uk-modal-body">
            <button class="uk-modal-close-default" type="button" uk-close></button>
            <h2 class="uk-modal-title">Контекст выполнения запроса</h2>

            <div v-if="isLoading">
                <p>Загрузка данных...</p>
            </div>

            <div v-else>
                <p><strong>ID:</strong> {{ selectedContext.id }}</p>
            </div>
        </div>
    </div>

    <div v-if="item">

        <div class="uk-container uk-container-xlarge">
            <div class="uk-navbar">
                <div class="uk-navbar-left">
                    <div>
                        <h2>
                            <span class="uk-icon uk-margin-small-right"
                                uk-icon="icon: tv; ratio: 2">
                            </span>
                            {{ item.name }}
                        </h2>
                        <p class="uk-article-meta">{{ item.description }}</p>
                    </div>
                </div>
                <div class="uk-navbar-right">
                    <a href="#vuln_set_modal" class="uk-button uk-button-secondary" uk-toggle>
                        <span class="uk-icon uk-margin-small-right"
                            uk-icon="icon: plus">
                        </span>
                        Указать уязвимый участок
                    </a>
                </div>
            </div>

            <ul uk-tab>
                <li><a href="#">Мониторинг</a></li>
                <li><a href="#">Уязвимости</a></li>
                <li><a href="#">Внешние зависимости</a></li>
                <li><a href="#">Конфигурация</a></li>
            </ul>
            <div class="uk-switcher uk-margin">
                <div>

                    <table class="uk-table uk-table-middle uk-table-divider">
                        <thead>
                            <tr>
                                <th class="uk-table-shrink">ID</th>
                                <th class="uk-width-small">URL</th>
                                <th class="uk-width-small">Запрос</th>
                                <th class="uk-width-small">Безопасность</th>
                                <th class="uk-table-shrink">Код ответа</th>
                                <th class="uk-table-shrink"></th>
                            </tr>
                        </thead>
                        <tbody>

                            <tr v-for="context in context_list" :key="context.context_id">
                                <td>
                                    {{ context.context_id }}
                                </td>
                                 <td>
                                    {{ context.request.url }}
                                </td>
                                <td>
                                    <span class="uk-label">{{ context.request.method }}</span>
                                </td>
                                <td>
                                    <span v-if="context.vulnerable" class="uk-label uk-label-danger">Уязвим</span>
                                    <span v-else class="uk-label uk-label-success">Безопасен</span>
                                </td>
                                <td>
                                    <span v-if="context.response.status_code[0] == '2'" class="uk-label uk-label-success">
                                        {{ context.response.status_code }}
                                    </span>
                                    <span v-else-if="context.response.status_code[0] == '4'" class="uk-label uk-label-warning">
                                        {{ context.response.status_code }}
                                    </span>
                                    <span v-else-if="context.response.status_code[0] == '5'" class="uk-label uk-label-danger">
                                        {{ context.response.status_code }}
                                    </span>
                                    <span class="uk-label" v-else>
                                        {{ context.response.status_code }}
                                    </span>
                                </td>
                                <td>
                                    <ul class="uk-iconnav">
                                        <li><a @click="openModal(item.id)" uk-icon="icon: link-external"></a></li>
                                    </ul>
                                </td>
                            </tr>

                        </tbody>
                    </table>

                </div>
                <div>

                    <table class="uk-table uk-table-middle uk-table-divider">
                        <thead>
                            <tr>
                                <th class="uk-table-shrink">ID</th>
                                <th class="uk-width-small">Тип уязвимости</th>
                                <th class="uk-width-small">CWE</th>
                                <th class="uk-width-small">Дата и время обнаружения</th>
                                <th class="uk-width-small"></th>
                            </tr>
                        </thead>
                        <tbody>

                            <tr v-for="vuln in vuln_list" :key="vuln.id">
                                <td>
                                    {{ vuln.id }}
                                </td>
                                <td>
                                    <span class="uk-label uk-label-danger">{{ vuln.type }}</span>
                                </td>
                                <td>
                                    <span class="uk-label">{{ vuln.cwe }}</span>
                                </td>
                                <td>
                                    {{ vuln.detected_at }}
                                </td>
                                <td>
                                    <ul class="uk-iconnav">
                                        <li><a @click="openModal(vuln.context_id)" uk-icon="icon: link-external"></a></li>
                                    </ul>
                                </td>
                            </tr>

                        </tbody>
                    </table>

                </div>
                <div>

                    Зависимости проекта

                </div>
                <div>

                    Данные о конфигурации

                </div>
            </div>

        </div>

    </div>
    <div class="uk-position-center uk-center" v-else>
        <span uk-icon="icon: warning; ratio: 1"></span> Такого проекта не существует.
    </div>
</template>
