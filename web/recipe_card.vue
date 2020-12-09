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
</style>

<template>
    <div class="card recipe_card">
        <div v-bind:style="{'background-image':'url('+random_place_holder_img()+')'}" class="card-img-top recipe_card_img"></div>
        <div class="card-body">
            <h5 class="card-title">{{post_title}}</h5>
            <h6 class="card-subtitle mb-2 text-muted"><i class="fa fa-user-circle" aria-hidden="true"></i>&nbsp;{{user_name}}</h6>
            <p class="card-text">{{post_text}}</p>
            <p><span class="badge badge-dark">{{print_date_time()}}</span></p>
            <slot></slot>
        </div>
    </div>
</template>

<script>

module.exports={
    props:["post_id","post_title","user_name","post_text","post_time"],
    methods:{
        print_date_time:function(){
            date=new Date(this.post_time);
            return date.toLocaleDateString("en-US")+" "+date.toLocaleTimeString("en-US",{timeStyle:"short"});
        },
        random_place_holder_img:function(){
            //temp
            return "/web/img/placeholder"+Math.floor((Math.random()*4)+1)+".jpg";
        }
    }
}
</script>