<template>
    <div class="modal-backdrop">
      <div class="modal">
        <header class="modal-header">
          <slot name="header">
            Create a new project
          </slot>
          <button
            type="button"
            class="btn-close"
            @click="close"
          >
            x
          </button>
        </header>
  
        <section class="modal-body">
                <p>
                    Name
                    <input 
                        class="inputName" 
                        type="text" 
                        name="projectName" 
                        :value=nameProject 
                        @input="nameProject=$event.target.value"
                    >
                </p>

                <p>
                    Creator
                    <input 
                        class="inputName" 
                        type="text" 
                        name="creator" 
                        :value=creator 
                        @input="creator=$event.target.value"
                    >
                </p>

                <p>
                    Status
                    <input 
                        class="inputName" 
                        type="text" 
                        name="status" 
                        :value=status 
                        @input="status=$event.target.value"
                    >
                </p>

                <p class="description">
                    Description
                    <textarea 
                        class="inputDescription" 
                        name="description" 
                        :value=description 
                        @input="description=$event.target.value"
                    ></textarea>
                </p>

                <p>
                    Load file
                    <input 
                        class="inputFile" 
                        type="file"
                        multiple
                        name="files" 
                        @change="previewFiles($event)"
                    >
                </p>

                <p><button @click="send">send</button></p>
         </section>
  
        <footer class="modal-footer">
          <button
            type="button"
            class="btn-green"
            @click="close"
          >
            Close Modal
          </button>
        </footer>
      </div>
    </div>
  </template>

<script>
import axios from 'axios';

export default {
  name: 'CreateProjectDialog',
  data(){
        return{
            nameProject:'',
            creator:'I am',
            status:'OK',
            description:'',
            inputFiles:[],
        }
    },
  methods: {
    close(){
        this.$emit('close')
    },
    previewFiles(event){
        this.inputFiles = event.target.files
    },
    send(){
        const config = { headers: { 'Content-Type': 'multipart/form-data' } };
        let url = '/projects/create'
        const formData = new FormData()

        for( var i = 0; i < this.inputFiles.length; i++ ){
            let file = this.inputFiles[i];

            formData.append('files', file);
        }

        formData.append('project_name', this.nameProject)
        formData.append('status', this.status)
        formData.append('creator', this.creator)
        formData.append('description', this.description)
        axios.post(url, formData, config).then((response)=>{
          this.close()
          this.$emit('addProject', response.data)
        })
    }   
  },
};
</script>

<style>
  .modal-backdrop {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.3);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .modal {
    min-width: 500px;
    min-height: 500px;
    background: #FFFFFF;
    box-shadow: 2px 2px 20px 1px;
    overflow-x: auto;
    display: flex;
    flex-direction: column;
  }

  .modal-header,
  .modal-footer {
    padding: 15px;
    display: flex;
  }

  .modal-header {
    position: relative;
    border-bottom: 1px solid #eeeeee;
    color: #4AAE9B;
    justify-content: space-between;
  }

  .modal-footer {
    border-top: 1px solid #eeeeee;
    flex-direction: column;
    justify-content: flex-end;
  }

  .modal-body {
    position: relative;
    padding: 20px 10px;
  }

  .btn-close {
    position: absolute;
    top: 0;
    right: 0;
    border: none;
    font-size: 20px;
    padding: 10px;
    cursor: pointer;
    font-weight: bold;
    color: #4AAE9B;
    background: transparent;
  }

  .btn-green {
    color: white;
    background: #4AAE9B;
    border: 1px solid #4AAE9B;
    border-radius: 2px;
  }
</style>