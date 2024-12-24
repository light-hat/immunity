<script setup>
import {computed} from 'vue';
</script>

<template>
    <div class="uk-background-secondary">
        <nav class="uk-navbar-container uk-navbar-transparent uk-light">
            <div class="uk-container uk-container-xlarge">
                <div uk-navbar>

                    <div class="uk-navbar-left">

                        <img src="../assets/favicon_white.png"
                        alt=""
                        width="48"
                        height="48">

                    </div>

                    <div class="uk-navbar-right">

                        <ul class="uk-navbar-nav">

                            <li v-if="$route.path === '/'" class="uk-active">
                                <a href="/">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: server">
                                    </span>
                                    Проекты
                                </a>
                            </li>
                            <li v-else>
                                <a href="/">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: server">
                                    </span>
                                    Проекты
                                </a>
                            </li>

                            <li v-if="$route.path === '/dataset'" class="uk-active">
                                <a href="/dataset">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: database">
                                    </span>
                                    Датасет
                                </a>
                            </li>
                            <li v-else>
                                <a href="/dataset">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: database">
                                    </span>
                                    Датасет
                                </a>
                            </li>
                        </ul>

                    </div>

                </div>
            </div>
        </nav>
    </div>
</template>

<style scoped>
nav {
    margin-bottom: 2em;
}

.img {
    margin-top: 1em;
}
</style>
