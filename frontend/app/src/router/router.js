import ProjectsTab from "@/views/ProjectsTab";
import TasksTab from "@/views/TasksTab";
import ViewTab from "@/views/ViewTab";
import InspectTab from "@/views/InspectTab";
import EditTab from "@/views/EditTab";

import {createRouter, createWebHistory} from "vue-router"

const routes = [
    {
        path: '/projects',
        component: ProjectsTab
    },
    {
        path: '/',
        component: ProjectsTab
    },
    {
        path: '/tasks/:projectName',
        component: TasksTab
    },
    {
        path: '/view',
        component: ViewTab
    },
    {
        path: '/edit/:projectName/:id',
        component: EditTab
    },
    {
        path: '/inspect',
        component: InspectTab
    }
]

const router = createRouter({
    routes,
    history: createWebHistory(process.env.BASE_URL)
})

export default router