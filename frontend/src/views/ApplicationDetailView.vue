<script>
import UIkit from 'uikit';
import axios from 'axios';
import { h, ref } from 'vue'

export default {
  name: 'ApplicationDetailView',
  //components: {
  //  VueFlow,
  //  Background,
  //},
  data() {
    return {
      item: null,
      context_list: null,
      vuln_list: null,
      lib_list: null,
      config_list: null,
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
        const config_data = await axios.get(`/api/users/project/${this.$route.params.id}/config/`);
        const libs_data = await axios.get(`/api/users/project/${this.$route.params.id}/libs/`);
        this.config_list = {...config_data.data.configs}
        this.lib_list = {...libs_data.data.libs}
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
        if (this.isLoading) {
          return;
        }

        this.isLoading = true;
        UIkit.modal('#context-modal').show();
        try {
          const context_request_data = await axios.get(`/api/users/context/${itemId}/`);
          this.selectedContext = {...context_request_data.data};
          this.$forceUpdate();
        } catch (error) {
          console.error('Ошибка при загрузке данных элемента:', error)
          UIkit.notification({ message: 'Не удалось загрузить контекст', status: 'danger' });
        } finally {
          this.isLoading = false;
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
                            <option value="Clean">Уязвимостей не содержит</option>
                            <option value="CWE-352">Подделка межсайтовых запросов (CSRF)</option>
                            <option value="CWE-639">Небезопасная прямая ссылка на объект (IDOR)</option>
                            <option value="CWE-77">Выполнение команд (Command injection)</option>
                            <option value="CWE-79">Межсайтовый скриптинг (XSS)</option>
                            <option value="CWE-89">SQL-инъекция</option>
                            <option value="CWE-16">Уязвимости, связанные с конфигурацией</option>
                            <option value="CWE-502">Десериализация недоверенных данных</option>
                            <option value="CWE-400">Неуправляемое потребление ресурсов</option>
                            <option value="CWE-918">Подделка серверных запросов (SSRF)</option>
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

    <div id="context-modal" class="uk-modal-container" uk-modal>
        <div class="uk-modal-dialog uk-margin-auto-vertical uk-modal-body" style="height: 80vh;" uk-overflow-auto>
            <button class="uk-modal-close-default" type="button" uk-close></button>
            <h3>Контекст выполнения запроса</h3>

            <div v-if="isLoading !== true && selectedContext !== null">
                <div uk-grid>
                    <div class="uk-width-auto@m">

                        <ul class="uk-tab-left" uk-tab="connect: #component-nav; animation: uk-animation-fade">
                            <li><a href="#">HTTP-запрос</a></li>
                            <li><a href="#">HTTP-ответ</a></li>
                            <li><a href="#">Вызовы библиотечных функций</a></li>
                            <li><a href="#">Данные об ошибках</a></li>
                            <li><a href="#">Граф потока управления</a></li>
                        </ul>

                    </div>
                    <div class="uk-width-expand@m">

                        <div id="component-nav" class="uk-switcher">
                            <div>
                                <dl class="uk-description-list uk-description-list-divider">
                                    <dt>Метод</dt>
                                    <dd v-if="selectedContext.request.method !== null">{{ selectedContext.request.method }}</dd>
                                    <dd v-else>Информация отсутствует</dd>
                                    <dt>Адрес</dt>
                                    <dd v-if="selectedContext.request.path !== null">{{ selectedContext.request.path }}</dd>
                                    <dd v-else>Информация отсутствует</dd>
                                    <dt>Заголовки запроса</dt>
                                    <dd>
                                        <pre><code><span v-for="(value, key) in selectedContext.request.headers" :key="key">{{ key }}: {{ value }}<br></span></code></pre>
                                    </dd>
                                    <dt>Параметры запроса</dt>
                                    <dd v-if="selectedContext.request.get_params !== null">
                                        <pre><code>{{ selectedContext.request.get_params }}</code></pre>
                                    </dd>
                                    <dd v-else>Отсутствуют</dd>
                                    <dt>Тело запроса</dt>
                                    <dd><pre><code>{{ selectedContext.request.body }}</code></pre></dd>
                                    <dt>Передаваемые файлы</dt>
                                    <dd v-if="selectedContext.request.files !== null">
                                        <pre><code>{{ selectedContext.request.files }}</code></pre>
                                    </dd>
                                    <dd v-else>Отсутствуют</dd>
                                    <dt>Пользователь</dt>
                                    <dd v-if="selectedContext.request.user !== null">{{ selectedContext.request.user }}</dd>
                                    <dd v-else>Информация отсутствует</dd>
                                </dl>
                            </div>
                            <div>
                                <dl class="uk-description-list uk-description-list-divider">
                                    <dt>Код ответа</dt>
                                    <dd v-if="selectedContext.response.status_code !== null">{{ selectedContext.response.status_code }}</dd>
                                    <dd v-else>Информация отсутствует</dd>
                                    <dt>Содержимое ответа</dt>
                                    <dd>
                                        <code><pre>{{ selectedContext.response.body }}</pre></code>
                                    </dd>
                                    <dt>Заголовки ответа</dt>
                                    <dd>
                                        <pre><code><span v-for="(value, key) in selectedContext.response.headers" :key="key">{{ key }}: {{ value }}</span></code></pre>
                                    </dd>
                                    <dt>Content-Type</dt>
                                    <dd v-if="selectedContext.response.content_type !== null">
                                        <pre><code>{{ selectedContext.response.content_type }}</code></pre>
                                    </dd>
                                    <dd v-else>-</dd>
                                    <dt>Content-Length</dt>
                                    <dd v-if="selectedContext.response.content_length !== null">
                                        <pre><code>{{ selectedContext.response.content_length }}</code></pre>
                                    </dd>
                                    <dd v-else>-</dd>
                                    <dt>Кодировка</dt>
                                    <dd v-if="selectedContext.response.charset !== null">{{ selectedContext.response.charset }}</dd>
                                    <dd v-else>Информация отсутствует</dd>
                                </dl>
                            </div>
                            <div>
                                <table class="uk-table uk-table-divider">
                                    <thead>
                                        <tr>
                                            <th>Библиотека</th>
                                            <th>Функция</th>
                                            <th>Временная метка</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="item in selectedContext.events.filter(i => i.external_call === true)" :key="item.id">
                                            <td>{{item.module}}</td>
                                            <td>{{item.func_name}}</td>
                                            <td>{{item.timestamp}}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <div>
                                <table class="uk-table uk-table-divider">
                                    <thead>
                                        <tr>
                                            <th>Тип исключения</th>
                                            <th>Модуль</th>
                                            <th>Файл</th>
                                            <th>Имя функции</th>
                                            <th>Строка</th>
                                            <th>Сообщение</th>
                                            <th>Временная метка</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="item in selectedContext.events.filter(i => i.type === 'error')" :key="item.id">
                                            <td>{{item.exception_type}}</td>
                                            <td>{{item.module}}</td>
                                            <td>{{item.filename}}</td>
                                            <td>{{item.func_name}}</td>
                                            <td>{{item.line}}</td>
                                            <td>{{item.exception_message}}</td>
                                            <td>{{item.timestamp}}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <div>
                                To be continued...
                            </div>
                        </div>

                    </div>
                </div>
            </div>
            <div v-else>
                <span class="uk-margin-small-right" uk-spinner="ratio: 3"></span>
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
                                        <li><a @click="openModal(context.context_id)" uk-icon="icon: link-external"></a></li>
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

                    <table class="uk-table uk-table-middle uk-table-divider">
                        <thead>
                            <tr>
                                <th class="uk-width-small">Библиотека</th>
                                <th class="uk-width-small">Версия</th>
                                <th class="uk-width-small">Безопасность</th>
                                <th class="uk-width-small">Уязвимости</th>
                                <th class="uk-width-small">Рекомендуемые версии</th>
                            </tr>
                        </thead>
                        <tbody>

                            <tr v-for="vul_lib in lib_list" :key="vul_lib.id">
                                <td>
                                    {{ vul_lib.key }}
                                </td>
                                <td>
                                    {{ vul_lib.value }}
                                </td>
                                <td>
                                    <span v-if="vul_lib.vulnerable" class="uk-label uk-label-danger">Уязвима</span>
                                    <span v-else class="uk-label uk-label-success">Безопасна</span>
                                </td>
                                <td>
                                    <span v-if="vul_lib.vulnerable">
                                    <ul>
                                        <li v-for="lib_vuln in vul_lib.vulnerabilities" :key="lib_vuln.id"><span class="uk-label uk-label-danger">{{lib_vuln.label}}</span></li>
                                    </ul>
                                    </span>
                                    <span v-else>-</span>
                                </td>
                                <td>
                                    <span v-if="vul_lib.vulnerable">
                                    <ul>
                                        <li v-for="lib_vuln in vul_lib.vulnerabilities" :key="lib_vuln.id"><span class="uk-label">{{lib_vuln.recommended_version}}</span></li>
                                    </ul>
                                    </span>
                                    <span v-else>-</span>
                                </td>
                            </tr>

                        </tbody>
                    </table>

                </div>
                <div>

                    <table class="uk-table uk-table-middle uk-table-divider" v-if="config_list !== null">
                        <thead>
                            <tr>
                                <th class="uk-width-small">Параметр</th>
                                <th class="uk-width-small">Значение</th>
                                <th class="uk-width-small">Безопасность</th>
                                <th class="uk-width-small">Метка уязвимости</th>
                                <th class="uk-width-small">Сообщение</th>
                            </tr>
                        </thead>
                        <tbody>

                            <tr v-for="vul_conf in config_list" :key="vul_conf.id">
                                <td>
                                    {{ vul_conf.key }}
                                </td>
                                <td>
                                    {{ vul_conf.value }}
                                </td>
                                <td>
                                    <span class="uk-label uk-label-danger" v-if="vul_conf.vulnerable">Уязвим</span>
                                    <span class="uk-label uk-label-success" v-else>Безопасен</span>
                                </td>
                                <td>
                                    <span class="uk-label uk-label-danger" v-if="vul_conf.vulnerable">CWE-16</span>
                                    <span v-else>-</span>
                                </td>
                                <td>
                                    {{ vul_conf.message }}
                                </td>
                            </tr>

                        </tbody>
                    </table>

                </div>
            </div>

        </div>

    </div>
    <div class="uk-position-center uk-center" v-else>
        <span uk-icon="icon: warning; ratio: 1"></span> Такого проекта не существует.
    </div>
</template>

<style>
@import "@vue-flow/core/dist/style.css";

body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>