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
        <top-bar v-bind:title="(user_name)?(user_name+'\'s Recipes'):('')" v-bind:top_bar_search="true"></top-bar>
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
        "recipe-card":httpVueLoader("/web/recipe_card.vue"),
        "recipe-like-btn":httpVueLoader("/web/recipe_like_btn.vue")
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
        }
    }
}
</script>