<template>
    <!-- Sidebar -->
        <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">

            <!-- Sidebar - Brand -->
            <router-link class="sidebar-brand d-flex align-items-center justify-content-center" to="/admin">
                <div class="sidebar-brand-icon">
                    <svg width="30" height="31" viewBox="0 0 30 31" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M0 9.02162C0 5.68411 2.70559 2.97852 6.0431 2.97852H30.2155C30.2155 6.31603 27.5099 9.02162 24.1724 9.02162H0ZM0 30.7768H24.1724C27.5099 30.7768 30.2155 28.0712 30.2155 24.7337H6.0431C2.70559 24.7337 0 27.4393 0 30.7768ZM0 19.8992C0 16.5617 2.68693 13.8561 6.00143 13.8561H15.0036C15.0036 17.1936 12.3166 19.8992 9.00214 19.8992H0Z" fill="url(#paint0_linear)"/>
                        <defs>
                            <linearGradient id="paint0_linear" x1="33.5907" y1="46.6685" x2="9.29574" y2="-11.6248" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#A048E0"/>
                                <stop offset="1" stop-color="#E08148"/>
                            </linearGradient>
                        </defs>
                    </svg>
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
                        <router-link class="collapse-item" to="/admin/broadcast">Broadcasts</router-link>
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