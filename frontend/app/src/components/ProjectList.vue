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
        axios.get('http://api:8001/api/v1/projects').then((response) => {
            this.projects = response.data
        })
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