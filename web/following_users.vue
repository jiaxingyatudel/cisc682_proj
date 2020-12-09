<style>
</style>

<template>
    <div>
        <div class="content_container">
            <div class="content">
                <ul class="list-group">
                    <li class="list-group-item" v-for="following_user in following_users_info" v-bind:key="following_user.user_id">
                        <router-link v-bind:to="'/user_recipes/'+following_user.user_id" tag="div" style="float:left;cursor:pointer">
                            <div><i class="fa fa-user-circle" aria-hidden="true"></i>&nbsp;{{following_user.user_name}}</div>
                            <div><small>{{following_user.user_intro}}</small></div>
                        </router-link>
                        <button type="button" class="btn btn-outline-danger" style="float:right">
                            <span><i class="fa fa-user-times" aria-hidden="true"></i></span>
                        </button>
                    </li>
                </ul>
            </div>
        </div>
        <top-bar title="Following"></top-bar>
    </div>
</template>

<script>
module.exports={
    data:function(){
        return{
            following_users_info:[]
        }
    },
    computed:{
        user_id:function(){
            return store.state.user_id;
        }
    },
    watch:{
        user_id:function(){
            this.get_following_users();
        }
    },
    components:{
        "top-bar":httpVueLoader("/web/top_bar.vue")
    },
    mounted:function(){
        this.get_following_users();
    },
    methods:{
        get_following_users:async function(){
            if(!this.user_id){
                return;
            }

            const response=await fetch("/get_following_users?user_id="+this.user_id,{
                method:"GET",
                credentials:"include"
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    this.following_users_info=resp.following_users_info;
                }
            }
        }
    }
}
</script>