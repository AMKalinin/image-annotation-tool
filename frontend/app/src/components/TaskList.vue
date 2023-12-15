<template>
    <div class="taskList">
        <task-item 
            v-for="task in tasks" :key="task.id"
            :task="task"
        />
    </div>
</template>

<script>
import TaskItem from './TaskItem.vue';

export default{
    data(){
        return{
            tasks: [{
                id:0,
                status:0},
                {
                id:1,
                status:1},
                {
                id:2,
                status:1},
                {
                id:3,
                status:1},
                {
                id:4,
                status:1},
                {
                id:5,
                status:1},
                {
                id:6,
                status:1},
                {
                id:7,
                status:1},
                {
                id:8,
                status:1},
                {
                id:9,
                status:1}
            ]
        }
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