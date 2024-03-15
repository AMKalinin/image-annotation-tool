<template>
    <div>
        <div class="create_project_tools">
            <button id="createNew"
                type="button"
                class="btn"
                @click="showModal">
                    Create new project
            </button>
            <button id="createBased">Create project based on</button>
        </div>
        <project-list :projects="projects"/>
        <create-project-dialog
            v-show="isModalVisible"
            @close="closeModal"
            @addProject="addProject"
        />
    </div>
</template>

<script>
import ProjectList from '@/components/ProjectList.vue';
import CreateProjectDialog from '@/components/CreateProjectDialog.vue';
import axios from 'axios'

export default{
    components:{ProjectList, CreateProjectDialog},
    data() {
      return {
        isModalVisible: false,
        projects: []
      };
    },
    mounted(){
      axios.get('/projects').then((response) => {
        this.projects = response.data
      })
    },
    methods: {
      showModal() {
        this.isModalVisible = true;
      },
      closeModal() {
        this.isModalVisible = false;
      },
      addProject(projectInfo){
        this.projects.push(projectInfo)
      }
    }
}

</script>

<style>
.create_project_tools{
    position: relative;
    top: 20px;
    left: 30px;
    margin-bottom: 30px;
}

.create_project_tools button{
    border-radius: 6px;
    height: 35px;
    font-size: 90%;
}

#createNew{
    background: #2DA44E;
    border: 1px solid #2A9147;
    color: #FFFFFF;
    margin-right: 45px;
    min-width: 125px;
}

#createBased{
    background: #F6F8FA;
    border: 1px solid #D5D8DA;
    color: #24292F;
    min-width: 160px;
}


</style>