<template>
    <div class="workarea">
        <Tool-Bar class="tool"></Tool-Bar>
        <View-Edit 
            class="edit" 
            :masks="masks" 
            ref="childComponent"
            @changeMaskVisibilityFlag="changeMaskVisibilityFlag"
            @changeMaskBacklightFlag="changeMaskBacklightFlag"
            @addMask="addMask">
        </View-Edit>
        <control-edit
            :masks="masks"
            :classList="classList"
            @changeMaskVisibilityFlag="changeMaskVisibilityFlag"
            @changeMaskBacklightFlag="changeMaskBacklightFlag"
            @deleteMask="deleteMask">
        </control-edit>
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
            masks: {},
            classList: []
        }
    },
    mounted(){
        axios.get('/projects/'+this.$route.params.projectName+'/tasks/'+this.$route.params.id+'/masks').then((response) => {
            let maskList = response.data
            for (let i=0; i<maskList.length; i++){
                maskList[i].visibilityFlag = true
                maskList[i].backlightFlag = false
                maskList[i].points = this.strToPointList(maskList[i].points)
                this.masks[maskList[i].id] = maskList[i]
            }
        })
        axios.get('/projects/'+this.$route.params.projectName+'/classes').then((response) => {
            this.classList = response.data
        })
    },
    methods: {
        strToPointList(pointStr){
            let pointsNumber = []
            let pointsList = pointStr.split('|')
            for (let i=0; i<pointsList.length; i++){
                let tmp = pointsList[i].split(',')
                pointsNumber.push([Number(tmp[0]),Number(tmp[1])])
            }
        return pointsNumber
        },
        changeMaskVisibilityFlag(maskId){
            this.masks[maskId].visibilityFlag = !this.masks[maskId].visibilityFlag 
        },
        changeMaskBacklightFlag(maskId){
            this.masks[maskId].backlightFlag = !this.masks[maskId].backlightFlag 
        },
        deleteMask(maskId){
            delete this.masks[maskId]
            // Надо отправить запрос об удалении на бэк
        },
        addMask(maskItem){
            maskItem.visibilityFlag = true
            maskItem.backlightFlag = false
            this.masks[maskItem.id] = maskItem
        }
    }
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