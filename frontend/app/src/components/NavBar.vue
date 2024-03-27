<template>
    <div>
        <ul class="navBar" @click="updateColor">
            <li class="navItem" >
                <router-link to="/projects" :id = "currentPath != projectsPath ||'active'">Projects</router-link>
            </li>
            <li class="navItem">
                <router-link to="/tasks" :id = "currentPath != tasksPath || 'active'">Tasks</router-link>
            </li>
            
            <li class="navItem">
                <router-link to="/view" :id = "currentPath != viewPath || 'active'" >View</router-link>
            </li>
        </ul>
    </div>
</template>

<script>
import { RouterLink } from 'vue-router';

export default{
    data() {
        return {
            currentPath: window.location.pathname,
            projectsPath: '/projects',
            tasksPath: '/tasks',
            viewPath: '/view'
        };
    },
    methods: {
        updateColor(){
            this.currentPath = window.location.pathname
        }
    },
    components:{RouterLink}
}
</script>

<style scoped>

.navBar
{
    list-style-type: none;
    margin: 0;
    padding: 0;
    overflow: hidden;
    background: #2C2C2C;
    top: 0;
    left: 0;
    height: 100%;
    min-height: 60px;
    max-height: 60px;
}

.navItem {
    float: left;
    margin: 0.9%;
}

#active {
    color: #828EFF;
    text-decoration: underline; 
}

.navItem a{
    position: relative;
    display: block;
    color: white;
    text-align: center;
    text-decoration: none;
    font-size: 150%;
}

</style>