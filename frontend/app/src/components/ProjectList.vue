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
        })
    },
    components:{ProjectItem}
}
</script>


<style>
.projectList
{   
    height: 87vh;
    position: relative;
    overflow: auto;
}
</style>