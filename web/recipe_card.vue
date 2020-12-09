<style>
.recipe_card{
    margin-bottom: 10px;
}

.recipe_card_img{
    height: 200px;
    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;
}

.recipe_card .card-link{
    cursor: pointer;
    color: orangered;
}

.recipe_author{
    cursor: pointer;
}
</style>

<template>
    <div class="card recipe_card">
        <div v-if="recipe_info.post_title_img" v-bind:style="{'background-image':'url('+recipe_info.post_title_img+')'}" class="card-img-top recipe_card_img"></div>
        <div class="card-body">
            <h5 class="card-title">{{recipe_info.post_title}}</h5>
            <router-link tag="h6" v-bind:to="'/user_recipes/'+recipe_info.user_id" class="card-subtitle mb-2 text-muted recipe_author"><i class="fa fa-user-circle" aria-hidden="true"></i>&nbsp;{{recipe_info.user_name}}</router-link>
            <p class="card-text">{{recipe_info.post_text}}</p>
            <p><span class="badge badge-dark">{{print_date_time()}}</span></p>
            <slot></slot>
        </div>
    </div>
</template>

<script>

module.exports={
    props:["recipe_info"],
    methods:{
        print_date_time:function(){
            date=new Date(this.recipe_info.post_time);
            return date.toLocaleDateString("en-US")+" "+date.toLocaleTimeString("en-US",{timeStyle:"short"});
        }
    }
}
</script>