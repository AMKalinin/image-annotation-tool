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

export default{
    props:{
        projects:{
            type: Array,
            required: true
        }
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