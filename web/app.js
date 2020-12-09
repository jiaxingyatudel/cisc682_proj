const store=new Vuex.Store({
    state:{
        user_id:false,
        user_checked:false
    },
    mutations:{
        user_check(state,user_id){
            state.user_id=user_id;
            state.user_checked=true;
        }
    }
});

const routes=[
    {
        path:"/",
        name:"home",
        component:httpVueLoader("/web/home.vue")
    },
    {
        path:"/home",
        name:"home",
        component:httpVueLoader("/web/home.vue")
    },
    {
        path:"/following_users",
        component:httpVueLoader("/web/following_users.vue"),
        beforeEnter:function(to,from,next){
            if((store.state.user_checked)&&(!store.state.user_id)){
                next({path:"/"});
            }else{
                next();
            }
        }
    },
    {
        path:"/liked_recipes",
        name:"liked_recipes",
        component:httpVueLoader("/web/liked_recipes.vue"),
        beforeEnter:function(to,from,next){
            if((store.state.user_checked)&&(!store.state.user_id)){
                next({path:"/"});
            }else{
                next();
            }
        }
    },
    {
        path:"/my_recipes",
        name:"my_recipes",
        component:httpVueLoader("/web/my_recipes.vue"),
        beforeEnter:function(to,from,next){
            if((store.state.user_checked)&&(!store.state.user_id)){
                next({path:"/"});
            }else{
                next();
            }
        }
    },
    {
        path:"/user_recipes/:user_id",
        name:"user_recipes",
        component:httpVueLoader("/web/user_recipes.vue"),
        props:true
    },
    {
        path:"/compose",
        name:"compose",
        component:httpVueLoader("/web/compose.vue"),
        beforeEnter:function(to,from,next){
            if((store.state.user_checked)&&(!store.state.user_id)){
                next({path:"/"});
            }else{
                next();
            }
        }
    }
];

const router=new VueRouter({
    routes:routes
});

(async function(){
    const response=await fetch("/check_user_cookie",{
        method:"POST",
        credentials:"include"
    });
    if(response.ok){
        const resp=await response.json();
        if(!resp.err){
            store.commit("user_check",resp.user_id);
        }else{
            store.commit("user_check",false);
        }

        new Vue({
            el:"#app",
            router:router,
            components:{
                "nav_menu":httpVueLoader("/web/menu.vue"),
                "user":httpVueLoader("/web/user.vue")
            }
        });
    }
})();