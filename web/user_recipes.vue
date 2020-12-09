<style>
</style>

<template>
    <div>
        <div class="content_container">
            <div class="content">
                <recipe-card
                    v-for="recipe_info in user_recipes_info"
                    v-bind:key="recipe_info.post_id"
                    v-bind:post_id="recipe_info.post_id"
                    v-bind:user_name="recipe_info.user_name"
                    v-bind:post_title="recipe_info.post_title"
                    v-bind:post_text="recipe_info.post_text"
                    v-bind:post_time="recipe_info.post_time"
                    v-bind:post_img="recipe_info.post_img"
                >
                <div>
                    <span v-if="!recipe_info.post_like" class="card-link" v-on:click="click_like_post(recipe_info.post_id)"><i class="fa fa-heart-o" aria-hidden="true"></i>&nbsp;Like this recipe to save for later</span>
                    <span v-if="recipe_info.post_like" class="card-link" v-on:click="click_cancel_like_post(recipe_info.post_id)"><i class="fa fa-heart" aria-hidden="true"></i>&nbsp;Cacel like</span>
                </div>
                </recipe-card>
            </div>
        </div>
        <top-bar v-bind:title="(user_name)?(user_name+'\'s Recipes'):('')"></top-bar>
    </div>
</template>

<script>
module.exports={
    props:["user_id"],
    data:function(){
        return{
            user_name:false,
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
        "recipe-card":httpVueLoader("/web/recipe_card.vue")
    },
    mounted:function(){
        this.get_user_name();
        this.get_user_recipes_info();
    },
    methods:{
        get_user_name:async function(){
            if(!this.user_id){
                return false;
            }

            const response=await fetch("/get_user_name_by_user_id?user_id="+this.user_id,{
                method:"GET"
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    this.user_name=resp.user_name;
                }
            }
        },
        get_user_recipes_info:async function(){
            if((!this.user_id)||(!this.my_user_id)){
                return;
            }

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
        click_like_post:async function(post_id){
            if(!this.my_user_id){
                return;
            }

            const response=await fetch("/like_post",{
                method:"POST",
                credentials:"include",
                body:JSON.stringify({
                    post_id:post_id,
                    user_id:this.my_user_id
                })
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    for(let i=0;i<this.user_recipes_info.length;i++){
                        recipe_info=this.user_recipes_info[i];
                        if(recipe_info.post_id==post_id){
                            recipe_info.post_like=true;
                            break;
                        }
                    }
                }else{
                    alert("System error")
                }
            }
        },
        click_cancel_like_post:async function(post_id){
            if(!this.my_user_id){
                return;
            }

            const response=await fetch("/cancel_like_post",{
                method:"POST",
                credentials:"include",
                body:JSON.stringify({
                    post_id:post_id,
                    user_id:this.my_user_id
                })
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    for(let i=0;i<this.user_recipes_info.length;i++){
                        recipe_info=this.user_recipes_info[i];
                        if(recipe_info.post_id==post_id){
                            recipe_info.post_like=false;
                            break;
                        }
                    }
                }else{
                    alert("System error")
                }
            }
        },
    }
}
</script>