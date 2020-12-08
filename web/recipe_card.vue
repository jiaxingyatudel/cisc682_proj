<style>
.recipe_card{
    margin-bottom: 10px;
}
</style>

<template>
    <div class="card recipe_card">
        <div class="card-body">
            <h5 class="card-title">{{post_title}}</h5>
            <p class="card-text">{{post_text}}</p>
            <p><span class="badge badge-light">{{print_date_time()}}</span></p>
            <slot></slot>
        </div>
    </div>
</template>

<script>
module.exports={
    props:["post_id","post_title","post_text","post_time"],
    methods:{
        print_date_time:function(){
            date=new Date(this.post_time);
            return date.toLocaleDateString("en-US")+" "+date.toLocaleTimeString("en-US",{timeStyle:"short"});
        }
    }
}
</script>