<template>
    <div class="maska">
        <div class="colorImg" :style="'background:' + mask.color + ';'"></div>

        <div class="contentMask">
            <label class="maskName">Name: {{mask.name}}</label> <br>
            
            <label class="check" ondblclick="event.stopPropagation();">
                <input value="{{mask.points}};{{mask.color}}" type="checkbox" class="maskaViewCheck">
                <span class="checkbox"></span>
            </label>

            <img
                v-if="typeMask === 0" 
                class="deleteBtn" 
                :src="imageTrash"
                title="Polygon" 
                ondblclick="event.stopPropagation();"
            >

            <label class="type">Type: {{ mask.type }} </label> <br>
            <label v-if="typeMask === 0">Class:   
                <select class="selectClass">
                    <option
                        v-if="mask.classCode == '000'"
                        value='{{project_name}};{{task_index}};{{mask.name}};{{mask.class_code}};{{mask.color}}'
                        >
                            Класс не выбран
                    </option>
                    <option
                        v-if="mask.classCode != '000'"
                        value='{{project_name}};{{task_index}};{{mask.name}};{{mask.class_code}};{{mask.color}}'
                        >
                            {{ mask.className }}
                    </option>
                    <option
                        v-if="mask.classCode != '000'"
                        value='{{project_name}};{{task_index}};{{mask.name}};000;#c0c0c0'
                        >
                            Класс не выбран
                    </option>
                    <template v-for="cls in classesList" :key="cls[0]">
                        <option 
                            v-if="mask.classCode != cls[2]"
                            value='{{projectName}};{{taskIndex}};{{mask.name}};{{cls[0]}};{{cls[3]}}'
                            >
                            {{cls[0]}}
                        </option>
                    </template>
                </select>
            </label>
            <label v-else-if="mask.classCode == '000'">
                Class: не выбран
            </label>
            <label v-else>
                Class: {{ mask.className }}
            </label>

        </div>
    </div>
</template>

<script>
import imageTrash from '../images/trash.svg';

export default{
    data(){
        return{
            projectName: 'asd',
            taskIndex: 0,
            imageTrash,
            typeMask:0,
            classesList:[['100','200','300'],
                        ['200','200','300'],
                        ['300','200','303'],
                        ['400','200','300']],
            mask:{
                color:'#c0c0c0',
                name:'123',
                points:[1,2,3],
                type:'rect',
                classCode: '100',
                className: 'asddsa'
            }
        }
    },
}
</script>

<style scoped>
.maska{
    position:relative;
    height: 70px;
    padding: 0px;
    border: 1px solid #D9DBDE;
    overflow: hidden;
}

.colorImg{
    width: 20px;
    height: 70px;
    position:absolute; 
    top: 0px;
    left: 0px;
}

.deleteBtn{
    position:absolute; 
    bottom: 0px;
    right: 10px;
}

.check{
    position:absolute; 
    top: 5px;
    right: 30px;
}

.maskaViewCheck{
    position: absolute;
    /* top: 10px;
    right: 10px; */
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;

}

.checkbox{
    position:absolute;
    width: 1.5em;
    height: 1.5em;
    background-image: url(../images/show.svg);
    background-size: 24px;
    background-repeat: no-repeat;
}

.maskaViewCheck:checked + .checkbox{
    background-image: url(../images/hide.svg);
}


.contentMask{
    position:relative;
    margin-left: 24px;
}

.selectClass{
    background: #F6F8FA;
    border: 1px solid #D9DBDE;
    border-radius: 6px;
    width: 10vw;
}
</style>