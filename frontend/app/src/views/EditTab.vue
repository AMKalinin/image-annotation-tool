<template>
    <div class="workarea">
        <Tool-Bar class="tool"></Tool-Bar>
        <View-Edit class="edit" :masks="masks"></View-Edit>
        <control-edit :masks="masks" :classList="classList"></control-edit>
    </div>
</template>

<script>
import axios from 'axios'
import ToolBar from '@/components/ToolBar.vue'
import ViewEdit from '@/components/ViewEdit.vue'
import ControlEdit from '@/components/ControlEdit.vue'

export default{
    components:{ToolBar, ViewEdit, ControlEdit},
    data(){
        return{
            masks: [],
            classList: []
        }
    },
    mounted(){
        axios.get('/projects/'+this.$route.params.projectName+'/tasks/'+this.$route.params.id+'/masks').then((response) => {
            this.masks = response.data
        })
        axios.get('/projects/'+this.$route.params.projectName+'/classes').then((response) => {
            console.log(response.data)
            this.classList = response.data
        })
    },
}
</script>

<style>
.workarea {  
    display: grid;
    grid-template-columns:  0.1fr 2.3fr 0.6fr; 
    grid-template-rows: 1fr;
    gap: 0px 0px;
    grid-template-areas:
        "tool edit controlEdit";
}

.tool {
    grid-area: tool;
    height: 100%;
}


</style>