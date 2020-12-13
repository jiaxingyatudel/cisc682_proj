<style>
</style>

<template>
    <div>
        <div class="content_container">
            <div class="content">
                <recipe-card
                    v-for="recipe_info in my_recipes_info"
                    v-bind:key="recipe_info.post_id"
                    v-bind:recipe_info="recipe_info"
                >
                <div><span class="card-link"><i class="fa fa-pencil" aria-hidden="true"></i>&nbsp;Edit</span></div>
                </recipe-card>
            </div>
        </div>
        <top-bar v-bind:top_bar_search="true"><span>My Recipes</span></top-bar>
    </div>
</template>

<script>
module.exports={
    data:function(){
        return{
            my_recipes_info:[]
        }
    },
    computed:{
        user_id:function(){
            return store.state.user_id;
        }
    },
    watch:{
        user_id:function(){
            this.get_my_recipes_info();
        }
    },
    components:{
        "top-bar":httpVueLoader("/web/top_bar.vue"),
        "recipe-card":httpVueLoader("/web/recipe_card.vue")
    },
    mounted:function(){
        this.get_my_recipes_info();
    },
    methods:{
        get_my_recipes_info:async function(){
            if(!this.user_id){
                return;
            }

            const response=await fetch("/get_my_recipes_info?user_id="+this.user_id,{
                method:"GET",
                credentials:"include"
            });
            if(response.ok){
                const resp=await response.json();
                if(!resp.err){
                    this.my_recipes_info=resp.my_recipes_info;
                }
            }
        }
    }
}
</script>