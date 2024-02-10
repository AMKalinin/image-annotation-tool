<template>
    <div class="projectList">
        <project-item 
            v-for="project in projects" :key="project.name"
            :project="project"
        />
    </div>
</template>

<script>
import ProjectItem from './ProjectItem.vue'
import axios from 'axios'

export default{
    data(){
        return{
            projects: []
        }
    },
    mounted(){
        axios.get('/projects').then((response) => {
            this.projects = response.data
        }).catch(function (error) {
            if (error.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
            } else if (error.request) {
            // The request was made but no response was received
            // `error.request` is an instance of XMLHttpRequest in the browser
            // and an instance of http.ClientRequest in node.js
            console.log(error.request);
            } else {
            // Something happened in setting up the request that triggered an Error
            console.log('Error', error.message);
            }
        });
    },
    components:{ProjectItem}
}
</script>


<style>
.projectList
{   
    height: 94vh;
    position: relative;
    overflow: auto;
}
</style>