<template>
    <div class="taskList">
        <task-item 
            v-for="task in tasks" :key="task.id"
            :task="task"
        />
    </div>
</template>

<script>
import TaskItem from './TaskItem.vue'
import axios from 'axios'

export default{
    data(){
        return{
            tasks: []
        }
    },
    mounted(){
        axios.get('/projects/'+this.$route.params.projectName+'/tasks').then((response) => {
            this.tasks = response.data
        })
    },
    components:{TaskItem}
}
</script>


<style>
.taskList
{   
    height: 94vh;
    position: relative;
    overflow: auto;
}
</style>