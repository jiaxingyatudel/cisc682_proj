<style>
</style>

<template>
    <span>
        <span v-if="!recipe_info.post_like" class="card-link" v-on:click="click_like_post()"><i class="fa fa-heart-o" aria-hidden="true"></i>&nbsp;Like this recipe to save for later</span>
        <span v-if="recipe_info.post_like" class="card-link" v-on:click="click_cancel_like_post()"><i class="fa fa-heart" aria-hidden="true"></i>&nbsp;Cancel like</span>
    </span>
</template>

<script>
module.exports={
    props:["recipe_info","user_id"],
    methods:{
        click_like_post:async function(){
            if(!this.user_id){
                return false;
            }

            const response=await fetch("/like_post",{
                method:"POST",
                credentials:"include",
                body:JSON.stringify({
                    post_id:this.recipe_info.post_id,
                    user_id:this.user_id
                })
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    this.recipe_info.post_like=true;
                }else{
                    alert("System error")
                }
            }
        },
        click_cancel_like_post:async function(post_id){
            if(!this.user_id){
                return false;
            }

            const response=await fetch("/cancel_like_post",{
                method:"POST",
                credentials:"include",
                body:JSON.stringify({
                    post_id:this.recipe_info.post_id,
                    user_id:this.user_id
                })
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    this.recipe_info.post_like=false;
                }else{
                    alert("System error")
                }
            }
        }
    }
}
</script>