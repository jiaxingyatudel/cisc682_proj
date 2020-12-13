<style>
</style>

<template>
    <div>
        <div class="content_container">
            <div class="content">
                <recipe-card
                    v-for="recipe_info in liked_recipes_info"
                    v-bind:key="recipe_info.post_id"
                    v-bind:recipe_info="recipe_info"
                >
                <div v-if="recipe_info.user_id!=user_id">
                    <recipe-like-btn v-bind:recipe_info="recipe_info" v-bind:user_id="user_id"></recipe-like-btn>
                </div>
                </recipe-card>
            </div>
        </div>
        <top-bar v-bind:top_bar_search="true"><span>Liked Recipes</span></top-bar>
    </div>
</template>

<script>
module.exports={
    data:function(){
        return{
            user_name:false,
            liked_recipes_info:[]
        }
    },
    computed:{
        user_id:function(){
            return store.state.user_id;
        }
    },
    components:{
        "top-bar":httpVueLoader("/web/top_bar.vue"),
        "recipe-card":httpVueLoader("/web/recipe_card.vue"),
        "recipe-like-btn":httpVueLoader("/web/recipe_like_btn.vue")
    },
    mounted:function(){
        this.get_liked_recipes_info();
    },
    methods:{
        get_liked_recipes_info:async function(){
            if(!this.user_id){
                return;
            }

            const params=new URLSearchParams({
                "user_id":this.user_id
            });
            const response=await fetch("/get_liked_recipes_info?"+params.toString(),{
                method:"GET",
                credentials:"include"
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    this.liked_recipes_info=resp.liked_recipes_info;
                }
            }
        }
    }
}
</script>