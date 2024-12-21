<script>
import {ref, onMounted} from 'vue';
import axios from '@/axios';
import {useAuthStore} from '@/stores/auth';

export default {
    setup() {
        const auth = useAuthStore();
        const projects = ref([]);

        const name = ref('');
        const description = ref('');
        const language = ref('')

        const handleCreateProject = async () => {
            try {
                response = await axios.post(
                    `http://${window.API_HOST}:${window.API_PORT}/api/users/project/`,
                    {
                        name: name.value,
                        description: description.value,
                        language: language.value,
                    },
                    {
                        headers: {
                            Authorization: `Bearer ${auth.accessToken}`,
                        },
                    },
                );
            } catch (error) {
                console.error('Error creating project', error);
            }
        };

        onMounted(async () => {
            try {
                const response = await axios.get(`http://${window.API_HOST}:${window.API_PORT}/api/users/project/`, {
                    headers: {
                        Authorization: `Bearer ${auth.accessToken}`,
                    },
                });
                projects.value = response.data.data;
            } catch (error) {
                console.error('Error fetching projects', error)
            }
        });
        return {
            projects,
            name,
            description,
            language,
            handleCreateProject
        }
    }
}

</script>

<template>
    <div id="create_project_modal" class="uk-modal-full" uk-modal>
        <div class="uk-modal-dialog">
            <button class="uk-modal-close-full uk-close-large" type="button" uk-close></button>
            <div class="uk-grid-collapse uk-child-width-1-2@s uk-flex-middle" uk-grid>

                <div class="uk-padding-large" uk-overflow-auto uk-height-viewport>
                    <article class="uk-article">
                        <h1 class="uk-article-title">Инструментирование веб-приложения</h1>
                        <p class="uk-text-lead">Тут в общем будет описано как установить агента и как его встроить в Django/Flask-приложение.</p>
                        <p>И может ещё до кучи напишу про докеризацию такого приложения и CI/CD. Если успею.</p>
                        <ul uk-tab>
                            <li><a href="#">Django</a></li>
                            <li><a href="#">Flask</a></li>
                        </ul>
                        <div class="uk-switcher uk-margin">
                            <div>123</div>
                            <div>321</div>
                        </div>
                        <p>Прочее содержимое.</p>
                    </article>
                </div>

                <div class="uk-padding-large">
                    <div class="uk-light uk-background-secondary uk-padding uk-flex uk-flex-middle uk-width-1-2">

                        <form @submit.prevent="handleCreateProject">

                            <h3>Создать новый проект</h3>

                            <fieldset class="uk-fieldset">

                                <div class="uk-margin">
                                    <input v-model="name"
                                          type="text"
                                          placeholder="Название проекта"
                                          class="uk-input uk-form-width-large"
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
                                    <select v-model="language" type="text" class="uk-select" aria-label="Язык программирования">
                                        <option value="python">Python</option>
                                    </select>
                                </div>

                                <button class="uk-button uk-button-default" type="submit" :disabled="loading">Создать</button>

                            </fieldset>

                        </form>

                    </div>
                </div>

            </div>
        </div>
    </div>
    <div class="uk-container uk-container-xlarge">
        <div class="uk-navbar">
            <div class="uk-navbar-left">
                <h2>
                    <span class="uk-icon uk-margin-small-right"
                        uk-icon="icon: server; ratio: 2">
                    </span>
                    Проекты ({{ projects.length }})
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
                    <th class="uk-center">Активные уязвимости</th>
                    <th class="uk-center">Статус</th>
                    <th class="uk-center">Последнее взаимодействие</th>
                    <th class="uk-center">Дата подключения</th>
                </tr>
            </thead>
            <tbody>

                <tr v-for="project in projects" :key="project.id">
                    <td>
                        <a href="#" class="uk-button uk-button-text">{{ project.name }}</a>
                    </td>
                    <td class="uk-center">
                        <span class="uk-label uk-label-default">
                            {{ project.language }}
                        </span>
                    </td>
                    <td class="uk-center">
                        <span class="uk-label uk-label-danger">
                            12
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
