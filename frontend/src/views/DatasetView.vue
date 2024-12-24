<script>
import {ref, onMounted} from 'vue';
import axios from '@/axios';

export default {
    setup() {
        const datasets = ref([]);

        const name = ref('');
        const description = ref('');
        const language = ref('')

        const handleMarkup = async () => {
            try {
                response = await axios.post(
                    `http://127.0.0.1:81/api/users/dataset/markup/`,
                    {
                        name: name.value,
                        description: description.value,
                        language: language.value,
                    },
                );
            } catch (error) {
                console.error('Error adding labels', error);
            }
        };

        onMounted(async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:81/api/users/dataset/`);
                datasets.value = response.data.data;
            } catch (error) {
                console.error('Error fetching datasets', error)
            }
        });
        return {
            datasets,
            name,
            description,
            language,
            handleMarkup
        }
    }
}
</script>

<template>
    <div class="uk-container uk-container-xlarge">
        <div class="uk-navbar">
            <div class="uk-navbar-left">
                <h2>
                    <span class="uk-icon uk-margin-small-right"
                        uk-icon="icon: database; ratio: 2">
                    </span>
                    Датасет (0)
                </h2>
            </div>
            <div class="uk-navbar-right">

            </div>
        </div>

        <table class="uk-table uk-table-middle uk-table-divider">
            <thead>
                <tr>
                    <th class="uk-center uk-table-shrink">id</th>
                    <th class="uk-center">Текст</th>
                    <th class="uk-center uk-width-small">Метка</th>
                </tr>
            </thead>
            <tbody>

                <tr v-for="dataset in datasets" :key="dataset.id">
                    <td>
                        <a href="#" class="uk-button uk-button-text">{{ dataset.id }}</a>
                    </td>
                    <td class="uk-center">
                        {{ dataset.text }}
                    </td>
                    <td class="uk-center">
                        <span v-if="dataset.label === 'Clean'" class="uk-label uk-label-success">
                            {{ dataset.label }}
                        </span>
                        <span v-else class="uk-label uk-label-danger">
                            {{ dataset.label }}
                        </span>
                    </td>
                </tr>

            </tbody>
        </table>
    </div>
</template>
