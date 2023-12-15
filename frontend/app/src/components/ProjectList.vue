<template>
    <div class="projectList">
        <project-item 
            v-for="project in projects" :key="project.id"
            :project="project"
        />
    </div>
</template>

<script>
import ProjectItem from './ProjectItem.vue';

export default{
    data(){
        return{
            projects: [{
                id:0,
                name:'Prj 1',
                task:{done:10,
                    all:20},
                lastUpdate: '20.09.2023'
                },
                {
                id:1,
                name:'Prj 2',
                task:{done:1,
                    all:4},
                lastUpdate: '21.09.2023'
                },
                {
                id:1,
                name:'Prj 2',
                task:{done:1,
                    all:4},
                lastUpdate: '21.09.2023'
                },
                {
                id:1,
                name:'Prj 2',
                task:{done:1,
                    all:4},
                lastUpdate: '21.09.2023'
                },
                {
                id:1,
                name:'Prj 2',
                task:{done:1,
                    all:4},
                lastUpdate: '21.09.2023'
                },
                {
                id:1,
                name:'Prj 2',
                task:{done:1,
                    all:4},
                lastUpdate: '21.09.2023'
                }
            ]
        }
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