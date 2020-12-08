<style>
#user_btn_container{
    position: absolute;
    top: 10px;
    left: 10px;
}

#user_btn{
    height: 40px;
    max-width: 160px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis
}

@media screen and (max-width: 1060px){
    #user_btn_user_name{
        display: none;
    }
}

.user_login_register_nav{
    margin-bottom: 10px;
}

.user_login_register_nav .nav-item{
    cursor: pointer;
}

.user_register_input_group,
.user_login_input_group,
.user_info_input_group,
.password_input_group{
    margin-bottom: 10px;
}

.user_register_input_group_prepend>span,
.user_login_input_group_prepend>span,
.user_info_input_group_prepend>span,
.password_input_group_prepend>span{
    width: 140px;
}
</style>

<template>
    <div>
        <div id="user_btn_container">
            <div v-if="!user_info_get">
                <button type="button" class="btn btn-light" v-on:click="click_register_btn">Register</button>
                <button type="button" class="btn btn-dark" v-on:click="click_login_btn">Login</button>
            </div>
            <div v-if="user_info_get">
                <button type="button" id="user_btn" class="btn btn-dark" v-on:click="click_user_btn">
                    <span><i class="fa fa-user-circle" aria-hidden="true"></i></span><span id="user_btn_user_name">&nbsp;{{user_name}}</span>
                </button>
            </div>
        </div>
        <div class="modal" data-backdrop="static" data-keyboard="false" id="user_modal">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <div v-if="!user_info_get">
                            <div class="container">
                                <ul class="nav nav-tabs user_login_register_nav">
                                    <li class="nav-item">
                                        <a class="nav-link" v-bind:class="(user_login_register_toogle)?('active'):('')" v-on:click="click_user_login_register_toogle(true)">Login</a>
                                    </li>
                                    <li class="nav-item">
                                        <a class="nav-link" v-bind:class="(!user_login_register_toogle)?('active'):('')" v-on:click="click_user_login_register_toogle(false)">Register</a>
                                    </li>
                                </ul>
                            </div>
                            <div class="container" v-if="!user_login_register_toogle">
                                <div class="input-group user_register_input_group">
                                    <div class="input-group-prepend user_register_input_group_prepend">
                                        <span class="input-group-text">User Name</span>
                                    </div>
                                <input type="text" class="form-control" v-model="register_user_name">
                                </div>
                                <div class="input-group user_register_input_group">
                                    <div class="input-group-prepend user_register_input_group_prepend">
                                        <span class="input-group-text">User Email</span>
                                    </div>
                                    <input type="text" class="form-control" v-model="register_user_email">
                                </div>
                                <label for="basic-url">Password needs to be longer than 8 digits</label>
                                <password-input-group title="Password" v-model="register_user_password"></password-input-group>
                                <button type="button" class="btn btn-outline-secondary" v-on:click="click_user_register()">Register</button>
                            </div>
                            <div class="container" v-if="user_login_register_toogle">
                                <div class="input-group user_login_input_group">
                                    <div class="input-group-prepend user_login_input_group_prepend">
                                    <span class="input-group-text">User Email</span>
                                </div>
                                <input type="text" class="form-control" v-model="login_user_email">
                                </div>
                                <password-input-group title="Password" v-model="login_user_password"></password-input-group>
                                <button type="button" class="btn btn-outline-secondary" v-on:click="click_user_login()">Login</button>
                            </div>
                        </div>
                        <div v-if="user_info_get">
                            <user-info-input-group title="Name" v-bind:old_value="user_name" v-model="user_info_input_user_name" v-on:confirm="click_user_info_user_name_confirm()"></user-info-input-group>
                            <user-info-input-group title="Name" v-bind:old_value="user_email" v-model="user_info_input_user_email" v-on:confirm="click_user_info_user_email_confirm()"></user-info-input-group>
                            <hr>
                            <div v-if="!change_password_toggle" class="btn-group">
                                <button type="button" class="btn btn-outline-secondary" v-on:click="click_change_password_toggle()">Change password</button>
                            </div>
                            <div v-if="change_password_toggle">
                                <password-input-group title="Old password" v-model="change_password_old_password"></password-input-group>
                                <password-input-group title="New password" v-model="change_password_new_password"></password-input-group>
                                <div class="btn-group">
                                    <button type="button" class="btn btn-outline-secondary" v-on:click="click_change_password_toggle()">Cancel</button>
                                    <button type="button" class="btn btn-dark" v-on:click="click_change_password_confirm()">Confirm</button>
                                </div>
                            </div>
                            <hr>
                            <div class="btn-group">
                                <button type="button" class="btn btn-outline-danger" v-on:click="click_user_logout()">Logout</button>
                                <button type="button" class="btn btn-outline-danger" v-on:click="click_user_logout_all()">Logout from all clients</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
