<script>
import {ref, onMounted} from 'vue';
import axios from '@/axios';

export default {
    setup() {
        const projects = ref([]);

        const name = ref('');
        const description = ref('');
        const language = ref('');

        const handleCreateProject = async () => {
            try {
                response = await axios.post(
                    `/api/users/project/`,
                    {
                        name: name.value,
                        description: description.value,
                        language: language.value,
                    },
                );
            } catch (error) {
                console.error('Error creating project', error);
            }

            window.location.reload();
        };

        onMounted(async () => {
            try {
                const response = await axios.get(`/api/users/project/`);
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
