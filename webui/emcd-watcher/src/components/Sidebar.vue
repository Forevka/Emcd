<template>
    <!-- Sidebar -->
        <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">

            <!-- Sidebar - Brand -->
            <router-link class="sidebar-brand d-flex align-items-center justify-content-center" to="/admin">
                <div class="sidebar-brand-icon rotate-n-15">
                    <i class="fas fa-laugh-wink"></i>
                </div>
                <div class="sidebar-brand-text mx-3">EMCD Admin</div>
            </router-link>

            <!-- Divider -->
            <hr class="sidebar-divider my-0">

            <!-- Nav Item - Dashboard -->
            <li class="nav-item">
                <router-link class="nav-link" to="/admin">
                    <i class="fas fa-fw fa-tachometer-alt"></i>
                    <span>Dashboard</span></router-link>
            </li>

            <!-- Divider -->
            <hr class="sidebar-divider">

            <!-- Heading -->
            <div class="sidebar-heading">
                Tools
            </div>

            <!-- Nav Item - Utilities Collapse Menu -->
            <li class="nav-item">
                <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapseUtilities"
                    aria-expanded="true" aria-controls="collapseUtilities">
                    <i class="fas fa-fw fa-wrench"></i>
                    <span>Utilities</span>
                </a>
                <div id="collapseUtilities" class="collapse" aria-labelledby="headingUtilities"
                    data-parent="#accordionSidebar">
                    <div class="bg-white py-2 collapse-inner rounded">
                        <h6 class="collapse-header">Custom Utilities:</h6>
                        <router-link class="collapse-item" to="/admin/faq">FAQ editing</router-link>
                    </div>
                </div>
            </li>
            <!-- Sidebar Toggler (Sidebar) -->
            <div class="text-center d-none d-md-inline">
                <button class="rounded-circle border-0" id="sidebarToggle"></button>
            </div>

        </ul>
        <!-- End of Sidebar -->
</template>


<script lang="ts">
import { Options, Vue } from "vue-class-component";

@Options({
  components: {
  }
})
export default class Sidebar extends Vue {
    mounted() {
        // @ts-ignore
        window.$("#sidebarToggle, #sidebarToggleTop").on('click', function() {
            // @ts-ignore
            window.$("body").toggleClass("sidebar-toggled");
            // @ts-ignore
            window.$(".sidebar").toggleClass("toggled");
            // @ts-ignore
            if (window.$(".sidebar").hasClass("toggled")) {
                // @ts-ignore
                window.$('.sidebar .collapse').collapse('hide');
            }
        });
    }
}
</script>