<style>
#menu_btn_container{
    position: absolute;
    top: 10px;
    right: 10px;
}

#menu_btn{
    width: 62px;
}

#compose_btn_container{
    position: absolute;
    bottom: 10px;
    right: 10px;
}

#compose_btn{
    border-radius: 20px;
    width: 40px;
    height: 40px;
}
#compose_btn:hover{
    width: auto;
}

#share_your_recipe{
    margin-left: 10px;
    display: none;
}
#compose_btn:hover>#share_your_recipe{
    display: inline;
}
</style>

<template>
    <div>
        <div id="menu_btn_container" v-if="user_id">
            <button id="menu_btn" type="button" class="btn btn-dark dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <i class="fa fa-bars" aria-hidden="true"></i>&nbsp;
            </button>
            <div class="dropdown-menu dropdown-menu-right" aria-labelledby="menu_btn">
                <router-link class="dropdown-item" to="/following_users"><i class="fa fa-users" aria-hidden="true"></i>&nbsp;Following</router-link>
                <router-link class="dropdown-item" to="/my_recipes"><i class="fa fa-folder-open" aria-hidden="true"></i>&nbsp;My Recipes</router-link>
            </div>
        </div>
        <div id="compose_btn_container" v-if="user_id">
            <router-link tag="button" class="btn btn-dark" id="compose_btn" type="button" to="/compose">
                <span><i class="fa fa-pencil" aria-hidden="true"></i></span><span id="share_your_recipe">Share your recipe</span>
            </router-link>
        </div>
    </div>
</template>

<script>
module.exports={
    computed:{
        user_id:function(){
            return store.state.user_id;
        }
    }
}
</script>