<template>
    <div class="app">
        <NavBar class="navbar"></NavBar>
        <router-view></router-view>
    </div>
</template>

<script>
import NavBar from "@/components/NavBar";

export default{
    components:{
        NavBar
    },
    data(){
        return {
        }
    },
    methods: {
    }
}
</script>

<style>
*{  
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.app{  
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: 0.1fr 1.9fr;
  gap: 0px 0px;
  grid-auto-flow: row;
  grid-template-areas:
    "Header"
    "Workarea";
  height: 100vh;
}

.navbar{
    grid-area: Header;
}

.workarea {
    grid-area: Workarea;
}
</style>