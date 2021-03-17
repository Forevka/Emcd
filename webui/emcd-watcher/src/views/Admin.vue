<template>
    
    <!-- Page Wrapper -->
    <div id="wrapper">

        <sidebar/>

        <!-- Content Wrapper -->
        <div id="content-wrapper" class="d-flex flex-column">

            <!-- Main Content -->
            <div id="content">

                <!-- Topbar -->
                <nav class="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow">

                    <!-- Sidebar Toggle (Topbar) -->
                    <button id="sidebarToggleTop" class="btn btn-link d-md-none rounded-circle mr-3">
                        <i class="fa fa-bars"></i>
                    </button>

                    <!-- Topbar Search 
                    <form
                        class="d-none d-sm-inline-block form-inline mr-auto ml-md-3 my-2 my-md-0 mw-100 navbar-search">
                        <div class="input-group">
                            <input type="text" class="form-control bg-light border-0 small" placeholder="Search for..."
                                aria-label="Search" aria-describedby="basic-addon2">
                            <div class="input-group-append">
                                <button class="btn btn-primary" type="button">
                                    <i class="fas fa-search fa-sm"></i>
                                </button>
                            </div>
                        </div>
                    </form>
                    -->

                    <!-- Topbar Navbar -->
                    <ul class="navbar-nav ml-auto">

                        <!-- Nav Item - Search Dropdown (Visible Only XS) -->
                        <li class="nav-item dropdown no-arrow d-sm-none">
                            <a class="nav-link dropdown-toggle" href="#" id="searchDropdown" role="button"
                                data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                <i class="fas fa-search fa-fw"></i>
                            </a>
                            <!-- Dropdown - Messages -->
                            <div class="dropdown-menu dropdown-menu-right p-3 shadow animated--grow-in"
                                aria-labelledby="searchDropdown">
                                <form class="form-inline mr-auto w-100 navbar-search">
                                    <div class="input-group">
                                        <input type="text" class="form-control bg-light border-0 small"
                                            placeholder="Search for..." aria-label="Search"
                                            aria-describedby="basic-addon2">
                                        <div class="input-group-append">
                                            <button class="btn btn-primary" type="button">
                                                <i class="fas fa-search fa-sm"></i>
                                            </button>
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </li>

                        <!-- Nav Item - User Information -->
                        <li class="nav-item dropdown no-arrow" v-if="user != null">
                            <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button"
                                data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                <span class="mr-2 d-none d-lg-inline text-gray-600 small">{{user.first_name}}</span>
                                <img class="img-profile rounded-circle"
                                    :src="user.photo_url">
                            </a>
                            <!-- Dropdown - User Information -->
                            <div class="dropdown-menu dropdown-menu-right shadow animated--grow-in"
                                aria-labelledby="userDropdown">
                                <a class="dropdown-item" href="#" data-toggle="modal" data-target="#logoutModal">
                                    <i class="fas fa-sign-out-alt fa-sm fa-fw mr-2 text-gray-400"></i>
                                    Logout
                                </a>
                            </div>
                        </li>

                    </ul>

                </nav>
                <!-- End of Topbar -->

                <!-- Begin Page Content -->
                <div class="container-fluid">

                    <router-view>
                        
                    </router-view>

                </div>
                <!-- /.container-fluid -->

            </div>
            <!-- End of Main Content -->

        </div>
        <!-- End of Content Wrapper -->

    </div>
    <!-- End of Page Wrapper -->

    <EditModal/>
    <LogoutModal/>
    <EditBroadcastTextModal/>
    
    <Loader/>
</template>


<script lang="ts">
import { Options, Vue } from "vue-class-component";
import {ActionTypes as UserActions} from "@/store/user/actions"
import Sidebar from '@/components/Sidebar.vue';
import EditModal from '@/components/EditModal.vue';
import EditBroadcastTextModal from '@/components/EditBroadcastTextModal.vue';
import LogoutModal from '@/components/LogoutModal.vue';
import Loader from "@/components/Loader.vue"
import {hideLoader, showLoader} from '@/utils/loader';

@Options({
  components: {
    Sidebar,
    EditModal,
    Loader,
    LogoutModal,
    EditBroadcastTextModal,
  }
})
export default class Admin extends Vue {

    async created() {
        showLoader()
        await this.$store.dispatch(UserActions.UPDATE_USER).then(() => {
            this.$store.dispatch(UserActions.UPDATE_LANGS)
            hideLoader()
        })
    }

    async mounted() {
        // Close any open menu accordions when window is resized below 768px
        // @ts-ignore
        window.$(window).resize(function() {
            // @ts-ignore
            if (window.$(window).width() < 768) {
            // @ts-ignore
            window.$('.sidebar .collapse').collapse('hide');
            }
            
            // Toggle the side navigation when window is resized below 480px
            // @ts-ignore
            if (window.$(window).width() < 480 && !window.$(".sidebar").hasClass("toggled")) {
                // @ts-ignore
            window.$("body").addClass("sidebar-toggled");
            // @ts-ignore
            window.$(".sidebar").addClass("toggled");
            // @ts-ignore
            window.$('.sidebar .collapse').collapse('hide');
            }
        });

        // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
        // @ts-ignore
        window.$('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function(e) {
            // @ts-ignore
            if (window.$(window).width() > 768) {
            // @ts-ignore
            const e0 = e.originalEvent,
                delta = e0.wheelDelta || -e0.detail;
            // @ts-ignore
            this.scrollTop += (delta < 0 ? 1 : -1) * 30;
            e.preventDefault();
            }
        });
    }


    get user(){
        return this.$store.getters.getUser
    }
}
</script>

<style lang="scss" scoped>
.container-fluid {
    overflow-y: scroll;
    max-height: calc(100vh - 4.375rem - 1.5rem);
    overflow-x: hidden;
}

</style>