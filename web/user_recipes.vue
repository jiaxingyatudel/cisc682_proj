<style>
</style>

<template>
    <div>
        <div class="content_container">
            <div class="content">
                <recipe-card
                    v-for="recipe_info in user_recipes_info"
                    v-bind:key="recipe_info.post_id"
                    v-bind:recipe_info="recipe_info"
                >
                <div v-if="((my_user_id)&&(recipe_info.user_id!=my_user_id))">
                    <recipe-like-btn v-bind:recipe_info="recipe_info" v-bind:user_id="my_user_id"></recipe-like-btn>
                </div>
                </recipe-card>
            </div>
        </div>
        <top-bar v-bind:top_bar_search="true">
            <span>{{(user_name)?(user_name+'\'s Recipes'):('')}}</span>
            <span v-if="((user_following_checked)&&(!user_following))" class="badge badge-dark" style="cursor:pointer" v-on:click="click_follow_user()"><i class="fa fa-user-plus" aria-hidden="true"></i>&nbsp;Follow</span>
            <span v-if="((user_following_checked)&&(user_following))" class="badge badge-dark" style="cursor:pointer" v-on:click="click_cancel_follow_user()"><i class="fa fa-users" aria-hidden="true"></i>&nbsp;Following</span>
        </top-bar>
    </div>
</template>

<script>
module.exports={
    props:["user_id"],
    data:function(){
        return{
            user_name:false,
            user_following:false,
            user_following_checked:false,
            user_recipes_info:[]
        }
    },
    computed:{
        my_user_id:function(){
            return store.state.user_id;
        }
    },
    components:{
        "top-bar":httpVueLoader("/web/top_bar.vue"),
        "recipe-card":httpVueLoader("/web/recipe_card.vue"),
        "recipe-like-btn":httpVueLoader("/web/recipe_like_btn.vue")
    },
    mounted:async function(){
        this.get_user_name();
        this.check_user_following();
        this.get_user_recipes_info();
    },
    methods:{
        get_user_name:async function(){
            if(!this.user_id){
                return false;
            }

            const params=new URLSearchParams({
                "user_id":this.user_id
            });
            const response=await fetch("/get_user_name_by_user_id?"+params.toString(),{
                method:"GET"
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    this.user_name=resp.user_name;
                }
            }
        },
        check_user_following:async function(){
            if(!this.my_user_id){
                return false;
            }

            const params=new URLSearchParams({
                "user_id":this.user_id,
                "my_user_id":this.my_user_id
            });
            const response=await fetch("/check_user_following?"+params.toString(),{
                method:"GET"
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    this.user_following_checked=true;
                    this.user_following=resp.user_following;
                }
            }
        },
        get_user_recipes_info:async function(){
            const params=new URLSearchParams({
                "user_id":this.user_id,
                "my_user_id":this.my_user_id
            });
            const response=await fetch("/get_user_recipes_info?"+params.toString(),{
                method:"GET",
                credentials:"include"
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    this.user_recipes_info=resp.user_recipes_info;
                }
            }
        },
        click_follow_user:async function(){
            if(!this.my_user_id){
                return false;
            }

            const response=await fetch("/follow_user",{
                method:"POST",
                credentials:"include",
                body:JSON.stringify({
                    "user_id":this.user_id,
                    "my_user_id":this.my_user_id
                })
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    this.user_following=true;
                }else{
                    alert("System error")
                }
            }
        },
        click_cancel_follow_user:async function(post_id){
            let b=confirm("Are you sure to cancel follwoing user "+this.user_name+"?");
            if(!b){
                return;
            }
    
            if(!this.my_user_id){
                return false;
            }

            const response=await fetch("/cancel_follow_user",{
                method:"POST",
                credentials:"include",
                body:JSON.stringify({
                    "user_id":this.user_id,
                    "my_user_id":this.my_user_id
                })
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    this.user_following=false;
                }else{
                    alert("System error")
                }
            }
        }
    }
}
</script>