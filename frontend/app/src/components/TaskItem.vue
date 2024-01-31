<template>
    <fieldset class="task" :id="task.id">
        <img class="imgTask" :src="'http://api:8001/api/v1/projects/'+task.project_name+'/tasks/'+task.id+'/icon'">
        <div>
            ID: {{task.id}}<br>
            <div v-if="task.status == 'OK'">
                <button class="btnEdit" @click="$router.push({ path: `/edit/${task.project_name}/${task.id}`})">Edit</button><br>
            </div>
            <div v-else>
                <button class="btnView" @click="$router.push('/inspect')">Inspect</button><br>
            </div>
        </div>
    </fieldset>
</template>


<script>
export default{
    props:{
        task:{
            type: Object,
            required: true
        }
    }
}
</script>


<style>

.task{
    margin-top: 10px;
    position:relative;
    height: 111px;
    padding: 0px;
    margin-bottom: 5px;
    border: 0px;
    background: rgba(177, 199, 255, 0.43);
    border-radius: 20px;
}

.task div{
    margin-left: 120px;
    margin-top: 10px;
}

.imgTask{
    position:absolute; 
    top:8px;
    left:10px;
    width: 95px;
    height: 95px;
}

.btnEdit{
    background: #6E98FE;
    border: 1px solid #2A4791;
    border-radius: 6px;
    position:absolute; 

    width: 90px;
    height: 25px;
    
    top: 20px;
    right: 20px;
}

.btnView{
    background: #2DA44E;
    border: 1px solid #2A9147;
    border-radius: 6px;
    position:absolute; 

    width: 90px;
    height: 25px;
    
    top: 20px;
    right: 20px;
    color: #FFFFFF;
}


.selected {
    opacity: 0.6;
  }

button a{
    color: black;
    text-align: center;
    text-decoration: none;
}
</style>