module.exports={
    data:function(){
        return {
            user_name:"",
            user_email:"",
            user_info_get:false,
            user_login_register_toogle:false,
            register_user_name:"",
            register_user_email:"",
            register_user_password:"",
            login_user_email:"",
            login_user_password:"",
            user_info_input_user_name:"",
            user_info_input_user_email:"",
            change_password_toggle:false,
            change_password_old_password:"",
            change_password_new_password:""
        }
    },
    computed:{
        user_id:function(){
            return store.state.user_id
        }
    },
    watch:{
        user_id:function(){
            this.get_user_info_all();
        }
    },
    components:{
        "user-info-input-group":httpVueLoader("/web/user_info_input_group.vue"),
        "password-input-group":httpVueLoader("/web/password_input_group.vue"),
    },
    mounted:function(){
        this.get_user_info_all();
    },
    methods:{
        get_user_info_all:async function(){
            if(!this.user_id){
                return false;
            }

            const response=await fetch("/get_user_info_all?user_id="+this.user_id,{
                method:"GET",
                credentials:"include"
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    this.user_name=resp.user_name;
                    this.user_email=resp.user_email;
                    this.register_user_name="";
                    this.register_user_email="";
                    this.register_user_password="";
                    this.login_user_email="";
                    this.login_user_password="";
                    this.user_info_get=true;
                }
                if(resp.err==1){
                }
            }
        },
        click_register_btn:function(){
            this.user_login_register_toogle=false;
            $("#user_modal").modal("show");
        },
        click_login_btn:function(){
            this.user_login_register_toogle=true;
            $("#user_modal").modal("show");
        },
        click_user_btn:function(){
            $("#user_modal").modal("show");
        },
        click_user_register:async function(){
            if(this.register_user_name.length<=0){
                alert("Not valid user name")
                return;
            }
            if(!(/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(this.register_user_email))){
                alert("Not valid email format")
                return;
            }
            if(this.register_user_password.length<=8){
                alert("Password needs to be longer than 8 digits")
                return;
            }

            const response=await fetch("/user_register",{
                method:"POST",
                body:JSON.stringify({
                    user_name:this.register_user_name,
                    user_email:this.register_user_email,
                    user_password:this.register_user_password
                })
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    store.commit("user_check",resp.user_id);
                    this.register_user_name="";
                    this.register_user_email="";
                    this.register_user_password="";
                    this.login_user_email="";
                    this.login_user_password="";
                    $("#user_modal").modal("hide");
                }
                if(resp.err==1){
                    alert("Email already registered");
                }
            }
        },
        click_user_login:async function(){
            const response=await fetch("/user_login",{
                method:"POST",
                body:JSON.stringify({
                    user_email:this.login_user_email,
                    user_password:this.login_user_password
                })
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    store.commit("user_check",resp.user_id);
                    this.register_user_name="";
                    this.register_user_email="";
                    this.register_user_password="";
                    this.login_user_email="";
                    this.login_user_password="";
                    $("#user_modal").modal("hide");
                }
                if(resp.err==1){
                    alert("Email and password not match");
                }
            }
        },
        click_user_logout:async function(){
            const response=await fetch("/user_logout",{
                method:"POST",
                credentials:"include"
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    store.commit("user_check",false);
                    this.user_name=false;
                    this.user_email=false;
                    this.register_user_name="";
                    this.register_user_email="";
                    this.register_user_password="";
                    this.login_user_email="";
                    this.login_user_password="";
                    window.location.reload();
                }
            }
        },
        click_user_logout_all:async function(){
            const response=await fetch("/user_logout_all",{
                method:"POST",
                credentials:"include",
                body:JSON.stringify({
                    user_id:this.user_id,
                })
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    store.commit("user_check",false);
                    this.user_name=false;
                    this.user_email=false;
                    this.register_user_name="";
                    this.register_user_email="";
                    this.register_user_password="";
                    this.login_user_email="";
                    this.login_user_password="";
                    window.location.reload();
                }
            }
        },
        click_user_login_register_toogle:function(b){
            this.user_login_register_toogle=b;
        },
        click_user_info_user_name_confirm:async function(){
            let b=confirm("Are you sure to change your name to "+this.user_info_input_user_name+"?");
            if(!b){
                return;
            }
            const response=await fetch("/user_change_user_name",{
                method:"POST",
                credentials:"include",
                body:JSON.stringify({
                    user_id:this.user_id,
                    user_name:this.user_info_input_user_name
                })
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    this.user_name=resp.user_name;
                }
                if(resp.err==1){
                    alert("System error");
                }
            }
        },
        click_user_info_user_email_confirm:async function(){
            let b=confirm("Are you sure to change your email to "+this.user_info_input_user_email+"?");
            if(!b){
                return;
            }
            const response=await fetch("/user_change_user_email",{
                method:"POST",
                credentials:"include",
                body:JSON.stringify({
                    user_id:this.user_id,
                    user_email:this.user_info_input_user_email
                })
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    this.user_email=resp.user_email;
                }
                if(resp.err==1){
                    alert("System error");
                }
                if(resp.err==2){
                    alert("Email already registered");
                }
            }
        },
        click_change_password_toggle:function(){
            this.change_password_toggle=!(this.change_password_toggle);
            this.change_password_old_password="";
            this.change_password_new_password="";
        },
        click_change_password_confirm:async function(){
            let b=confirm("Are you sure to change your password?");
            if(!b){
                return;
            }
            const response=await fetch("/user_change_password",{
                method:"POST",
                credentials:"include",
                body:JSON.stringify({
                    user_id:this.user_id,
                    user_email:this.user_email,
                    user_old_password:this.change_password_old_password,
                    user_new_password:this.change_password_new_password
                })
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    alert("Password changed")
                    this.change_password_toggle=false;
                    this.change_password_old_password="";
                    this.change_password_new_password="";
                }
                if(resp.err==1){
                    alert("System error");
                }
                if(resp.err==2){
                    alert("Old password not match");
                }
            }
        }
    }
}
</script>