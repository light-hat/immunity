<script setup>
import {computed} from 'vue';
import {useAuthStore} from '../stores/auth';

const authStore = useAuthStore();
const isAuthenticated = computed(() => authStore.isAuthenticated);
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

                        <a v-if="$route.path === '/login'"
                        href="/login"
                        class="uk-navbar-item uk-logo"
                        aria-label="Back to Home">
                            Авторизация
                        </a>
                        <a v-if="$route.path === '/register'"
                        href="/register"
                        class="uk-navbar-item uk-logo"
                        aria-label="Back to Home">
                            Создать аккаунт
                        </a>
                        <a v-if="isAuthenticated" href="/"
                        class="uk-navbar-item uk-logo"
                        aria-label="Back to Home">
                            Immunity IAST
                        </a>

                    </div>

                    <div class="uk-navbar-right" v-if="isAuthenticated">

                        <ul class="uk-navbar-nav">

                            <li v-if="$route.path === '/application'" class="uk-active">
                                <a href="/application">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: server">
                                    </span>
                                    Проекты
                                </a>
                            </li>
                            <li v-else>
                                <a href="/application">
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

                            <li v-if="$route.path === '/profile'" class="uk-active">
                                <a href="/profile">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: user">
                                    </span>
                                    Личный кабинет
                                </a>
                            </li>
                            <li v-else>
                                <a href="/profile">
                                    <span class="uk-icon uk-margin-small-right"
                                        uk-icon="icon: user">
                                    </span>
                                    Личный кабинет
                                </a>
                            </li>
                        </ul>

                    </div>
                    <div class="uk-navbar-right" v-else>
                        <a v-if="$route.path === '/login'"
                            class="uk-button uk-button-default"
                            href="/register">Регистрация</a>

                        <a v-if="$route.path === '/register'"
                            class="uk-button uk-button-default"
                            href="/login">Авторизация</a>
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
