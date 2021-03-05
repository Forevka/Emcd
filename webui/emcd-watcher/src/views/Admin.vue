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

    <!-- Scroll to Top Button
    <a class="scroll-to-top rounded" href="#page-top">
        <i class="fas fa-angle-up"></i>
    </a>-->

    <!-- Logout Modal-->
    <div class="modal fade" id="logoutModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
        aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Ready to Leave?</h5>
                    <button class="close" type="button" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">×</span>
                    </button>
                </div>
                <div class="modal-body">Select "Logout" below if you are ready to end your current session.</div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" type="button" data-dismiss="modal">Cancel</button>
                    <router-link class="btn btn-primary" to="/">Logout</router-link>
                </div>
            </div>
        </div>
    </div>
</template>


<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { TelegramAuthModel } from '@/models/TelegramAuthModel';
import {ActionTypes as UserActions} from "@/store/user/actions"
import Sidebar from '@/components/Sidebar.vue';

@Options({
  components: {
      Sidebar
  }
})
export default class Admin extends Vue {

    mounted() {
        this.$store.dispatch(UserActions.UPDATE_USER)

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

        // Scroll to top button appear
        // @ts-ignore
        window.$(document).on('scroll', function() {
            // @ts-ignore
            const scrollDistance = window.$(this).scrollTop();
            // @ts-ignore
            if (scrollDistance > 100) {
                // @ts-ignore
            window.$('.scroll-to-top').fadeIn();
            // @ts-ignore
            } else {
            // @ts-ignore
            window.$('.scroll-to-top').fadeOut();
            }
        });

        // Smooth scrolling using jQuery easing
        // @ts-ignore
        window.$(document).on('click', 'a.scroll-to-top', function(e) {
            // @ts-ignore
            const $anchor = window.$(this);
            // @ts-ignore
            window.$('html, body').stop().animate({
            // @ts-ignore
            scrollTop: (window.$($anchor.attr('href')).offset().top)
            }, 1000, 'easeInOutExpo');
            // @ts-ignore
            e.preventDefault();
        });
    }


    get user(){
        return this.$store.getters.getUser
    }
}
</script>