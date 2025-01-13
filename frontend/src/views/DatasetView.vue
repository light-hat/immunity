<script>
import {ref, onMounted} from 'vue';
import axios from '@/axios';

export default {
    setup() {
        const datasets = ref([]);
        const counters = ref({});

        const name = ref('');
        const description = ref('');
        const language = ref('');

        const handleMarkup = async () => {
            try {
                response = await axios.post(
                    `/api/users/dataset/markup/`,
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
                const response = await axios.get(`/api/users/dataset/`);
                datasets.value = response.data.data;
                const response_counters = await axios.get(`/api/users/dataset/counters/`);
                counters.value = response_counters.data;
            } catch (error) {
                console.error('Error fetching datasets', error)
            }
        });
        return {
            datasets,
            counters,
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
                    Датасет
                </h2>
            </div>
            <div class="uk-navbar-right">

            </div>
        </div>

        <dl class="uk-description-list">
            <dt>Без уязвимостей</dt>
            <dd>{{ counters.Clean }} шт.</dd>
            <dt>CWE-352</dt>
            <dd>{{ counters.CWE352 }} шт.</dd>
            <dt>CWE-639</dt>
            <dd>{{ counters.CWE639 }} шт.</dd>
            <dt>CWE-77</dt>
            <dd>{{ counters.CWE77 }} шт.</dd>
            <dt>CWE-79</dt>
            <dd>{{ counters.CWE79 }} шт.</dd>
            <dt>CWE-89</dt>
            <dd>{{ counters.CWE89 }} шт.</dd>
            <dt>CWE-16</dt>
            <dd>{{ counters.CWE16 }} шт.</dd>
            <dt>CWE-502</dt>
            <dd>{{ counters.CWE502 }} шт.</dd>
            <dt>CWE-400</dt>
            <dd>{{ counters.CWE400 }} шт.</dd>
            <dt>CWE-918</dt>
            <dd>{{ counters.CWE918 }} шт.</dd>
        </dl>

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
